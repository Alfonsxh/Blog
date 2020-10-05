---
title: "PCIE"
date: 2019-06-10 22:15:49
lastmod: 2020-12-16 20:41:37
draft: false
keywords: ["Linux", "Linux运维"]
description: "PCIE"
tags: ["Linux", "Linux运维"]
categories: ["Linux", "Linux运维"]
author: "Alfons"
---

**PCIE(Peripheral Component Interconnect Express，快捷外设互联标准)** 仅应用于内部互连，相当于CPU与各硬件设备数据传输的高速公路。

<!--more-->

![PCIE_slot_device](/images/Linux运维/PCIE_slot_device.png)

如上图，为主板上的PCIE扩展槽。

## PCI架构

在PCIE之前，还出现了其他的总线标准，**PCI** 是最著名的一个。

**PCI(Peripheral Component Interconnect)** 在1992年被Intel提出，于2004年被PCIE取代。

一个典型的PCI架构图如下所示：

![PCIE_pci_arch](/images/Linux运维/PCIE_pci_arch.jpg)

有上图可知，PCI的总线主要由三部分组成：

- **PCI设备** - 符合PCI总线标准的设备称之为PCI设备。
- **PCI总线** - PCI总线在系统中可以有多条，可以做树状的扩展，每条PCI总线都可以连接 **多个PCI设备或PCI桥**。
- **PCI桥** - 当一条PCI总线的承载量不够时，可以用新的PCI总线进行扩展。(类似于插线板)

## PCIE架构

**PCI** 采用了并行的传输机制，虽然说，理想状态下，并行可以大幅的提升传输效率，但是在 **高速传输的时候，并行的连线直接干扰异常严重，而且随着频率的提高，干扰（EMI）越来越不可跨越**。

(怎么说呢，就是总线离得特别近，电子同时在相邻的总线上走时，电磁感应产生了相互的干扰)

而 **PCIE** 使用的是 **串行的方式**，通过使用差分信号传输。减少了并行传输带来的信号干扰。

![PCIE_pcie_arch](/images/Linux运维/PCIE_pcie_arch.png)

- **PCI传输**: 33MHz x 4B = 133MB/s
- **PCIe 1.0 x 1**: 2.5GHz x 1b = 250MB/s (PCIe 1.0和2.0采用了8b/10b编码方式，这意味着每个字节（8b）都用10bit传输)

## Linux下PCIE总线设备查看

Linux下通过lspci命令可以查看PCIE总线上的设备相关的信息。

![PCIE_lspci](/images/Linux运维/PCIE_lspci.jpg)

最简单的命令如上所示，**lspci** 会展示出计算机总线上所关联的硬件设备。

前面的一串数字表示的含义是 `[总线ID]:[设备ID].[设备对应的功能ID]`。

总线ID是根据扫描的 **PCI bridge** 所连接的 **另一条PCI总线** 的顺序依次累加的。

如上图，一共有4条 **PCI bridge**。

下图所示的会更清晰一些：

![PCIE_lspci_tv](/images/Linux运维/PCIE_lspci_tv.jpg)

使用 **-t** 命令能够显示出总线的树状结构。

对开头的 `01.0-[01]--+-00.0` 解释为:

- **01.0** - 父节点的设备ID以及功能号，默认总线ID为 **00**。
- **[01]** - 当前总线的ID。
- **00.0** - 连接在 **01** 总线下面的设备ID以及功能号。

(具体的总线ID的设定规则可以参考下面的资料)

可以通过 **-s** 选项查看特定设备的信息。

![PCIE_lspci_s](/images/Linux运维/PCIE_lspci_s.jpg)

可以看见，只有 **01:** 总线下才有设备连接，与 **-t** 选项显示的一样。

> 2020-12-15: 新增下面内容

## PCIE 总线地址命名

PCIE总线地址的命名方式如下：`[domain:][bus]:[device].[func]`

- **domain** - PCIE的域地址，四位或多位十六进制字符表示，通常为 `0000`，如果通过PCIE扩展卡接入，可能会出现不同的域地址
- **bus** - 总线地址，**一个域最多包含256个总线**，通常使用两位十六进制字符表示，表示范围：`00` -> `ff`
- **device** - 设备地址，**一个总线上最多包含32个设备**，通常使用两位十六进制字符表示，表示范围：`00` -> `1f`
- **func** - 设备的功能，**一个设备最多有8种功能**，通常使用一位数字表示，表示范围：`0` -> `7`

## 参考

- [深入PCI与PCIe之一：硬件篇](https://zhuanlan.zhihu.com/p/26172972)
- [必看: 原来PCIe技术原理这么简单！](https://blog.csdn.net/BtB5e6Nsu1g511Eg5XEg/article/details/88386645)
- [Linux Device Drivers, 3rd Edition, Chapter 12. PCI Drivers](https://learning.oreilly.com/library/view/linux-device-drivers/0596005903/ch12.html)