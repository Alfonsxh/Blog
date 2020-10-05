---
title: "如何杀死Python subprocess.Popen创建的进程"
date: 2018-09-28 21:51:01
lastmod: 2018-09-28 22:01:27
draft: false
keywords: ["Python"]
description: "如何杀死Python subprocess.Popen创建的进程"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

在使用`Popen`模块创建进程执行时，发现启动的进程`proc`在使用`proc.kill()`后，仍然存在。

<!--more-->

```python
import time
from subprocess import Popen, PIPE

# airodumpProc = Popen(["/usr/local/sbin/airodump-ng", "wlan0"])
airodumpProc = Popen("/usr/local/sbin/airodump-ng wlan0", shell = True)

time.sleep(10)
airodumpProc.kill()

while True:
    time.sleep(3)
```

例如上面的代码，使用`Popen`模块运行`airodump-ng`程序扫描周边的Wifi。程序启动后会在主进程下生成好几个子孙进程。

经过10秒后杀死进程，对应主进程下的子孙进程消失，但是并没有真正的消失。

处理前：

![Popen_shell_process_htop](/images/Python/Python杀不死的子进程/Popen_shell_process.jpg)

处理后：

![Popen_shell_kill_process_1](/images/Python/Python杀不死的子进程/Popen_shell_kill_process_1.jpg)

![Popen_shell_kill_process_2](/images/Python/Python杀不死的子进程/Popen_shell_kill_process_2.jpg)

可以使用`pgrep airodump-ng -a`命令看见，之前执行任务的子孙进程仍在运行中，不过在主进程中的状态已经不存在。只有当关闭执行程序时，相关进程才会退出。

![Popen_shell_watch_process_1](/images/Python/Python杀不死的子进程/Popen_shell_watch_process_1.jpg)

使用`os.kill(pid, sig)`命令同样杀不死。之前一直使用的是`pkill airodump-ng`的方式杀死所有同名的进程，现在有的需求是，需要保留其余同名的进程，而只让目标进程及其子孙进程停止工作。

Google了一下，发现提供的方法大多是`os.killpg()`的方式，但这种方式会杀死进程所属的组进程，导致程序退出，显然无法满足现在的需要。

其他方法也试了，都无法解决实际问题。

现在找到的方法比较笨，找到主进程下所有的子孙进程，一个个杀死，再杀死主进程。

```python
import time
import os
import signal
import psutil
from subprocess import Popen, PIPE


def KillProcByPid(pid):
    """
    根据进程id杀死对应进程下的所有进程，包括子进程
    :param pid: 进程ID
    :return:
    """
    proc = psutil.Process(pid)
    childProc = proc.children(recursive = True)
    for p in childProc:
        os.kill(p.pid, signal.SIGKILL)
    os.kill(pid, signal.SIGKILL)


# airodumpProc = Popen(["/usr/local/sbin/airodump-ng", "wlan0"])
airodumpProc = Popen("/usr/local/sbin/airodump-ng wlan0", shell = True)

time.sleep(10)
# airodumpProc.kill()
KillProcByPid(airodumpProc.pid)

while True:
    time.sleep(3)
```

使用`psutil.Process(pid)`方法，附着目标进程，获取目标进程下的所有子孙进程，参数`recursive = True`表示的是获取子孙进程。

获取子孙进程后，得到子孙进程的pid，根据pid，一个个杀死子孙进程，最后结束主进程。

进程此番处理后，目标主进程下的子孙进程就都处理完毕了。

处理前：

![Popen_shell_process2](/images/Python/Python杀不死的子进程/Popen_shell_process2.jpg)

处理后：

![Popen_shell_watch_process_2](/images/Python/Python杀不死的子进程/Popen_shell_watch_process_2.jpg)