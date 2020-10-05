---
title: "CMake使用(一)-格式规范"
date: 2018-11-10 23:27:53
lastmod: 2018-11-10 23:27:53
draft: false
keywords: ["C++", "CMake"]
description: "CMake使用(一)-格式规范"
tags: ["C++", "CMake"]
categories: ["C++", "CMake"]
author: "Alfons"
---

一个cmake文件至少包含以下内容

```javascript
cmake_minimum_required (VERSION 3.0)    # 所需的cmake最低版本

project (Tutorial)  # 工程名

add_executable(Tutorial tutorial.cxx)   # 可执行程序的名称，以及项目可执行程序的编译文件
```

<!--more-->

在开头部分，我们可以添加一些编译的选项。

```javascript
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
add_compile_options(-std=c++11)
```

可以通过`set`函数来设置，也可以通过`add_compile_options`来设置。值的注意的是，`add_compile_options`是针对所有编译器而言，`CMAKE_CXX_FLAGS`只针对`CXX`编译器。

其他的，头文件包含、子编译项目以及源文件包含有必要的化也可以添加。

总体的cmake文件如下：

```javascript
cmake_minimum_required(VERSION 3.0)

project(AlgorithmsTest)

# 设置编译选项选项
# 值得注意的是add_compile_options命令添加的编译选项是针对所有编译器的(包括c和c++编译器)，
# 而set命令设置CMAKE_C_FLAGS或CMAKE_CXX_FLAGS变量则是分别只针对c和c++编译器的

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
add_compile_options(-std=c++11)

# 添加头文件目录
include_directories(ElementNotRepeat)

# 添加子文件夹，会包含子文件夹目录下的CMakeLists.txt文件
add_subdirectory(ElementNotRepeat)

# 添加源文件
aux_source_directory(. MainSrcs)

# 添加可执行程序
add_executable(Test ${MainSrcs})

# 添加动态库依赖
target_link_libraries(Test NotRepeat)
```

子目录`ElementNotRepeat`下的CMakeLists.txt文件内容如下：

```javascript
aux_source_directory(. DIR_SRCS)

add_library(NotRepeat ${DIR_SRCS})
```