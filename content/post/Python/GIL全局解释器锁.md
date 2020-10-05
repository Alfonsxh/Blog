---
title: "Python GIL"
date: 2019-01-30 13:32:21
lastmod: 2019-01-30 13:41:53
draft: false
keywords: ["Python"]
description: "Python GIL"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

对于CPU密集型程序来说，使用Python作为开发工具，是一个失败的尝试，因为 `GIL(Global Interpreter Lock)`。

**GIL** 译为 **全局解释器锁**。是的，是 **解释器锁**。

<!--more-->

首先要认清的一点是，**GIL** 并不是 **Python** 特性，它是实现Python解释器(CPython)时所引入的一个概念。对于其他的解释器，**JPython解释器** 就没有 **GIL**。但由于历史的原因，大部分情况下，我们默认使用 **CPython** 作为解释器，久而久之，我们就习惯了----**Python的GIL**。

要不要使用 **JPython作为解释器** 呢？可以尝试，但最好不要，如果使用 **JPython作为解释器**，那么许多 **Python** 使用的 **c语言插件** 将无法使用...

## GIL

早期编程是没有多线程的概念的，当时的CPU还只能是单核的。随着多核CPU的出现，为了有效的利用CPU多个核心的性能，多线程编程的方式慢慢的热了起来，但随之也带来了一些问题：**线程间数据一致性和状态同步的困难**。

最简单的办法就是 **加锁**，于是就有了 **GIL** 这把 **大锁**！

**CPython 设置 GIL** 最大的好处是 ---- **线程安全**。不让多个线程同时执行同一条字节码，避免了可能多个线程同时对某个对象进行操作。

### GIL设计原理

最初设计GIL时，是基于操作系统本身的线程调度，社区认为 **现在操作系统的线程调度方案已经非常成熟稳定了，没必要自己再弄一套**。所以，Python的线程就是 **C语言的一个pthread**。

为了让各个线程能够平均利用CPU时间，python会计算当前 **已执行的微代码的数量**，达到一定数量后就强制释放GIL。

伪代码如下：

```c
while True:
    acquire GIL
    for i in 1000:
        do something
    release GIL
    /* Give Operating System a chance to do thread scheduling */
```

可以看到，在获取和释放GIL时，时间间隔十分的短暂。当只有一个CPU核心时，任何一个线程被唤醒，都能成功获得GIL。

但当有多个CPU核心时，问题就来了：当一个核心上的线程释放了GIL后，另一个核心上的线程来获取时，往往是之前核心上的线程又获取了GIL，后面的线程只能是等待之前的线程执行完毕才能真正的获取到GIL。

![GIL_with_diff_CPU](/images/Python/GIL全局解释器锁/GIL_with_diff_CPU.jpg)

上面的图，是发生在运行 **CPU密集型任务** 时。第一个表示的是，单个CPU核心上运行两个线程，可以看到程序运行的十分流畅。但当使用两个CPU核心运行两个线程时，大部分时间是，GIL获取失败，浪费了大量的CPU时间。

对于 **I/O密集型** 程序来说，大部分时间是在处理数据的读写，解释器会在进行I/O操作时将GIL释放。但是，**如果在I/O密集型操作的线程中，如果出现了CPU密集型线程，那么在运行CPU密集型线程时，该线程仍然会一直占用CPU！**

现在GIL这种方式被证明是 **蛋疼的也是低效的**，但当我们试图去把 **GIL** 排除时，根据 **CPython解释器** 设计的模块已经太多了，想要去掉GIL将是件浩大的工程。(Python 3.6 版本似乎对 GIL 有了些优化，下面的例子可以看到)

## 实验

下面分别使用单线程、多线程、多进程在四核CPU上进行 **CPU密集型** 程序测试。

```python
# 单线程程序
import time


def single_thread(n):
    for i in range(n):
        pass


if __name__ == '__main__':
    start_time = time.time()
    single_thread(10 ** 8)
    print("use time: {}'s.".format(time.time() - start_time))
```

在使用python2.7时，所用的时间为： **3.30's**。使用python3.6时，所用的时间为： **1.90's**。

```python
# 多线程
import time
from threading import Thread


def single_thread(n):
    for i in range(n):
        pass


def multi_thread(n, thread_num):
    thread_list = list()
    for _ in range(thread_num):
        t = Thread(target = single_thread, args = (int(n / thread_num),))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    start_time = time.time()
    multi_thread(10 ** 8, 2)
    print("use time: {}'s.".format(time.time() - start_time))
```

在使用python2.7时，所用的时间为： **4.35's**。使用python3.6时，所用的时间为： **1.72's**。

```python
# 多进程
import time
from multiprocessing import Process


def single_thread(n):
    for i in range(n):
        pass


def multi_thread(n, thread_num):
    thread_list = list()
    for _ in range(thread_num):
        t = Process(target = single_thread, args = (int(n / thread_num),))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    start_time = time.time()
    multi_thread(10 ** 8, 2)
    print("use time: {}'s.".format(time.time() - start_time))
```

在使用python2.7时，所用的时间为： **1.82's**。使用python3.6时，所用的时间为： **1.00's**。

汇总如下：

|程序|Python版本|运行时间|
|:---:|:---:|:---:|
|**单线程**|**2.7**|**3.30's**|
|**单线程**|**3.6**|**1.90's**|
|**多线程**|**2.7**|**4.35's**|
|**多线程**|**3.6**|**1.72's**|
|**多进程**|**2.7**|**1.82's**|
|**多进程**|**3.6**|**1.00's**|

可以看到，对于Python2.7版本，**在使用多线程进行CPU密集型计算时，比使用单线程还要慢**！多进程的方式，每个进程单独含有自己的GIL锁，所以不会出现跨进程GIL的问题。

另外，Python3.2版本开始，社区陆续对GIL做了比较深入的优化，现在使用python3.6版本测试同样的程序，在效率上有了很大的提升。

## 解决方案

如何避免GIL导致的CPU利用效率低下的问题呢？下面有一些方案可供参考。

### 使用multiprocessing代替threading

可以从上面的实验看到，在使用多进程的方法后，运行效率均有了很大的提升，这是因为，在使用多进程时，每个进程会单独开启一个解释器，各个进程中的GIL不会相互影响。

当然，多进程使用时也会有些不同的地方。在使用 **多线程(Thread)** 时，对于共有的变量，我们只需声明一个 **global** 变量就行了，不同线程调用时只需 **加锁解锁** 即可。但对于 **多进程(Process)** 来说，不能通过这种方法来在进程间传递值了，每个子进程会复制一份 **global变量**，改变的变量只对各自的进程有效。

### 使用C扩展编程技术

这种方案的主要思想是，在进行CPU密集型计算时，我们可以 **将CPU密集型计算任务转移到C语言程序上**。

**C扩展最重要的特性是它们和Python解释器是保持独立的**，也就是说，C扩展不会和Python程序竞争GIL。因此，可以将计算密集型程序使用C扩展来计算，而Python程序主要完成 **I/O密集型操作**。

可以使用下面的方式释放GIL。具体参考：[从C扩展中释放全局锁](https://python3-cookbook.readthedocs.io/zh_CN/latest/c15/p07_release_the_gil_in_c_extensions.html)

```c
#include "Python.h"
...

PyObject *pyfunc(PyObject *self, PyObject *args) {
   ...
   Py_BEGIN_ALLOW_THREADS
   // Threaded C code.  Must not use Python API functions
   ...
   Py_END_ALLOW_THREADS
   ...
   return result;
}
```

典型的例子 ---- **Numpy**。

### 不使用CPython作为解释器

这种方法要慎之又慎，因为大部分Python模块都是基于 **CPyhton解释器** 进行编写的，其他解释器或许没有对应的版本。

没有GIL的解释器现在已知的解释器：**Jython**、**IronPython**、**PyPy-STM**。

## 参考

- [Python的GIL是什么鬼，多线程性能究竟如何](http://cenalulu.github.io/python/gil-in-python/)
- [Understanding the Python GIL](http://www.dabeaz.com/GIL/)
- [12.9 Python的全局锁问题](https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p09_dealing_with_gil_stop_worring_about_it.html)
- [15.7 从C扩展中释放全局锁](https://python3-cookbook.readthedocs.io/zh_CN/latest/c15/p07_release_the_gil_in_c_extensions.html)
- [Is there a Python implementation without the GIL?](https://www.quora.com/Is-there-a-Python-implementation-without-the-GIL)