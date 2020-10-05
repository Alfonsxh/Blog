---
title: "流畅的Python - 第18章-使用asyncio处理并发"
date: 2018-08-18 10:52:18
lastmod: 2018-08-18 10:52:18
draft: false
keywords: ["Books", "流畅的Python"]
description: "第18章-使用asyncio处理并发"
tags: ["Books", "流畅的Python"]
categories: ["Books", "流畅的Python"]
author: "Alfons"
---

## 线程与协程对比

`线程`处理任务时，所有的线程争抢CPU的资源；`协程`处理任务时，由单线程完成，所有的任务都有序的安排在未来进行执行。

<!--more-->

![18-deff-between-thread-and-coroutine](/images/Books/ProfessionBooks/流畅的Python/18-deff-between-thread-and-coroutine.png)

书上的[示例](https://github.com/Alfonsxh/FluentPython/tree/master/18-Asyncio)主要讲了实现动画形式显示文本式旋转指针，线程和协程两种不同的方式。

线程方面，主要使用了`threading`模块中的`Thread`方法创建线程并执行。注意的一点是，python中的线程`不提供终止线程的API`，所以需要给线程发送消息才能关闭线程，如此例中的`signal.go`属性。

```python
def supervisor():
    """
    启动线程开始执行
    :return: 返回结果
    """
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("thinking", signal))
    print("Spinner object -> {} begin".format(spinner))
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result
```

通过`asyncio`模块创建协程的要求比较多。

- 首先需要有一个`事件循环`，使用`asyncio.get_event_loop()`产生。
- 然后使用`run_until_complete`将`协程`注册到`事件循环`中。`run_until_complete`接收`Future对象`或者`Task任务(为Future对象的子类)`，也可以接收`普通的协程`，默认会将协程封装成`Task`。
- task对象可以使用`loop.create_task(supervisor())`实现，也可以使用`asyncio.ensure_future(supervisor())`实现。
- 最后全部任务执行完后返回所有的结果，`run_until_complete`接收什么参数，就返回对应参数返回的结果。如果传入的是`wait_coro`，则返回`wait_coro`对象所做的事，返回一个元组。

```python
async def supervisor():
    """
    事件驱动的参数函数
    :return: 返回思考结果
    """
    # spinner = asyncio.async(spin("thinking"))         # update asyncio.async to asyncio.ensure_future
    spinner = asyncio.ensure_future(spin("thinking"))
    print("Spinner -> {} begin.".format(spinner))
    result = await slow_function()
    spinner.cancel()
    return result


def main():
    loop = asyncio.get_event_loop()  # 获取事件循环
    result = loop.run_until_complete(supervisor())  # 驱动supervisor协程，返回参数返回的结果
    loop.close()  # 关闭事件驱动
    print("Answer:", result)
```

线程方式与协程方式的对比如下：

- 协程中不建议使用`time.sleep(...)`来进行时间的等待，会引起阻塞。推荐的是使用`await asyncio.sleep(...)`代替。
- 用于驱动协程的`Task对象`不能由自己动手实例化，而是通过把协程传给`async.async(...)函数`或者`loop.create_task(...)方法`获取。获取完后的`Task对象`的执行时间已经确定！在线程中，必须调用`start()方法`才能运行线程。
- 线程不能通过外部的API进行停止，协程可以通过使用`Task.cancel()`实例方法，在协程内部抛出`asyncio.CancelledError`异常，协程可以在暂停的`yield`处捕获此异常进行退出操作。
- 在协程中，supervisor()函数(或者task对象)必须由`loop.run_until_complete()`执行。
