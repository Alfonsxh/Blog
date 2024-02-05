---
title: "node_exporter"
date: 2024-02-05T17:32:58+08:00
lastmod: 2024-02-05T17:32:58+08:00
draft: false
keywords: ["Prometheus", "Exporter", "node_exporter"]
description: ""
tags: ["Prometheus", "Exporter", "node_exporter"]                      # 归档 
categories: ["Prometheus", "Exporter", "node_exporter"]                # 分类
author: "Alfons"

comment: true                 # 是否显示评论
# toc: true                     # 是否展示目录
# autoCollapseToc: false        # 是否展示下拉式目录
# postMetaInFooter: true        # 是否在页脚显示文章源信息
# hiddenFromHomePage: false     # 是否在首页隐藏

# 文章license
# contentCopyright: '<a href= "https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en"> Creative Commons BY-NC-ND 3.0 </a>'

# reward: false                 # 是否展示支付二维码

# 数学公式
# mathjax: false
# mathjaxEnableSingleDollar: false
# mathjaxEnableAutoNumber: false

# 隐藏页眉和页脚
# hideHeaderAndFooter: false

# enableOutdatedInfoWarning: false

# 流程图
# flowchartDiagrams:
#   enable: true
#   options: ""

# 序列图
# sequenceDiagrams: 
#   enable: true
#   options: ""

---

node_exporter 是 Prometheus 官方提供的一个用于采集计算机硬件信息的 Exporter。几乎所有的指标都来源于文件系统：`/proc`、`/sys`。这么做的好处显而易见，指标采集的效率非常的高。

<!--more-->

## 项目结构

node_exporter 

## 参考

- [procfs](https://pkg.go.dev/github.com/prometheus/procfs)
