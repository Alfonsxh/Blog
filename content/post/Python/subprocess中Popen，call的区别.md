---
title: "subprocess中Popen，call的区别"
date: 2018-07-07 19:12:47
lastmod: 2018-07-07 19:12:47
draft: false
keywords: ["Python"]
description: "subprocess中Popen，call的区别"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

这两天测试的时候，发现使用Popen创建的进程没有把命令执行完毕，导致程序Bug～

<!--more-->

观察了一下，subprocess模块，执行系统命令有两种方式，Popen或者call。


但是使用Popen运行的进程会在后台运行，并不是等待进程结束才进行下一步操作。

```python
import datetime
from subprocess import call, Popen

print("Start time {time}.".format(time=datetime.datetime.now()))

prog = Popen("sleep 3; touch popen.txt", shell=True)
print("Popen finish time {time}.".format(time=datetime.datetime.now()))

call("sleep 3; touch call.txt", shell=True)
print("call finish time {time}.".format(time=datetime.datetime.now()))
```

上面代码产生的结果为：

```shell
Start time 2018-06-20 22:48:17.665699.
Popen finish time 2018-06-20 22:48:17.666363.
call finish time 2018-06-20 22:48:20.669785.
```

可以看到，Popen运行并没有等待命令运行完毕，而call运行的进程会等待命令运行完毕，才继续下一步操作。

查看subprocess源码，可以看到，Popen为subprocess的一个类，call为subprocess的一个方法。

```python
def call(*popenargs, timeout=None, **kwargs):
    """Run command with arguments.  Wait for command to complete or
    timeout, then return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])
    """
    with Popen(*popenargs, **kwargs) as p:
        try:
            return p.wait(timeout=timeout)
        except:
            p.kill()
            p.wait()
            raise
```

从源码中可以看到，call方法其实调用的是Popen类，p.wait是等待Popen运行的进程结束才退出。

所以呢，以后在需要在程序中运行系统命令时，如果需要等待命令执行完成，还是使用call来执行。或者，麻烦一点，在使用Popen执行后，加上Popen.wait()，等待命令执行完毕。

