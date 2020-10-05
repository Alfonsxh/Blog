---
title: "RAID"
date: 2019-06-10 22:15:49
lastmod: 2019-06-12 10:19:12
draft: false
keywords: ["Linux", "Linux运维"]
description: "RAID"
tags: ["Linux", "Linux运维"]
categories: ["Linux", "Linux运维"]
author: "Alfons"
---

**独立硬盘冗余阵列(RAID, Redundant Array of Independent Disks)**，利用虚拟化技术将多个磁盘组合起来，成为一个多个硬盘的阵列，从而提升效率或者资料冗余。

根据RAID的层级不同，资料会以多种形式放置在多个磁盘上。

<!--more-->

## RAID层级

RAID的层级，常用的包括：RAID0、RAID1、RAID5、RAID10。

### RAID 0 (stripe)

![RAID_raid0](/images/Linux运维/RAID_raid0.png)

**raid 0** 的方式是将原始数据按块分别存储在不同的磁盘上。这种方式目前不推荐使用，**因为一旦某一块磁盘损坏，将会使得该块磁盘保存的数据丢失。**

### RAID 1 (mirror)

![RAID_raid1](/images/Linux运维/RAID_raid1.png)

**raid 1** 的方式比 **raid 0** 要好一些，**将原始数据拷贝成多份，存储在不同的磁盘上**。这样做的好处在于，当一块磁盘损坏了，另一块磁盘仍可以提供数据。

**raid 1** 也有缺点，数据重复，磁盘利用率低。

### RAID 5 (奇偶校验)

![RAID_raid5](/images/Linux运维/RAID_raid5.png)

**raid 5** 的方式:

- 将原始数据分成多份，分别存储在不同的磁盘上。
- 必须要有三块或以上的物理磁盘。
- 存储的数据量为 **(n-1)/n \* 磁盘总量**。
- 假如有四块盘，前三块存储了A、B、C三份数据，第四块的内容则使用奇偶校验的方式进行计算得到。
- 不做热备份的情况下，允许损坏一块磁盘，损坏的一块的内容可以通过其他三块盘计算得到。
- 热备盘的作用是，当其中的一块磁盘损坏时，能够通过奇偶校验的方式，将数据还原到热备盘上，用热备盘替换损坏的磁盘工作。
- 损坏两块磁盘就不能恢复数据了。
- **每块盘都可以存储奇偶校验的内容。**

### RAID 10

![RAID_raid10](/images/Linux运维/RAID_raid10.png)

**raid 10** 的架构如上图，底层通过 **raid 1** 将数据进行镜像备份，上一层通过 **raid 0** 将原始数据分别分发给不同的raid。

这么做能够有效的防止坏盘导致数据的丢失问题。

**PS: raid可以通过不同的组合方式组成新的磁盘阵列**。

## RAID信息查看

不同的产商提供的工具有所不同，大环境下，使用的比较多的是 **storcli64** 工具。

下面主要介绍如何查看raid相关的信息。

`storcli64 show` 可以查看raid的信息，可以分成几个等级：

- **/cx** - Controller specific commands
- **/ex** - Enclosure specific commands
- **/sx** - Slot/PD specific commands
- **/vx** - Virtual drive specific commands
- **/dx** - Disk group specific commands
- **/fx** - Foreign configuration specific commands
- **/px** - Phy specific commands
- **/bbu** - Battery Backup Unit related commands

可以通过 `storcli64 show` 查看raid的基本信息，主要是控制器相关。

```bash
System Overview :
===============

---------------------------------------------------------------
Ctl Model   Ports PDs DGs DNOpt VDs VNOpt BBU sPR DS  EHS ASOs 
---------------------------------------------------------------
  0 9271-8i     8  12   2     0   2     0 Opt On  1&2 Y      3 
---------------------------------------------------------------
```

上面的内容是输出的结果，可以看到该设备只有一个控制器，物理磁盘作为raid的有12块，raid的数量有2个。

通过 `storcli64 /c0 show` 查看对应的控制器的信息，如果有两块，第二块通过 `/c1` 的方式，以此类推。

```bash
TOPOLOGY :
========

--------------------------------------------------------------------------
DG Arr Row EID:Slot DID Type  State BT       Size PDC  PI SED DS3  FSpace 
--------------------------------------------------------------------------
 0 -   -   -        -   RAID5 Optl  N    2.181 TB enbl N  N   dflt N      
 0 0   -   -        -   RAID5 Optl  N    2.181 TB enbl N  N   dflt N      
 0 0   0   8:0      9   DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 0 0   1   8:1      12  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 0 0   2   8:2      17  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 0 0   3   8:3      11  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 -   -   -        -   RAID5 Optl  N    5.089 TB enbl N  N   dflt N      
 1 0   -   -        -   RAID5 Optl  N    5.089 TB enbl N  N   dflt N      
 1 0   0   8:4      16  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   1   8:5      19  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   2   8:6      10  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   3   8:7      14  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   4   8:8      13  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   5   8:9      18  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   6   8:10     20  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
 1 0   7   8:11     15  DRIVE Onln  N  744.687 GB enbl N  N   dflt -      
--------------------------------------------------------------------------
```

结果会显示出控制器 `/c0` 下的详细信息，包括 **TOPOLOGY(拓扑结构)**、**VD LIST**、**PD LIST**、**BBU_Info** 等。

如果觉得结果很难处理的话，可以通过在命令的末尾添加 **j** 来输出json格式的结果。如 `storcli64 /c0 show j`。

```bash
{
"Controllers":[
{
	"Command Status" : {
		"Controller" : 0,
		"Status" : "Success",
		"Description" : "None"
	},
	"Response Data" : {
        ...
    }
}]
}
```

通过组合不同等级的设备可以单独查看各设备的信息。例如 `/c0/v0` 即为查看 **0号控制器下0号raid的信息**。命令为 `storcli64 /c0/v0 show`。

如果项查看所有的信息，可以通过 **all** 来替换索引来实现。如 `storcli64 /c0/vall show` 为查看 **0号控制器下所有raid的信息**。

## 参考

- [Advantages and disadvantages of various RAID levels](https://datapacket.com/blog/advantages-disadvantages-various-raid-levels/)
- [What is RAID 0, 1, 5, & 10?](https://www.youtube.com/watch?v=U-OCdTeZLac)
- [RAID 磁盘阵列配置和调优小结](https://wsgzao.github.io/post/raid/)
- [storcli 简易使用介绍](https://www.cnblogs.com/luxiaodai/p/9878747.html)