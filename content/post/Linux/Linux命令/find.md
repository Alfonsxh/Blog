---
title: "Linux命令find"
date: 2019-03-23 20:16:43
lastmod: 2019-03-23 20:16:43
draft: false
keywords: ["Linux", "Linux命令"]
description: "Linux命令find"
tags: ["Linux", "Linux命令"]
categories: ["Linux", "Linux命令"]
author: "Alfons"
---

通过 **find命令**，可以很方便的查找符合目标类型的文件，例如多长时间内修改过的文件，大小范围内的文件等，配合一些其他的操作，例如删除操作。

**find命令** 基本语法： `find [path] [option] [expression]`。

<!--more-->

## 例子

### 基本操作

列出当前目录及其子目录的文件：

```shell
# 直接使用find即可
$ find
.
./去除awk截取参数中的换行符.md
./Linux命令find.md
./README.md
./Linux命令awk.md
./Linux命令sed.md
```

找出特定格式的文件：

```shell
$ find ../Image/ -name "*.jpg"
../Image/Python/同步与异步/DiffBetweenThreadAndCoro.jpg
../Image/Python/GIL全局解释器锁/GIL_with_diff_CPU.jpg
../Image/Python/hashcat使用说明/increment_set_8_9.jpg
../Image/Python/hashcat使用说明/increment_not_set.jpg
...

# 在目录深度的最大范围为2的目录中查找指定格式的文件，只有三个
$ find ../Image/ -maxdepth 2 -name "*.jpg" 
../Image/Docker/get_master_nil.jpg
../Image/Docker/diff_between_run_create.jpg
../Image/Docker/get_master_success.jpg
```

### 查找时间范围内的文件

时间范围选项：

- **atime/天，amin/分钟**: a表示 **accessed**，按照用户最近一次访问(存取过)时间来过滤。
- **ctime/天，cmin/分钟**: c表示 **change**，按照文件数据元(例如权限等)最近一次修改时间来过滤。
- **mtime/天，mmin/分钟**: m表示 **modified**，按照用户最近一次修改时间来过滤。
- **newer file**: 查找比 **file** 修改时间更长的文件。(newer 表示file更新一点)
- **anewer file**: 查找比 **file** 存取时间更长的文件。
- **cnewer file**: 查找比 **file** 修改时间更长的文件。

对于前六个参数的时间范围:

- **-atime -7** 表示在七天内修改过。
- **-atime 7** 表示正好在七天前修改过。
- **-atime +7** 表示修改时间超过七天。

例子：

```shell
# 找出特定时间范围内的文件
$ find ../Image/ -name "*.jpg" -ctime -30 | xargs ls -l
-rw一点-rw-r-- 1 alfons alfons  79076 3月   9 21:57 ../Image/Docker/dif一点f_between_run_create.jpg
-rw一点-rw-r-- 1 alfons alfons 154655 3月   9 21:57 ../Image/Docker/get一点_master_nil.jpg
-rw-rw-r-- 1 alfons alfons 156051 3月   9 21:57 ../Image/Docker/get_master_success.jpg
-rw-r--r-- 1 alfons alfons 211543 2月  20 22:25 ../Image/Python/DoubanMovie爬虫/1_new_search_subjects.jpg
-rw-rw-r-- 1 alfons alfons   5366 1月  14 10:49 ../Image/Python/DoubanMovie爬虫/5_captcha.jpg

# 找到比READM.md更老的文件
$ ls -l README.md 
-rw-rw-r-- 1 alfons alfons 9 7月  18  2018 README.md

$ find ../Image/ -name "*.jpg" -newer README.md | xargs ls -l
-rw-rw-r-- 1 alfons alfons  84299 9月  28 22:33 ../Image/Books/OtherBooks/见识.jpg
-rw-rw-r-- 1 alfons alfons  26541 11月  4 21:26 ../Image/Books/OtherBooks/今日简史.jpg
....
```

### 根据文件类型查找

基本命令格式： `find . -type [类型参数]`。

类型参数：

- **f**: 普通文件。
- **l**: 链接符号。
- **d**: 目录。
- **c**: 字符设备。
- **b**: 块设备
- **s**: sock套接字。
- **p**: FIFO。

例如：

```shell
# 查找本地文件夹内七天前修改过的普通文件
$ find . -type f -ctime +7 | xargs ls -l
-rw-rw-r-- 1 alfons alfons 9 7月  18  2018 ./README.md

# 查找修改日期超过七天的文件夹
$ find .. -maxdepth 1 -type d -ctime +7 | xargs ls -l -d
drwxr-xr-x   3 alfons alfons 4096 12月 17 21:06 ../Algorithms
drwxr-xr-x   4 alfons alfons 4096 7月  18  2018 ../Books
drwxrwxr-x   3 alfons alfons 4096 11月 10 17:05 ../C++
drwxr-xr-x   2 alfons alfons 4096 7月   7  2018 ../LeetCode
drwxrwxr-x 149 alfons alfons 4096 7月  31  2018 ../node_modules
drwxr-xr-x   6 alfons alfons 4096 1月  30 13:26 ../Python
drwxrwxr-x   2 alfons alfons 4096 7月   7  2018 ../.vscode
drwxrwxr-x   2 alfons alfons 4096 1月  30 13:43 ../陈皓专栏笔记
drwxrwxr-x   2 alfons alfons 4096 2月  17 21:28 ../随笔
drwxrwxr-x   2 alfons alfons 4096 12月 16 21:52 ../《左耳听风每周练习》
```

### 根据文件大小查找

按文件大小查找需要用到 `-size n` 选项，后面跟单位选项：

- **b**: 块（512字节）
- **c**: 字节
- **w**: 字（2字节）
- **k**: 千字节
- **M**: 兆字节
- **G**: 吉字节

**n** 的大小和上面时间的使用一样， **+** 表示超过n大小的文件， **-** 表示小于n大小的文件。

找到大小大于 **10KB** 的md文件:

```shell
$ find . -type f -name "*.md" -size +10k | xargs ls -l -h
-rw-rw-r-- 1 alfons alfons 17K 12月  2 20:08 ./Algorithms/AlgorithmsArea/红黑树.md
-rw-rw-r-- 1 alfons alfons 14K 11月  6 23:24 ./Books/OtherBooks/见识.md
-rwx------ 1 alfons alfons 28K 10月 17 15:15 ./Books/ProfessionBooks/MySQL必知必会/2_MySQL基本操作.md
-rwx------ 1 alfons alfons 13K 10月 18 17:39 ./Books/ProfessionBooks/MySQL必知必会/3_MySQL高级操作_聚集和分组.md
-rwx------ 1 alfons alfons 14K 10月 23 20:13 ./Books/ProfessionBooks/MySQL必知必会/4_MySQL高级操作_联结查询.md
...
```

### 找到文件后的操作

大部分时候，我们查找到文件后，需要对文件进行一些操作。需要用到 `-exec` 或者 `-ok` 选项，后面跟的都是 **shell命令**。

命令格式：`find . -type f -exec rm {} \;`。

`-exec` 和 `-ok` 的不同之处在于，`-exec` 会直接执行后续的操作。而 `-ok` 选项需要用户确认是否执行后续的选项。

后面的 **{}** 表示的是待处理的已经找到的目标文件。

`-exec` 必须由一个 **;** 结束，之所以使用 `\;`，是转义的意思，shell脚本通常会对 **;** 进行处理。

找到目标文件并删除：

```shell
# 使用 -exec 选项不会出现确认选项
$ find . -type f -size -8c -exec rm {} \;

# 而使用 -ok 选项则会出现用户确认
$ find . -type f -size -8c -ok rm {} \;
< rm ... ./wait_del.txt > ? y
```

比较推荐的是 **使用管道的方式** 来对找到的目标文件进行处理。

```shell
# 有些命令不支持管道操作，需要使用xargs命令做下中转
$ find . -type f -size -10c | xargs ls -l
-rw-rw-r-- 1 alfons alfons 9 7月  18  2018 ./README.md
```

## 参考

- [find命令](http://man.linuxde.net/find)
- [Linux命令之find exec rm](https://blog.csdn.net/u011334621/article/details/38063143)