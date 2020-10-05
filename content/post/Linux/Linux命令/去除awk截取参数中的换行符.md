---
title: "去除awk截取参数中的换行符"
date: 2019-03-23 20:16:43
lastmod: 2019-03-23 20:16:43
draft: false
keywords: ["Linux", "Linux命令"]
description: "去除awk截取参数中的换行符"
tags: ["Linux", "Linux命令"]
categories: ["Linux", "Linux命令"]
author: "Alfons"
---

事情是这样的：

有一个配置文件，里面有数据库的账号密码，需要读出来，然后对数据库进行初始化。

可是搞了半天，用户名和密码用awk是读出来了，打印出来看着是正常的，但是初始化数据库时总是出错。

最后发现是文件的问题，用010打开，在windows下的文件换行符为 **\r**，awk取出来时，账号名和密码都包含这个特殊的字符，导致初始化未能成功。

<!--more-->

## 实例

配置文件内容如下：

```json
...
username=alfons
password=12345678
...
```

获取用户名和密码的脚本如下：

```shell
username=$(awk -F= '$1=="username" { print $2 } ' mysql.conf)
password=$(awk -F= '$1=="password" { print $2 } ' mysql.conf)
```

获取的内容为：

```shell
username="alfons\r"
password="12345678\r"
```

因为后面的 **\r** 导致了无法初始化数据库的问题！处理方式是使用 **sed命令** 进行替换。

```shell
username=$(awk -F= '$1=="username" { print $2 } ' mysql.conf | sed 's/\r//g' | sed 's/\n//g')
password=$(awk -F= '$1=="password" { print $2 } ' mysql.conf | sed 's/\r//g' | sed 's/\n//g')
```

保险起见，将 **\r** 和 **\n** 一同换了。