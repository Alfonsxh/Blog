---
title: "Python pyconcrete加解密py文件"
date: 2020-06-03 22:53:48
lastmod: 2020-06-03 22:53:48
draft: false
keywords: ["Python", "pyconcrete"]
description: "Python pyconcrete加解密py文件"
tags: ["Python", "pyconcrete"]
categories: ["Python", "pyconcrete"]
author: "Alfons"
---

**pyconcrete** 是一个加密模块，可以将py文件，通过AES加密的方式，将py文件编译过后的pyc文件转换成家秘密后的pye文件，在使用时，再通过AES解密出pyc源码，直接加载到内存中，进行执行。

这种方式可以暂时保证源码不被泄漏，但是，加密的方式为对称加密，只要知道密钥，就能解密出pyc源码，再通过其他方式，就能还原出py文件。

<!--more-->

## 安装过程

通过 `pip install` 的方式无法正确安装，建议是通过源码编译的方式进行安装。

```shell
> git clone https://github.com/Falldog/pyconcrete.git
> cd pyconcrete
> python setup.py build
running build
please input the passphrase # 输入密码
for encrypt your python script (enter for default) : 
xxxxxx
please input again to confirm   # 再次确认
xxxxxx
running build_py
...
```

编译安装的核心在于，**通过注入的方式，将AES密钥写入头文件 secret_key.h 中**，然后编译成动态库，使得密钥不暴露。因此，一个密钥文件对应一个动态库，不同的密钥生成的动态库，不可以相互解密。

```python
# setup.py
def create_secret_key_header(key, factor):
    # reference from - http://stackoverflow.com/questions/1356896/how-to-hide-a-string-in-binary-code
    # encrypt the secret key in binary code
    # avoid to easy read from HEX view

    key_val_lst = []
    for i, k in enumerate(key):
        n = ord(k) if PY2 else k
        key_val_lst.append("(0x%X ^ (0x%X - %d))" % (n, factor, i))
    key_val_code = ", ".join(key_val_lst)
    
    # 格式化待注入的c头文件内容
    code = """
        #define SECRET_NUM 0x%X
        #define SECRET_KEY_LEN %d
        static const unsigned char* GetSecretKey()
        {
            unsigned int i = 0;
            static unsigned char key[] = {%s, 0/* terminal char */};
            static int is_encrypt = 1/*true*/;
            if( is_encrypt )
            {
                for(i = 0 ; i < SECRET_KEY_LEN ; ++i)
                {
                    key[i] = key[i] ^ (SECRET_NUM - i);
                }
                is_encrypt = 0/*false*/;
            }
            return key;
        }
    """ % (factor, len(key), key_val_code)
    
    # 将密钥写入 secret_key.h 中
    with open(SECRET_HEADER_PATH, 'w') as f:
        f.write(code)
```

build完后，会生成python的 **pyconcrete模块**，其中的动态库文件中，已经包含了安装时输入的AES密钥。目录结构如下：

```shell
build/lib.linux-x86_64-3.6/pyconcrete/
├── __init__.py
├── _pyconcrete.cpython-36m-x86_64-linux-gnu.so # 安装后，会重命名为 _pyconcrete.so
└── version.py
```

其中 **__init__.py** 文件中包含的即是动态库的py调用。

```python
from . import _pyconcrete

info = _pyconcrete.info
encrypt_file = _pyconcrete.encrypt_file
decrypt_file = _pyconcrete.decrypt_file
decrypt_buffer = _pyconcrete.decrypt_buffer     # 解密函数

class PyeLoader(object):
    ...

    def load_module(self, fullname):
        if fullname in sys.modules:  # skip reload by now ...
            return sys.modules[fullname]

        data = decrypt_buffer(self.data)  # 主要功能！！！decrypt pye！！！

        self._validate_version(data)

        if sys.version_info >= (3, 7):
            # reference python source code
            # python/Lib/importlib/_bootstrap_external.py _code_to_timestamp_pyc() & _code_to_hash_pyc()
            # MAGIC + HASH + TIMESTAMP + FILE_SIZE
            magic = 16
        elif sys.version_info >= (3, 3):
            # reference python source code
            # python/Lib/importlib/_bootstrap_external.py _code_to_bytecode()
            # MAGIC + TIMESTAMP + FILE_SIZE
            magic = 12
        else:
            # load pyc from memory
            # reference http://stackoverflow.com/questions/1830727/how-to-load-compiled-python-modules-from-memory
            # MAGIC + TIMESTAMP
            magic = 8

        code = marshal.loads(data[magic:])      # 加载解密后的pyc文件内容

        m = self.new_module(fullname, self.full_path, self.pkg_path)
        sys.modules[fullname] = m
        exec(code, m.__dict__)
        return m

    ...


class PyeMetaPathFinder(object):
    def find_module(self, fullname, path=None):
        mod_name = fullname.split('.')[-1]
        paths = path if path else sys.path

        for trypath in paths:
            mod_path = join(trypath, mod_name)
            is_pkg = isdir(mod_path)
            if is_pkg:
                full_path = join(mod_path, '__init__' + EXT_PYE)
                pkg_path = mod_path
            else:
                full_path = mod_path + EXT_PYE
                pkg_path = trypath

            if exists(full_path):
                return PyeLoader(is_pkg, pkg_path, full_path)

sys.meta_path.insert(0, PyeMetaPathFinder())    # 导入模块hook，会在每次加载模块时，进行pye文件的解密
```

## 加密过程

例如，加密测试文件 **src_file.py**。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
print("hello world")
```

进行加密

```shell
> ./pyconcrete-admin.py compile --source=../src_file.py --pye
> ls
src_file.py  src_file.pye
```

## 解密过程

首先利用同一动态库中的 **decrypt_buffer方法**，进行解密，**pye -> pyc**。

```python
import os
from pyconcrete._pyconcrete import decrypt_buffer

pye_dir = "./pye_dir"
pyc_dir = "./pyc_dir"

if not os.path.isdir(pyc_dir):
    os.mkdir(pyc_dir)

for file_name in os.listdir(pye_dir):
    with open(os.path.join(pye_dir, file_name), 'rb') as f:
        data = decrypt_buffer(f.read())  # decrypt pye

    with open(os.path.join(pyc_dir, file_name[:file_name.rfind('.')] + '.pyc'), 'wb') as f:
        f.write(data)
```

在 **pyc_dir路径** 下，生成解密的pyc文件。此时的文件仍为不可读内容，需要通过其他方式反编译为py文件。

```shell
> pip install uncompyle6
> uncompyle6 -o dst_file.py src_file.pyc 
src_file.pyc -- 
# Successfully decompiled file
```

反编译后的 **dst_file.py** 内容如下：

```python
# uncompyle6 version 3.7.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.5 (default, Apr  1 2018, 05:46:30) 
# [GCC 7.3.0]
# Embedded file name: ../src_file.py
# Compiled at: 2020-05-28 23:20:22
# Size of source mod 2**32: 182 bytes
print('hello world')
```

## 总结

看似很高级的加密方式，防止他人窥探源码，实则鸡肋到不行，稍微了解一点，即可破解。

## 参考

- [pyconcrete git](https://github.com/Falldog/pyconcrete)
- [uncompyle6 git](https://github.com/rocky/python-uncompyle6)