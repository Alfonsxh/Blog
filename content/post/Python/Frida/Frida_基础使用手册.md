---
title: "Frida使用手册"
date: 2018-11-29 19:29:58
lastmod: 2018-11-29 19:29:58
draft: false
keywords: ["Python", "Frida"]
description: "Frida使用手册"
tags: ["Python", "Frida"]
categories: ["Python", "Frida"]
author: "Alfons"
---

## 0、介绍

`Frida` 是一个跨平台的应用分析工具。能够注入JavaScript或者自己库的片段注入到 Windows, macOS, Linux, iOS, Android, and QNX 平台的应用上。支持 Google 的 `V8` 引擎，从版本9开始，也支持 `Duktape`。

代码注入的方式很多。`Xposed` 会永久修改Android应用程序加载器，每次启动的新进程都运行的时自己的挂钩程序。

`Frida` 通过将代码直接写入进程内存来实现代码的植入。当附加到正在运行的应用程序时，`Frida`使用`ptrace`来劫持正在运行的进程的线程。该线程用于分配一块内存并使用迷你引导程序填充它。引导程序启动一个新线程，连接到设备上运行的`Frida`调试服务器，并加载包含`Frida`代理程序和检测代码的动态生成的库文件。被劫持的线程在恢复到其原始状态后恢复，并且流程执行继续照常进行。

<!--more-->

![Frida](https://raw.githubusercontent.com/OWASP/owasp-mstg/master/Document/Images/Chapters/0x04/frida.png)

***FRIDA Architecture，来源：http：//www.frida.re/docs/hacking/***

以下是FRIDA在Android上提供的主要API：

- 实例化Java对象并调用静态和非静态类方法
- 替换Java方法实现
- 通过扫描Java堆枚举特定类的实时实例（仅限Dalvik）
- 扫描进程内存以查找字符串
- 拦截本机函数调用以在函数入口和出口处运行您自己的代码

## 1、安装

Windows或Linux上需要安装python模块以及frida-tools工具包。

```linux
pip install frida       # python 模块
pip install frida-tools # frida 工具
```

在Android设备上，需要下载[frida-server](https://build.frida.re/frida-snapshot/android/arm/bin/frida-server)，然后将frida-server工具push到设备上，然后添加可执行权限。

```shell
alfons>$ adb push ./frida-server /data/local/tmp/frida-server
alfons>$ adb shell
alfons>$ cd  /data/local/tmp/frida-server
alfons>$ chmod +x frida-server
alfons>$ ./frida-server
```

注意：Android必须root。

## 2、frida-tools

工具包里包含了以下小工具：

- **frida-ps**
- **frida-discover**
- **frida-ls-devices**
- **frida-kill**
- **frida-trace**

### 2.1、frida-ps

显示特定设备的进程信息，默认为本机的进程。

```shell
alfons>$ frida-ps --help
Usage: frida-ps [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -D ID, --device=ID    connect to device with the given ID
  -U, --usb             connect to USB device
  -R, --remote          connect to remote frida-server
  -H HOST, --host=HOST  connect to remote frida-server on HOST
  -a, --applications    list only applications
  -i, --installed       include all installed applications

# -U 显示usb连接的设备
# -a 显示应用的进程
# -i 显示安装的应用
alfons>$ frida-ps -U -a
 PID  Name                                      Identifier
----  ----------------------------------------  ---------------------------------------
1862  Android Services Library                  com.google.android.ext.services
7808  Chrome                                    com.android.chrome
7179  SuperSU                                   eu.chainfire.supersu
4619  Telegram                                  org.telegram.messenger
6919  YouTube                                   com.google.android.youtube
4526  com.qualcomm.atfwd                        com.qualcomm.atfwd
1935  com.quicinc.cne.CNEService.CNEServiceApp  com.quicinc.cne.CNEService
1585  org.codeaurora.ims                        org.codeaurora.ims
···
```

### 2.2、frida-discover

记录一段时间内各线程调⽤用的函数和符号名。(似乎没什么效果)

```shell
alfons>$ frida-discover --help
Usage: frida-discover [options] target

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -D ID, --device=ID    connect to device with the given ID
  -U, --usb             connect to USB device
  -R, --remote          connect to remote frida-server
  -H HOST, --host=HOST  connect to remote frida-server on HOST
  -f FILE, --file=FILE  spawn FILE
  -n NAME, --attach-name=NAME
                        attach to NAME
  -p PID, --attach-pid=PID
                        attach to PID
  --debug               enable the Node.js compatible script debugger
  --enable-jit          enable JIT
```

### 2.3、frida-ls-devices

显示连接的终端设备信息。

```shell
alfons>$ frida-ls-devices --help
Usage: frida-ls-devices [options]

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit

alfons>$ frida-ls-devices
Id          Type    Name
----------  ------  ----------------
local       local   Local System
ZX1G222TZL  usb     Motorola Nexus 6
tcp         remote  Local TCP
```

### 2.4、frida-kill

杀死特定终端上的指定进程，**名称** 或者 **进程号**。

```shell
alfons>$ frida-kill --help
Usage: frida-kill [options] process

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -D ID, --device=ID    connect to device with the given ID
  -U, --usb             connect to USB device
  -R, --remote          connect to remote frida-server
  -H HOST, --host=HOST  connect to remote frida-server on HOST

# 杀死usb设备上进程ID为23031的进程
alfons>$ frida-kill -U 23031
```

### 2.5、frida-trace

**frida-trace** 命令可以跟踪目标应用的使用痕迹。

```shell
alfons>$ frida-trace --help
Usage: frida-trace [options] target

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -D ID, --device=ID    connect to device with the given ID
  -U, --usb             connect to USB device
  -R, --remote          connect to remote frida-server
  -H HOST, --host=HOST  connect to remote frida-server on HOST
  -f FILE, --file=FILE  spawn FILE
  -n NAME, --attach-name=NAME
                        attach to NAME
  -p PID, --attach-pid=PID
                        attach to PID
  --debug               enable the Node.js compatible script debugger
  --enable-jit          enable JIT
  -I MODULE, --include-module=MODULE
                        include MODULE
  -X MODULE, --exclude-module=MODULE
                        exclude MODULE
  -i FUNCTION, --include=FUNCTION
                        include FUNCTION
  -x FUNCTION, --exclude=FUNCTION
                        exclude FUNCTION
  -a MODULE!OFFSET, --add=MODULE!OFFSET
                        add MODULE!OFFSET
  -T, --include-imports
                        include program's imports
  -t MODULE, --include-module-imports=MODULE
                        include MODULE imports
  -m OBJC_METHOD, --include-objc-method=OBJC_METHOD
                        include OBJC_METHOD
  -s DEBUG_SYMBOL, --include-debug-symbol=DEBUG_SYMBOL
                        include DEBUG_SYMBOL
```

使用 **frida-trace** 能够Hook设备上应用程序的调用。

```shell
# 显示usb设备上微信的使用痕迹
# -f 参数为启动对应的应用程序，不加此参数时，需要设备上对应的程序处于启动状态。
alfons>$ frida-trace -i dlsym -U -f com.tencent.mm
Spawning `com.tencent.mm`...
Resolving functions...
Instrumenting functions...
dlsym: Auto-generated handler at "C:\Users\xiaohui\Desktop\__handlers__\linker\dlsym.js"
Started tracing 1 function. Press Ctrl+C to stop.
           /* TID 0x437e */
   336 ms  dlsym()
   336 ms  dlsym()
   337 ms  dlsym()
   ···

# 不加-f参数需要手动启动对应的程序，否则会执行失败。
alfons>$ frida-trace -i dlsym -U  com.tencent.mm
Attaching...
Resolving functions...
Instrumenting functions...
dlsym: Loaded handler at "C:\Users\xiaohui\Desktop\__handlers__\linker\dlsym.js"
Started tracing 1 function. Press Ctrl+C to stop.
           /* TID 0x464e */
 12301 ms  dlsym()
 ···
```

使用 **frida-trace** 命令会在指定目录生成对应的Javascript文件，然后Frida将其注入到进程中，并hook特定调用（libc.so中的dlsym函数）。修改生成的Javascript文件dlsym.js可以输出dlsym函数的调用参数。

通过修改 **dlsym.js** 的内容可以查看更多关于进程的信息。

```shell
...
onEnter: function (log, args, state) {
  log("dlsym(" + "pathname=" + Memory.readUtf8String(args[0]) + ", flags=" + Memory.readUtf8String(args[1]) + ")");
  },
...
```

args包含的是对应目标函数的传入参数列表的地址，使用Memory.readUtf8String()函数获取对应的字符串。

再次运行程序输出如下：

```shell
alfons>$ frida-trace -i dlsym -U -f com.tencent.mm
Spawning `com.tencent.mm`...
Resolving functions...
Instrumenting functions...
dlsym: Loaded handler at "C:\Users\xiaohui\Desktop\__handlers__\linker\dlsym.js"
Started tracing 1 function. Press Ctrl+C to stop.
           /* TID 0x3f40 */
   274 ms  dlsym(pathname=javalib.odex, flags=oatdata)
   274 ms  dlsym(pathname=javalib.odex, flags=oatlastword)
   274 ms  dlsym(pathname=javalib.odex, flags=oatxposed)
   275 ms  dlsym(pathname=javalib.odex, flags=oatbss)
   275 ms  dlsym(pathname=javalib.odex, flags=oatbsslastword)
   277 ms  dlsym(pathname=base.odex, flags=oatdata)
   278 ms  dlsym(pathname=base.odex, flags=oatlastword)
   278 ms  dlsym(pathname=base.odex, flags=oatxposed)
   278 ms  dlsym(pathname=base.odex, flags=oatxposedlastword)
   278 ms  dlsym(pathname=base.odex, flags=oatbss)
   279 ms  dlsym(pathname=base.odex, flags=oatbsslastword)
   912 ms  dlsym(pathname=javalib.odex, flags=oatdata)
   912 ms  dlsym(pathname=javalib.odex, flags=oatlastword)
   912 ms  dlsym(pathname=javalib.odex, flags=oatxposed)
   913 ms  dlsym(pathname=javalib.odex, flags=oatbss)
   913 ms  dlsym(pathname=javalib.odex, flags=oatbsslastword)
   915 ms  dlsym(pathname=base.odex, flags=oatdata)
   915 ms  dlsym(pathname=base.odex, flags=oatlastword)
   915 ms  dlsym(pathname=base.odex, flags=oatxposed)
   915 ms  dlsym(pathname=base.odex, flags=oatxposedlastword)
   915 ms  dlsym(pathname=base.odex, flags=oatbss)
   915 ms  dlsym(pathname=base.odex, flags=oatbsslastword)
   958 ms  dlsym(pathname=tinker_classN.dex, flags=oatdata)
   959 ms  dlsym(pathname=tinker_classN.dex, flags=oatlastword)
   959 ms  dlsym(pathname=tinker_classN.dex, flags=oatxposed)
   959 ms  dlsym(pathname=tinker_classN.dex, flags=oatxposedlastword)
   959 ms  dlsym(pathname=tinker_classN.dex, flags=oatbss)
   959 ms  dlsym(pathname=tinker_classN.dex, flags=oatbsslastword)
  1069 ms  dlsym(pathname=libstlport_shared.so, flags=JNI_OnLoad)
  1073 ms  dlsym(pathname=libc++_shared.so, flags=JNI_OnLoad)
  1076 ms  dlsym(pathname=libwechatxlog.so, flags=JNI_OnLoad)
  1136 ms  dlsym(pathname=libc++_shared.so, flags=Java_com_tencent_mars_xlog_Xlog_setConsoleLogOpen)
  1136 ms  dlsym(pathname=libc++_shared.so, flags=Java_com_tencent_mars_xlog_Xlog_setConsoleLogOpen__Z)
  1136 ms  dlsym(pathname=libstlport_shared.so, flags=Java_com_tencent_mars_xlog_Xlog_setConsoleLogOpen)
  1136 ms  dlsym(pathname=libstlport_shared.so, flags=Java_com_tencent_mars_xlog_Xlog_setConsoleLogOpen__Z)
  1137 ms  dlsym(pathname=libwechatxlog.so, flags=Java_com_tencent_mars_xlog_Xlog_setConsoleLogOpen)
  ···
```

## 3、frida-cli

**Frida** 还提供了shell界面，用户可以使用Frida的[Javascrip API](https://www.frida.re/docs/javascript-api/#java)写命令了。不同于hook libc函数，我们可以直接使用Java函数和对象，通过Tab可以查看和补全命令。

```shell
alfons>$ frida --help
Usage: frida [options] target

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -D ID, --device=ID    connect to device with the given ID
  -U, --usb             connect to USB device
  -R, --remote          connect to remote frida-server
  -H HOST, --host=HOST  connect to remote frida-server on HOST
  -f FILE, --file=FILE  spawn FILE
  -n NAME, --attach-name=NAME
                        attach to NAME
  -p PID, --attach-pid=PID
                        attach to PID
  --debug               enable the Node.js compatible script debugger
  --enable-jit          enable JIT
  -l SCRIPT, --load=SCRIPT
                        load SCRIPT
  -c CODESHARE_URI, --codeshare=CODESHARE_URI
                        load CODESHARE_URI
  -e CODE, --eval=CODE  evaluate CODE
  -q                    quiet mode (no prompt) and quit after -l and -e
  --no-pause            automatically start main thread after startup
  -o LOGFILE, --output=LOGFILE
                        output to log file
```

可选参数和 **frida-trace** 类似。

```shell
# 启动微信
alfons>$ frida -U --no-pause -f com.tencent.mm
     ____
    / _  |   Frida 12.0.4 - A world-class dynamic instrumentation toolkit
   | (_| |
    > _  |   Commands:
   /_/ |_|       help      -> Displays the help system
   . . . .       object?   -> Display information about 'object'
   . . . .       exit/quit -> Exit
   . . . .
   . . . .   More info at http://www.frida.re/docs/home/
Spawning `com.tencent.mm`...
Spawned `com.tencent.mm`. Resuming main thread!
[Motorola Nexus 6::com.tencent.mm]->
```

打印目标应用所包含的类名。

```shell
[Motorola Nexus 6::com.tencent.mm]-> Java.perform(function(){Java.enumerateLoadedClasses({"onMatch":function(className){ console.log(className) },"onComplete":function(){}})})
···
com.tencent.common.http.MttRequestBase
com.tencent.smtt.webkit.WebViewChromiumExtension$61
org.chromium.android_webview.ScrollAccessibilityHelper$HandlerCallback
com.tencent.common.threadpool.ComparableFutureTask
com.tencent.tbs.core.webkit.WebView
com.tencent.mtt.game.export.IGamePlayerPrivateResolver
org.chromium.content_public.browser.LoadUrlParams
com.tencent.tbs.common.lbs.LBS
···
```

使用的脚本内容如下：

```javascript
Java.enumerateLoadedClasses(
  {
  "onMatch": function(className){
        console.log(className)
    },
  "onComplete":function(){}
  }
)
```

使用Fridas API的 **Java.enumerateLoadedClasses** 枚举所有加载的类，并使用console.log将匹配的类输出到控制台。

我们还可以使用本地的js文件来执行。

例如mm.js：

```javascript
Java.perform(function () {
    Java.enumerateLoadedClasses(
      {
      "onMatch": function(className){
            console.log(className)
        },
      "onComplete":function(){}
      });
});
```

运行时通过 **-l** 参数加载对应的javascript脚本：

```shell
alfons>$ frida -U --no-pause -l ./mm.js -f com.tencent.mm
```

## 4、Python绑定

通过导入 **frida** 模块，可以使用python编写对应的程序，实现相应的功能。

```python
import frida

# 注入的js代码
jscode = """
"""


# message 的回调函数
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


session = frida.get_usb_device().attach('app full name')  # 附着的usb设备的对应的程序的进程，返回会话
script = session.create_script(jscode)  # 创建执行的脚本
script.on('message', on_message)  # 回调函数
script.load()  # 加载js脚本执行的结果
input("Press enter to continue...")  # 此句必须的，防止进程结束而无法展示结果
```

上面是使用python构造`frida`脚本的模板，主要包含了`Javascript`脚本代码，必要的回调函数。

具体使用见下面代码，打印程序所加载的所有类名。

```python
import frida

jscode = """
console.log("[*] Starting script");
Java.perform(function () {
    Java.enumerateLoadedClasses(
    {
    "onMatch": function(className){
            console.log(className)
        },
    "onComplete":function(){}
    });
});
console.log("[*] Stoping script");
"""


def on_message(message, data):
    try:
        print("[*]message:", message)
        print("[*]data:", data)
    except:
        print("[*]on_message except!")


enumerate_devices = frida.enumerate_devices()  # 获取所有的设备
get_local_device = frida.get_local_device()  # 获取本地设备
get_remote_device = frida.get_remote_device()  # 获取远程设备
device = frida.get_usb_device()  # 获取usb设备

# 启动应用，并返回对应的进程号
# processId = device.spawn("com.tencent.mm")
# session = device.attach(processId)

# 下面两个函数 get_process attach 都需要在设备上启动了程序后，才能获取到进程状态
processInfo = device.get_process("com.tencent.mm")  # 获取微信的进程信息
attachSession = device.attach(processInfo.pid)  # 附着微信的进程，并返回进程的会话

script = attachSession.create_script('console.log("[*] Starting script");')
# script = attachSession.create_script(jscode)    # 创建一个新的js脚本
script.on("message", on_message)    # 设置 message 回调函数

print('[*] Running CTF')

script.load()       # 加载js脚本运行结果

device.kill(processInfo.pid)        # 杀死对应的进程，参数可以是进程名称或者进程号

input("Press enter to continue...")  # 此句必须的，防止进程结束而无法展示结果
```

上面代码会打印目标进程的类名信息。

```shell
[*] Running CTF
[*] Starting script
org.apache.http.HttpEntityEnclosingRequest
org.apache.http.ProtocolVersion
org.apache.http.HttpResponse
org.apache.http.impl.cookie.DateParseException
org.apache.http.HeaderIterator
···
```

注意：**使用Frida的关键还是在于Javascript脚本的编写！！**