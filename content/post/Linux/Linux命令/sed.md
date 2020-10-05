---
title: "sed"
date: 2019-03-23 20:16:43
lastmod: 2019-03-23 20:16:43
draft: false
keywords: ["Linux", "Linux命令"]
description: "sed"
tags: ["Linux", "Linux命令"]
categories: ["Linux", "Linux命令"]
author: "Alfons"
---

**sed** 是一种流编辑器，用于处理文本数据。文本数据是以 **行为单位** 进行处理。可以是文件流，也可以是 **STDIN** 管道传入的数据。

命令格式为： `sed [参数] [动作]`。

<!--more-->

参数：

- **-n**: 使用silent模式，一般情况下，**sed** 默认将输出所有的数据在屏幕上，使用 **-n** 参数后，只有被处理的行才会列出来，通常和 **-p** 一起使用。
- **-e**: 允许在一行中执行多条命令，各命令互不干扰。
- **-f**: 将sed的动作写在文件中，执行文件中的sed命令对文本数据进行处理
- **-r**: 使用扩展型正则表达式语法(默认为基础正则表达式)。
- **-i**: 直接修改文件内容，而不是由屏幕输出。

动作： `[n1, n2]动作`

- n1, n2 表示的是行索引，不一定需要，存在时为 **左闭右闭**。例如 `10，20动作` 表示的是 **对从第十行到第二十行(包括第十行到第二十行)的数据** 进行操作。
- **a**: 新增，`n1,n2a str` 在第n1行到n2行后面都新增一行，内容为str。
- **c**: 替换，`n1,n2c str` 将第n1行到n2行的内容替换为str，是整个替换，不是一行一行替换！
- **d**: 删除，`n1,n2d` 将第n1行到n2行都删除。
- **i**: 插入，`n1,n2i str` 在第n1行到n2行前面都新增一行，内容为str。
- **p**: 打印，`n1,n2p` 将第n1行到n2行的内容打印出来，通常和 **-n** 参数一起使用。
- **s**: 替换，`n1,n2s/old/new/g` 通常和 **g** 动作一起使用，将第n1行到n2行中的目标old替换成new。可以使用正则表达式进行匹配。
- **g**: 行内全替换，**s动作** 不加 **g** 只会替换每行初次匹配到的目标，加了会替换行内的所有目标。

## 例子

```shell
$ cat pets.txt
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
```

### 替换操作s

替换 **my** ---> **alonfs**:

```shell
sed 's/my/alfons/g' test.txt
```

替换单引号为双引号：

```shell
# 单引号中的语句无法转义双引号，只能在双引号中转义单引号。
sed "s/'/\"/g" test.txt
```

在每行行首添加 ‘#’：

```shell
# ^在正则表达式中表示的是开头的意思
sed 's/^/#/g' test.txt

# 同样在末尾加上标点，使用 $ 标识
sed 's/$/./g' test.txt
```

替换每一行的第一个 **s** 为 **\***:

```shell
# 语句后面的1表示的是第几个
sed 's/s/*/1' test.txt

# 替换第二个s使用2代替
sed 's/s/*/2' test.txt
```

替换一二行的 **my** ----> **your**，替换三四行的 **This** ----> **That**：

```shell
# 下面的命令和 sed -e '1,2s/my/your/g' -e '3,4s/This/That/g' test.txt 效果一样
sed '1,2s/my/your/g; 3,4s/This/That/g' test.txt
This is your cat, your cat's name is betty
This is your dog, your dog's name is frank
That is my fish, my fish's name is george
That is my goat, my goat's name is adam
```

将 **my** 用 **『』** 括起来:

```shell
# 使用 & 来标记前面匹配的内容
sed 's/my/『&』/g' test.txt
```

简略的表示内容，如第一行 **cat:betty**：

```shell
# 使用 () 表示的是正则表达式匹配的结果，在使用时，使用 \1 \2 表示结果
$ sed 's/This is my \([^,]*\), .*is \([.*]*\)/\1:\2/g' test.txt
cat:betty
dog:frank
fish:george
goat:adam
```

### a命令(append)和i命令(insert)

**a命令** 表示的是在 **目标行的后面** 添加一行，而 **i命令** 则是在 **目标行的前面** 插入一行。

```shell
# 1i 表示在第一行前面插入一行
$ sed '1i This is first line.' test.txt 
This is first line.
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my fish, my fish's name is george
This is my goat, my goat's name is adam

# $表示在最后一行后面添加一行
$ sed '$a This is last line.' test.txt 
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
This is last line.
```

### c命令

**c命令** 也是替换的意思，和 **s命令** 不同的是，**c命令** 是将 **一至多行替换，并不会根据内容替换**。

```shell
# 将2 至 3 行的内容替换成 ...
$ sed '2,3c ...' test.txt 
This is my cat, my cat's name is betty
...
This is my goat, my goat's name is adam
```

### d命令

**d命令** 是删除命令，删除指定的行。

删除含有 **dog** 的行：

```shell
# /dog/ 表示的是匹配到含有dog的那一行，和使用行索引是一样的，只不过用 // 来找了一遍。
sed '/dog/d' test.txt
This is my cat, my cat's name is betty
This is my fish, my fish's name is george
This is my goat, my goat's name is adam
```

## 进阶

注释 **dog** 行，及其后三行：

```shell
$ sed '/dog/,+3s/^/# /' test.txt 
This is my cat, my cat's name is betty
# This is my dog, my dog's name is frank
# This is my fish, my fish's name is george
# This is my goat, my goat's name is adam
```

命令打包：

```shell
# 使用{}将要执行的命令括起来，可以在同一行执行多条命令
# 在第二行及其后面的行中，找到包含 This 的行
# 其中包含 fish 的行的第二个 my 用 {} 括起来
$ sed '2,${/This/{/fish/s/my/{&}/2}}' test.txt 
This is my cat, my cat's name is betty
This is my dog, my dog's name is frank
This is my fish, {my} fish's name is george
This is my goat, my goat's name is adam
```

## 参考

- [SED 简明教程](https://coolshell.cn/articles/9104.html)
- [sed命令](http://man.linuxde.net/sed)