---
title: "CMake使用(二)-预编译选项添加"
date: 2018-11-10 23:27:53
lastmod: 2018-11-10 23:27:53
draft: false
keywords: ["C++", "CMake"]
description: "CMake使用(二)-预编译选项添加"
tags: ["C++", "CMake"]
categories: ["C++", "CMake"]
author: "Alfons"
---

分两种情况，一种是添加宏定义选项，一种是添加编译选项。

<!--more-->

## 添加宏定义选项

例如，在main函数中打印项目的版本号。

```C++
#include <iostream>

#include "config.h"

int main() {
    fprintf(stdout, "Version -> %d.%d\n", PROJECT_VERSION_MAJOR, PROJECT_VERSION_MINOR);

    return 1;
}
```

**PROJECT_VERSION_MAJOR** 和 **PROJECT_VERSION_MINOR** 参数需在 **config.h.in** 头文件中设置对应的值。

```C++
#define PROJECT_VERSION_MAJOR @VERSION_MAJOR@
#define PROJECT_VERSION_MINOR @VERSION_MINOR@
```

在CMakelists.txt文件中对相应的参数进行赋值。

```js
# 设置编译选项
set(VERSION_MAJOR 1)        # 设置选项需放定义文件的前面
set(VERSION_MINOR 0)

configure_file(     # 配置文件
        "${PROJECT_SOURCE_DIR}/include/config.h.in"
        "${PROJECT_SOURCE_DIR}/include/config.h"
        )
```

当编译时，会在 **config.h** 头文件中添加对应的 **#define** 宏定义参数。

```C++
#define PROJECT_VERSION_MAJOR 1
#define PROJECT_VERSION_MINOR 0
```

因此程序的输出为：

```shell
Version -> 1.0
```

## 添加编译选项

例如，按要求运行对应的程序

```C++
#include <iostream>

#include "config.h"
#include "DeleteRepeatElem.h"

int main() {
    fprintf(stdout, "Version -> %d.%d\n", PROJECT_VERSION_MAJOR, PROJECT_VERSION_MINOR);

#ifdef USE_NO_REPEAT_LIB
    DelRepeatElems();
#endif

    std::cout << "helloworld" << std::endl;
    return 1;
}
```

主函数中有个编译选项 **USE_NO_REPEAT_LIB**，是否使用该动态库。

要实现该功能，需要在CMakelists.txt中添加option选项，并使用 **add_definitions** 添加对应的定义。

```js
option(USE_NO_REPEAT_LIB "help: Use norepeat library." ON)        # 设置编译选项，通过判断是否设置该选项，添加对应的预编译内容。改变编译选项后，要清理后编译
if (USE_NO_REPEAT_LIB)
    add_definitions(-DUSE_NO_REPEAT_LIB)
endif ()
```

值得注意的是，当改变了option设置的值时，一定要先清空之前构建的内容，使用 **rebuild**，而不是使用 **build**！！！

最终的结果如下：

```shell
$ ./Test
Version -> 1.0
1 number is 1
2 number is 3
3 number is 1
4 number is 1
5 number is 2
6 number is 2
7 number is 1
34 number is 1
43 number is 1
342 number is 1
432 number is 1
helloworld
```