---
title: "Python中一种单例无效的情况"
date: 2019-06-26 22:24:42
lastmod: 2019-06-26 22:24:42
draft: false
keywords: ["Python"]
description: "Python中一种单例无效的情况"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

在Python中，如果要创建一个单例，通常有两种方式。

<!--more-->

第一种，利用python的模块的特性，先创建一个对象，其他的模块通过导入此模块，来实现单例。

```python
class SingleCls:
    def __init__(self):
        self.__info_list = list()
        # self.__info_list = multiprocessing.Manager().list()

    def AddMessage(self, message):
        self.__info_list.append("Hello %s" % message)

    def __repr__(self):
        return str(self.__info_list)

single_obj = SingleCls()
```

另一种，使用python一切皆对象的属性，**类也属于对象，使用类中的类属性来保存创建好的单例**。

```python
class SingleCls:
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(SingleCls, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.__info_list = list()

    def AddMessage(self, message):
        self.__info_list.append("Hello %s" % message)

    def __repr__(self):
        return str(self.__info_list)

single_obj = SingleCls()
```

单例的本质是，不同模块使用的是同一个对象，这需要在 **‘第三方’** 的领土上创建。

可是在多进程的环境中，结果却不一定了。

- 多进程的环境中，子进程通过fork产生，会拷贝父进程中的变量，单例也不例外。
- 所以，子进程中的单例对象，已经各不相同了！
- 导致的结果就是，虽然子进程中对单例对象进行了很多操作，但是父进程中的单例对象却未发生改变。

```python
def func(m):
    single_obj.AddMessage(m)
    print("single_obj {m} -> ".format(m=m), single_obj)


func("1")
func("2")
func("3")
pool = multiprocessing.Pool(4)
pool.apply(func, args=("First",))
pool.apply(func, args=("Second",))
pool.apply(func, args=("Third",))
# pool.apply(single_obj.AddMessage, args=("First",))
# pool.apply(single_obj.AddMessage, args=("Second",))
# pool.apply(single_obj.AddMessage, args=("Third",))
pool.close()
pool.join()

print(single_obj)
```

输出如下所示：

```shell
single_obj 1 ->  ['Hello 1']
single_obj 2 ->  ['Hello 1', 'Hello 2']
single_obj 3 ->  ['Hello 1', 'Hello 2', 'Hello 3']
single_obj First ->  ['Hello 1', 'Hello 2', 'Hello 3', 'Hello First']
single_obj Second ->  ['Hello 1', 'Hello 2', 'Hello 3', 'Hello Second']
single_obj Third ->  ['Hello 1', 'Hello 2', 'Hello 3', 'Hello Third']
['Hello 1', 'Hello 2', 'Hello 3']
```