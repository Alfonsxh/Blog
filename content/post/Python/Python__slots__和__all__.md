---
title: "Python \_\_slots\_\_和\_\_all\_\_"
date: 2019-01-25 22:35:00
lastmod: 2019-01-26 23:39:42
draft: false
keywords: ["Python"]
description: "Python \_\_slots\_\_和\_\_all\_\_"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

## \_\_slots\_\_

在python中，我们可以在实例化对象后绑定对象的方法或属性：

<!--more-->

```python
class Employer:
    pass


e = Employer()
e.name = "alfons"
print("name is -> ", e.name)

e.salary = 1000
print("salary is -> ", e.salary)

# output
name is ->  alfons
salary is ->  1000
```

**\_\_slots\_\_** 在类中声明，类型为 **list 或 tuple**，表示的是 **对象在实例化后能够绑定的属性的限制**，也就是说，之后绑定的属性名被限定在 **\_\_slots\_\_** 中。

```python

class Employer:
    __slots__ = ["name"]
    pass


e = Employer()
e.name = "alfons"
print("name is -> ", e.name)

e.salary = 1000
print("salary is -> ", e.salary)

# output
name is ->  alfons
Traceback (most recent call last):
  File "/mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/MagicMethod/__slots__.py", line 19, in <module>
    e.salary = 1000
AttributeError: 'Employer' object has no attribute 'salary'
```

如果子类继承了父类，并且父类中声明了 **\_\_slots\_\_** ，子类的情况会出现两种：

- **子类中未声明**，那么子类不会继承父类中的 **\_\_slots\_\_**。
- 子类中也声明了 **\_\_slots\_\_**，那么就会继承父类的 **\_\_slots\_\_**。
 
(有点绕啊)

```python
# 1 子类不声明
class Human:
    __slots__ = ["name"]


class Employer(Human):
    pass


e = Employer()
e.name = "alfons"
print("name is -> ", e.name)

e.salary = 1000
print("salary is -> ", e.salary)

# output
name is ->  alfons
salary is ->  1000

# 2 子类声明
class Human:
    __slots__ = ["name"]


class Employer(Human):
    __slots__ = ["salary"]


e = Employer()
e.name = "alfons"
print("name is -> ", e.name)

e.salary = 1000
print("salary is -> ", e.salary)

e.sex = "male"
print("sex is -> ", e.sex)

# ouput
name is ->  alfons
salary is ->  1000you hua
Traceback (most recent call last):
  File "/mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/MagicMethod/__slots__.py", line 25, in <module>
    e.sex = "male"
AttributeError: 'Employer' object has no attribute 'sex'
```

另外，如果 **\_\_slots\_\_** 中包含了 **\_\_dict\_\_**，则 **\_\_slots\_\_** 将不起作用！！

```python
class Human:
    __slots__ = ["name"]


class Employer(Human):
    __slots__ = ["__dict__", "salary"]


e = Employer()
e.name = "alfons"
print("name is -> ", e.name)

e.salary = 1000
print("salary is -> ", e.salary)

e.sex = "male"
print("sex is -> ", e.sex)

# output
name is ->  alfons
salary is ->  1000
sex is ->  male
```

### 降低内存使用

其实， **\_\_slots\_\_** 最主要的作用还是 **降低设备的内存使用**，它限定了实例中属性的范围。

例子可以参考：[Saving 9 GB of RAM with Python’s __slots__](http://tech.oyster.com/save-ram-with-python-slots/)

(不过我做实验却得不到差异，不知道是不是现在的版本已经做了相关的优化。至少Pypy是已经优化的了。)

## \_\_all\_\_

在标准库模块中，经常会看见 **\_\_all\_\_** 列表，里面会包含很多字符串，字符串的名称与该模块的导入函数有许多相同的名称。如下所示:

```python
# struct.py
__all__ = [
    # Functions
    'calcsize', 'pack', 'pack_into', 'unpack', 'unpack_from',
    'iter_unpack',

    # Classes
    'Struct',

    # Exceptions
    'error'
    ]

from _struct import *
from _struct import _clearcache
from _struct import __doc__
```

**\_\_all\_\_** 表示的是程序中在 `import *` 后能够直接使用的集合。例如下面：

```python
from struct import *

p = pack("I2s", 2, b"he")
print(p)

u_p = unpack("I2s", p)
print(u_p)
```

**struct** 模块中 **\_\_all\_\_** 中包含了 **pack() 和 unpack()** 函数，因此，在程序中可以直接使用。

不过我不太喜欢这种用法，相比于上面直接使用函数，更喜欢加上所属的模块，明了一些。

```python
import struct

p_2 = struct.pack("I2s", 2, b"he")
print(p_2)

u_p_2 = struct.unpack("I2s", p_2)
print(u_p_2)
```