---
title: "2_Scrapy模块使用及调试"
date: 2019-01-14 16:25:42
lastmod: 2019-01-14 16:25:42
draft: false
keywords: ["Python", "Scrapy", "爬虫"]
description: "2_Scrapy模块使用及调试"
tags: ["Python", "Scrapy", "爬虫"]
categories: ["Python", "Scrapy", "爬虫"]
author: "Alfons"
---

## 安装

```shell
pip install scrapy
```

<!--more-->

## 创建一个新工程

```shell
scrapy startproject <project_name>
```

其中 **project_name** 为项目名称，默认会在当前目录下创建一个名为 **project_name** 的文件夹用于目标 **Spider任务**。

具体命令如下：

```shell
$ scrapy startproject -h
Usage
=====
  scrapy startproject <project_name> [project_dir]

Create new project

Options
=======
--help, -h              show this help message and exit

Global Options
--------------
--logfile=FILE          log file. if omitted stderr will be used
--loglevel=LEVEL, -L LEVEL
                        log level (default: DEBUG)
--nolog                 disable logging completely
--profile=FILE          write python cProfile stats to FILE
--pidfile=FILE          write process ID to FILE
--set=NAME=VALUE, -s NAME=VALUE
                        set/override setting (may be repeated)
--pdb                   enable pdb on failure
```

初始时的目录结构如下所示：

![project_framework_begin](/images/Python/Scrapy/scrapy_project_framework_begin.png)

## 启动调试

使用 **IDE** 时，为了方便调试，可以新建 **run.py** 使用 **spider.cmdline** 中的 **execute函数** 执行命令，达到调试的效果。

```python
# run.py
from scrapy.cmdline import execute

if __name__ == '__main__':
    spider_app = 'DoubanMovie'
    cmd = 'scrapy crawl {0} --nolog'.format(spider_app)

    execute(cmd.split())
```