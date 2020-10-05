---
title: "Python中的进程池和线程池"
date: 2019-06-26 22:24:42
lastmod: 2019-06-26 22:24:42
draft: false
keywords: ["Python"]
description: "Python中的进程池和线程池"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

最近有用Python标准模板库里的线程池实现一些东西，发现非常好用，记录一下。

<!--more-->

## 非模板库实现

之前自己实现线程池呢，有两种

- 创建线程时提供输入参数
- 使用任务队列

```python
def func(x, return_dict):
    time.sleep(1)
    print(x << 2)
    return_dict[x] = x * x

def PoolByUser():
    pool = list()
    return_dict = dict()

    for i in range(10):
        p = threading.Thread(target=func, args=(i, return_dict))
        p.start()
        pool.append(p)

    for p in pool:
        p.join()

    print(return_dict)
```

第一种方式，先创建list用来保存线程。**return_dict** 为保存结果的字典。多线程比多进程实现的好处在于，**主进程中的变量在多个子线程中是共享的**，无需复杂的操作。

结束时，需要挨个停止。

```python
task_queue = Queue()
need_run = True
return_dict = dict()


def task_func(return_dit):
    while need_run:
        try:
            x = task_queue.get(timeout=2)
            return_dit.update({x: x * x})
        except:
            pass


def PoolUseTaskQueue():
    t_list = list()
    for i in range(10):
        t = threading.Thread(target=task_func, args=(return_dict,))
        t.start()
        t_list.append(t)

    [task_queue.put(i) for i in range(20)]

    global need_run
    need_run = False
    for t in t_list:
        t.join()
    print(return_dict)
```

第二种方式，通过模拟任务队列的方式实现。先创建多个线程，然后将需要的输入参数传入队列中，每个子线程通过任务队列来获取输入的参数。标准模板库中的队列对象内部，已经实现了锁的功能，无需自己实现。

## 标准模板库实现

标准模板库中实现多线程和多进程的方法十分简单！

```python
pool = multiprocessing.Pool(4)
pool.apply(func, args=("First",))
pool.apply(func, args=("Second",))
pool.apply(func, args=("Third",))
pool.close()
pool.join()
```

如上，只需创建多进程池，然后将方法添加池中，既可。相关函数功能简介如下：

- **apply** - 最简单的方式，传入参数为方法，和该方法所需的入参。
- **apply_async** - 上述方式的异步实现模式。
- **map** - 传入的参数为方法，以及该方法所需的参数迭代器，**适用于单个入參的方法**，当然也可以把多个入參当作一个结构体传入。
- **map_async** - 上述方式的异步实现模式。
- **starmap** - 与map不同之处在于，它可以将多个入參一同传入，而不用组成结构体。
- **starmap_async** -上述方式的异步实现模式。

multiprocessing模块还有 **多线程池——ThreadPool**，使用的方式和多进程池的方式一样。

## 进程间通信

进程间的通信方式不同于线程间。子进程在创建时，已经将父进程中的变量copy了一份，导致了每个子进程中 **之前相同的变量都不相同了**，因此不能通过父进程的变量进行子进程间的通信。

这时候需要第三方的机构来做一个类似中间人的过程。

信号、信号量、共享内存、socket、管道、实体文件等等。

multiprocess中Manager对象，可以实例化dict、list对象出来，用于子进程间的通信。

也可以通过multiprocess中的Queue。