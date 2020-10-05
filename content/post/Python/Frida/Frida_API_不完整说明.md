---
title: "Frida API"
date: 2018-11-29 19:29:58
lastmod: 2018-11-29 19:29:58
draft: false
keywords: ["Python", "Frida"]
description: "Frida API"
tags: ["Python", "Frida"]
categories: ["Python", "Frida"]
author: "Alfons"
---

## Python API

`Frida Python端`调用的`API`主要用于启动程序，并将`JavaScript 脚本`注入到对应进程的内存。

<!--more-->

### 获取设备相关

```shell
>>> frida.enumerate_devices()    # 获取所有的设备列表
[Device(id="local", name="Local System", type='local'), Device(id="tcp", name="Local TCP", type='remote'), Device(id="ZX1G222TZL", name="Motorola Nexus 6", type='usb')]

>>> frida.get_local_device()    # 获取本地设备
Device(id="local", name="Local System", type='local')

>>> frida.get_remote_device()   # 获取远程设备
Device(id="tcp", name="Local TCP", type='remote')

>>> frida.get_usb_device()  # 获取usb设备
Device(id="ZX1G222TZL", name="Motorola Nexus 6", type='usb')

>>> device_manager = frida.get_device_manager()     # 获取设备管理员
>>> device_manager
<_frida.DeviceManager object at 0x0000021DC7BE2E90>

>>> device_manager.enumerate_devices()  # 从设别管理员处获取所有设备的列表
[Device(id="local", name="Local System", type='local'), Device(id="tcp", name="Local TCP", type='remote'), Device(id="ZX1G222TZL", name="Motorola Nexus 6", type='usb')]

>>> device_manager.add_remote_device("127.0.0.1")   # 添加远程设备
Device(id="tcp@127.0.0.1", name="127.0.0.1", type='remote')

>>> device_manager.remove_remote_device("127.0.0.1") # 移除远程设备
>>> device_manager.get_device("ZX1G222TZL")     # 根据deviceId获取设备句柄
Device(id="ZX1G222TZL", name="Motorola Nexus 6", type='usb')
```

### 设备相关

```shell
>>> device = frida.get_usb_device()     # 获取usb设备
>>> device
Device(id="ZX1G222TZL", name="Motorola Nexus 6", type='usb')

>>> device.get_frontmost_application()  # 获取当前正在运行的应用信息
Application(identifier="com.android.chrome", name="Chrome", pid=8310)

>>> device.enumerate_applications() # 获取当前设备所有的应用信息
[Application(identifier="com.github.shadowsocks", name="Shadowsocks"), Application(identifier="com.android.cts.priv.ctsshim", name="com.android.cts.priv.ctsshim"), Application(identifier="com.android.providers.telephony", name="电话和短信存储", pid=1579)...]

>>> device.enumerate_processes()    # 获取当前所有的进程信息
[Process(pid=1, name="init"), Process(pid=229, name="ueventd"), Process(pid=247, name="logd"), Process(pid=255, name="debuggerd"), Process(pid=256, name="vold"), Process(pid=258, name="debuggerd:signaller"), Process(pid=286, name="healthd"), Process(pid=287, name="mdm_helper"), Process(pid=288, name="sensors.qcom"), Process(pid=289, name="qseecomd")...]

>>> device.get_process("com.tencent.mm")   # 获取对应进程的信息
Process(pid=4269, name="com.tencent.mm")

>>> device.spawn("com.tencent.mm")  # 重新启动对应的应用，返回启动后的进程ID（如果设备上进程已经打开，则不用进行此步骤）
9097

>>> device.resume(processId)    # 恢复对应进程的状态，参数可以是进程ID，也可以是进程的名称

>>> attachSession = device.attach(processId)    # 附着对应的进程，返回对应进程的会话。参数可以是进程ID，也可以是进程的名称
>>> attachSession
Session(pid=9922)

>>> device.kill("com.tencent.mm") # 杀死对应的进程。参数可以是进程ID，也可以是进程的名称
```

### 脚本相关

```shell
>>> script = attachSession.create_script(jscode)  # 在附着的进程中创建一个脚本，传入参数为str类型，如果要输入字节码类型，使用create_script_from_bytes接口
>>> script
<_frida.Script object at 0x0000015C20F12DC8>

>>> script.on("message", on_message)    # 创建一个message的回调函数(frida特别指定了message回调)

>>> script.load()  # 加载js脚本，并打印运行结果
```

`Frida`关于python的接口使用大致就上述内容，还有一些接口并未完全展示。

## Frida's JavaScript API

相对于python的接口，`Frida`中更重要的是`JavaScript`的接口。

### console接口

`console`日志模块是`Frida`中使用频率最多的一个模块。`console.log(line)`, `console.warn(line)`, `console.error(line)`三个都是打印日志的接口。

```javascript
//在内存中查找libc.so的起始地址，打印前256字节的内容。
var libc = Module.findBaseAddress("libc.so");
var buf = Memory.readByteArray(libc, 256);
console.log(hexdump(buf, {
    offset: 0,
    length: 256,
    header: true,
    ansi: false
}));
```

### Process接口

`Process`接口主要包含了程序运行的环境，查找模块的地址等等。

```javascript
console.log("\n[*] Process.arch -> " + Process.arch);       // 打印cpu的平台，ia32, x64, arm or arm64
console.log("[*] Process.platform -> " + Process.platform);     // 打印目标操作系统，linux、windows
console.log("[*] Process.pageSize -> " + Process.pageSize);         // 打印虚拟页面大小
console.log("[*] Process.pointerSize -> " + Process.pointerSize);   // 打印指针占用的内存大小
console.log("[*] Process.codeSigningPolicy -> " + Process.codeSigningPolicy);     // 默认值是 optional，除非是在 Gadget 模式下通过配置文件来使用 required，通过这个属性可以确定 Interceptor API 是否有限制，确定代码修改或者执行未签名代码是否安全。
console.log("[*] Process.isDebuggerAttached() -> " + Process.isDebuggerAttached());     // 确定当前是否有调试器附加
console.log("[*] Process.getCurrentThreadId() -> " + Process.getCurrentThreadId());     // 获取当前线程ID

Process.enumerateThreads({                  // 枚举所有线程enumerateThreadsSync为返回所有线程的列表
    onMatch: function (thread) {            // 匹配到执行
        console.log("\n[*] thread.id -> " + thread.id);     // 打印线程id
        console.log("[*] thread.state -> " + thread.state);     // 打印线程状态
        console.log("[*] thread.context -> " + thread.context);     // 打印寄存器
    },
    onComplete: function () {
    }
});

Process.enumerateModules({                  // 枚举所有模块。enumerateModulesSync返回所有模块的列表
    onMatch: function (module) {         // 匹配到执行
        console.log("\n[*] module.name -> " + module.name);     //打印模块名字
        console.log("[*] module.base -> " + module.base);     // 打印模块基地址
        console.log("[*] module.size -> " + module.size);     // 打印模块大小
        console.log("[*] module.path -> " + module.path);     // 打印模块路径
    },
    onComplete: function () {
    }
});

var libc_module = Process.findModuleByName("libc.so");       // 根据模块的名字查找模块，同getModuleByName
libc_module = Process.findModuleByAddress(libc_module.base);        // 根据模块的地址查找模块，同getModuleByAddress
console.log("\n[*] Process.findModuleByName(\"libc.so\"):");
console.log("[*] libc_module.name -> " + libc_module.name);     //打印模块名字
console.log("[*] libc_module.base -> " + libc_module.base);     // 打印模块基地址
console.log("[*] libc_module.size -> " + libc_module.size);     // 打印模块大小
console.log("[*] libc_module.path -> " + libc_module.path);     // 打印模块路径

var cache_block = Process.findRangeByAddress(Process.getModuleByName("libc.so").base);  // 获取目标内存块信息，地址找不到返回null。getRangeByAddress则会抛出异常
console.log("\n[*] cache_block.base -> " + cache_block.base);     // 内存块的基地址
console.log("[*] cache_block.size -> " + cache_block.size);     // 内存块大小
console.log("[*] cache_block.protection -> " + cache_block.protection); // 内存块保护属性，r-x、rwx等
console.log("[*] cache_block.file.path -> " + cache_block.file.path);   // 内存块对应文件路径
console.log("[*] cache_block.file.offset -> " + cache_block.file.offset);   // 内存块对应文件内偏移
console.log("[*] cache_block.file.size -> " + cache_block.file.size);   // 内存块对应文件大小

Process.enumerateRanges("r-x", {        // 枚举指定 protection 类型的内存块。Process.enumerateRangesSync(protection)返回所有匹配到的内存块列表
    onMatch: function (range) {         // 匹配到指定内存块的操作
        console.log("\n[*] range.base -> " + range.base);     // 内存块的基地址
        console.log("[*] range.size -> " + range.size);     // 内存块大小
        console.log("[*] range.protection -> " + range.protection); // 内存块保护属性，r-x、rwx等
        if (range.file) {           // 如果含有file属性的话，打印file属性的内部参数
            console.log("[*] range.file.path -> " + range.file.path);   // 内存块对应文件路径
            console.log("[*] range.file.offset -> " + range.file.offset);   // 内存块对应文件内偏移
            console.log("[*] range.file.size -> " + range.file.size);   // 内存块对应文件大小
        }
    },
    onComplete: function () {
        console.log("[*] onComplete! ");
    }
});
```

### Module接口

`Module`接口主要和各个模块相关。

```javascript
Module.enumerateImports("libwechatnormsg.so", {      // 根据模块的名称，枚举指定模块从其他模块中导入的项。enumerateImportsSync(name)同步版本，返回导入项列表
    onMatch: function (imp) {
        console.log("\n[*] imp.type -> " + imp.type);       // 导入项的类型，function 或者 variable
        console.log("[*] imp.name -> " + imp.name);         // 导入项的名称
        console.log("[*] imp.module -> " + imp.module);     // 与导入项关联的模块的名称
        console.log("[*] imp.address -> " + imp.address);   // 导入项的绝对地址
    },
    onComplete: function () {
        console.log("[*] onComplete! ");
    }
});

Module.enumerateExports("libc.so", {      // 根据模块的名称，枚举指定模块被其他模块使用的导出的项。enumerateExportsSync(name)同步版本，返回导出项列表
    onMatch: function (exp) {
        console.log("\n[*] exp.type -> " + exp.type);       // 导出项的类型
        console.log("[*] exp.name -> " + exp.name);         // 导出项的名称
        console.log("[*] exp.address -> " + exp.address);   // 导出项的绝对地址
    },
    onComplete: function () {
        console.log("[*] onComplete! ");
    }
});

Module.enumerateSymbols("libc.so", {            // 枚举模块中包含的符号。enumerateSymbolsSync(name)为同步版本，返回符号的列表
    onMatch: function (sym) {
        console.log("\n[*] sym.isGlobal -> " + sym.isGlobal);   //bool类型，表示符号是否全局可见
        console.log("[*] sym.type -> " + sym.type);   //符号的类型，包括unknown,section,undefined (Mach-O),absolute (Mach-O),prebound-undefined (Mach-O),indirect (Mach-O),object (ELF),function (ELF),file (ELF),common (ELF),tls (ELF)。
        if (sym.section) {          // 节区信息。不一定含有
            console.log("[*] sym.section.id -> " + sym.section.id);   // 节区名称
            console.log("[*] sym.section.protection -> " + sym.section.protection);   // 节区保护属性，r-x、rwx等
        }
        console.log("[*] sym.name -> " + sym.name);   // 符号名称
        console.log("[*] sym.address -> " + sym.address);   // 符号的绝对地址
    },
    onComplete: function () {
        console.log("[*] onComplete! ");
    }
});
```

### Memory接口

`Memory`接口，主要实现的是对内存的操作，包括内存的读和写。

```javascript
// 在 address 开始的地址，size 大小的内存范围内以 pattern 这个模式进行匹配查找，查找到一个内存块就回调callbacks
Memory.scan(Module.findBaseAddress("libc.so"), 1024, "50 e5 ?? 64", {
    onMatch: function (address, size) {                     // 根据条件匹配到相应的内存块后，回调匹配信息
        console.log("[*] Memory.scan.onMatch.address -> " + address);   // 打印匹配到的地址
        console.log("[*] Memory.scan.onMatch.size -> " + size);     // 打印匹配到的内容长度
    },
    onError: function (reason) {            // 异常处理
        console.log("[*] Memory.scan.onError.reason -> " + reason);     
    },
    onComplete: function () {
        console.log("[*] Memory.scan.onComplete over.");
    }
});

var buf = Memory.alloc(128);       // 在目标进程的堆上分配size字节的空间
console.log("\n[*] Before copy: ");
console.log(hexdump(buf, {          // 打印buf的内容
    offset: 0,
    length: 128,
    header: true,
    ansi: false                 // ansi为windows系统下的字体
}));

Memory.copy(buf, Module.findBaseAddress("libc.so"), 128);         // 从src地址拷贝规定size的内容至dst地址
console.log("\n[*] After Memory.copy -> " );
console.log(hexdump(buf, {
    offset: 0,
    length: 128,
    header: true,
    ansi: false
}));

var buf2 = Memory.dup( Module.findBaseAddress("libc.so"), 64);      // dup结合了alloc和copy的操作，从指定地址开始，复制大小为size的内容，返回复制后的内容
console.log("\n[*] After Memory.dup -> " );
console.log(hexdump(buf2, {
    offset: 0,
    length: 128,
    header: true,
    ansi: false
}));

var cache_block = Process.findRangeByAddress(Process.getModuleByName("libc.so").base);  // 获取原始libc.so模块内存信息
console.log("\n[*] Before Memory.protect:");
console.log("[*] cache_block.base -> " + cache_block.base);     // 原始内存块的基地址
console.log("[*] cache_block.size -> " + cache_block.size);     // 原始内存块的大小
console.log("[*] cache_block.protection -> " + cache_block.protection); // 原始内存块的保护属性为r-x

Memory.protect(cache_block.base, cache_block.size, "rwx");      // 修改内存块的保护属性为rwx
var cache_block2 = Process.findRangeByAddress(Process.getModuleByName("libc.so").base); // 重新读取libc.so模块内存信息
console.log("\n[*] After Memory.protect:");
console.log("[*] cache_block2.base -> " + cache_block2.base);     // 修改后内存块的基地址  不变
console.log("[*] cache_block2.size -> " + cache_block2.size);     // 修改后内存块大小  不变
console.log("[*] cache_block2.protection -> " + cache_block2.protection); // 修改后内存块的保护属性  改变为rwx

var pointerValue = Memory.readPointer(Process.getModuleByName("libc.so").base);     // 读取指定地址处的值
console.log("[*] Before Memory.writePointer-> " + pointerValue);

Memory.writePointer(libc_address, ptr("0x78563412"));       // 在指定内存地址处写入值
pointerValue = Memory.readPointer(Process.getModuleByName("libc.so").base);
console.log("[*] After Memory.writePointer -> " + pointerValue);

Memory.writeByteArray(Process.getModuleByName("libc.so").base, [0xff, 0xff]);           // 在指定地址，写入对应的字节数组
var valueArr = Memory.readByteArray(Process.getModuleByName("libc.so").base, 128);      // 读取指定地址，规定size大小的内容。读取的内容需要通过hexdump接口展示
console.log("[*] Memory.readByteArray -> " + valueArr);
console.log(hexdump(valueArr, {
    offset: 0,
    length: 128,
    header: true,
    ansi: false
}));
```

`Memory`模块还有很多指定类型的读取写入的模块接口，这里不做展示。

### 基础类型

官方说明文档中主要介绍了三种类型，int64、uint64、NativePointer。其中`NativePointer`类型对应于`C`中的指针类型。

```javascript
var int_v = new Int64(64);
console.log("\n[*] new Int64(64) -> " + int_v);       // Int64(v)、UInt64(v) 需要使用关键字new来创建
console.log("[*] int64(64) -> " + int64(64));   // int64(v)、uint64(v) 不需要，可直接创建
console.log("[*] int_v.toString(radix = 16) -> 0x" + int_v.toString(radix = 16));     // 按照对应进制进行转换（貌似只有十进制和十六进制选择）

var nativePointerA = new NativePointer("0x123456");
console.log("\n[*] new NativePointer(\"0x123456\") -> " + nativePointerA);      // 指针类型变量
console.log("[*] ptr(\"0x123456\") -> " + ptr("0x123456"));
console.log("[*] ptr(\"0x123456\") + ptr(\"0x111111\") -> " +  ptr("0x123456").add(0x111111));    // 指针类型变量不能直接相加，需要使用add()接口
console.log("[*] nativePointerA.toInt32() -> " + nativePointerA.toInt32());         // 转换成int类型
console.log("[*] nativePointerA.toString() -> " + nativePointerA.toString(radix=10));       // 按进制转换成对应进制的值
```

### Interceptor接口

`Interceptor`一系列接口中最重要的是`attach(target, callbacks)`接口。通过该接口，可以在进入目标函数前`查看和修改`目标函数的参数。

`Interceptor.attach(target, callbacks)`接口一般用于`Android Native层Hook`。

```javascript
Interceptor.attach(Module.findExportByName("libc.so", "open"), {       // Interceptor拦截器附着(attach)所有函数名为dlopen
    onEnter: function (args) {                              // 拦截函数进入时的操作
        console.log("[*] Interceptor.attach.onEnter!");
        for (var arg in args) {
            console.log("[*] args[" + arg + "] -> " + args[arg])
        }
        console.log('[*] Context information:');
        console.log('[*] Context  : ' + JSON.stringify(this.context));
        console.log('[*] Return   : ' + this.returnAddress);
        console.log('[*] ThreadId : ' + this.threadId);
        console.log('[*] Depth    : ' + this.depth);
        console.log('[*] Errornr  : ' + this.err);
    },
    onLeave: function (retval) {                            // 函数返回后的操作
        console.log("[*] Interceptor.attach.onLeave!");
        for (var r in retval) {
            console.log("[*] retval[" + r + "] -> " + retval[r])
        }
    }
});
```

### Java接口

`Frida`通过`jni`打通了`Java`和`JavaScript`的通道。在`Frida`中的`Java接口`都由`JavaScript`实现。

这里需要特别注意的一点是，在`Frida`中调用`Java`，需要将实现功能的函数都放置在`Java.perform()`内。

```JavaScript
console.log("\n[*] Java.available -> " + Java.available);
Java.perform(function () {                  // 执行任意 Java 操作都需要使⽤此函数
    Java.enumerateLoadedClasses({                // 枚举加载的类。enumerateLoadedClassesSync() 为同步版本，返回值为类名的列表。
        onMatch: function (className) {          // 匹配到时，参数为类名
            console.log("\n[*] className -> " + className);
        },
        onComplete: function () {
            console.log("[*] Java.enumerateLoadedClasses.onComplete -> ");
        }
    });

   var logClass = Java.use("com.tencent.mm.sdk.platformtools.x");  // 获取指定类名的JavaScript引用
    logClass.i.overload("java.lang.String", "java.lang.String").implementation = function (arg1, arg2) {    // 源代码中含有重载的函数接口，这里要指定。
        if ("MicroMsg.LauncherUI" === arg1) {
            console.log("\n[*] logClass.i.overload(\"java.lang.String\", \"java.lang.String\")");
            console.log("[*] Original arg1 -> " + arg1);
            console.log("[*] Original arg2 -> " + arg2);
        }
        this.i(arg1, arg2);     // 如果不运行源函数功能，则源函数也不会运行
    };

    var strClass = Java.use("java.lang.String");
    logClass.i.overload("java.lang.String", "java.lang.String", '[Ljava.lang.Object;').implementation = function (arg1, arg2, arg3) {
        if ("MicroMsg.LauncherUI" === arg1) {
            // 使用JavaScript引用类的功能，包括：
            // $new：new 运算符，初始化新对象。注意与 $init 区分
            // $alloc：分配内存，但不不初始化
            // $init：构造器器⽅方法，⽤用来 hook ⽽而不不是给 js 调⽤用
            // $dispose：析构函数
            // $isSameObject：是否与另⼀一个 Java 对象相同
            // $className：类名
            console.log("\n[*] strClass.$className -> " + strClass.$className);
            console.log("[*] strClass.$new(\"Hello World!) -> " + strClass.$new("Hello World!"));
        }
        return this.i(arg1, arg2, arg3);
    };

    var bool_a = Java.use("java.lang.Boolean").$new(true);      // 与Java相关的接口，必须在Java.perform(function(){...}) 规定的函数外层使用，内层不能使用。
    Java.scheduleOnMainThread(function () {
        // var bool_a = Java.use("java.lang.Boolean").$new(true);       // 错误的做法
        console.log("[*] Java.use(\"java.lang.Boolean\").$new(true) -> " + bool_a);
    });

    Java.choose("com.tencent.mm.ui.LauncherUI", {     // 在Java的内存堆上扫描指定类名称的Java对象，每次扫描到一个对象，则回调callbacks
        onMatch: function (instance) {              // 参数为目标的单例
            for (var i in instance) {
                console.log("[*] instance[" + i + "] -> " + instance[i]);
            }
        },
        onComplete: function () {
            console.log("[*] Java.choose().onComplete!")
        }
    });

    Java.cast(ptr("0x1234"), Java.use("java.lang.String"));     // 将指定地址的内容强转为目标类型(使用Java.use()后的对象)
});
```

## 参考资料

- [Frida JavaScript API](https://www.frida.re/docs/javascript-api/)
- [基于 FRIDA 的全平台逆向分析](https://www.slideshare.net/ssusercf6665/frida-107244825)