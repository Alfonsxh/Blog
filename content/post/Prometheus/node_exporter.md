---
title: "node_exporter"
date: 2024-02-05T17:32:58+08:00
lastmod: 2024-02-05T17:32:58+08:00
draft: true
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

node_exporter 的入口为 node_exporter.go 文件，同级目录下的 collector 目录包含了所有的采集指标。

```shell
# tree -L 2
├── collector
│   ├── arp_linux.go
│   ├── bcache_linux.go
│   ├── bonding_linux.go
│   ├── bonding_linux_test.go
│   ├── boot_time_bsd.go
...
├── node_exporter.go
...
```

node_exporter 也是按照 [Exporter简单入门](./Exporter简单入门.md) 中提到的三个步骤，进行编写。

- 「1」创建采集项 Collector
- 「2」注册采集项对象
- 「3」绑定HttpHandler，并启动web服务

只不过为了管理众多的采集指标，提取出了一个注册组件。所有的采集指标，都通过 `registerCollector` 函数进行注册。

```go
// arp_linux.go
type arpCollector struct {
    fs           procfs.FS
    deviceFilter deviceFilter
    entries      *prometheus.Desc
    logger       log.Logger
}

func init() {
    registerCollector("arp", defaultEnabled, NewARPCollector)
}

// NewARPCollector returns a new Collector exposing ARP stats.
func NewARPCollector(logger log.Logger) (Collector, error) {
    fs, err := procfs.NewFS(*procPath)
    if err != nil {
        return nil, fmt.Errorf("failed to open procfs: %w", err)
    }

    return &arpCollector{
        fs:           fs,
        deviceFilter: newDeviceFilter(*arpDeviceExclude, *arpDeviceInclude),
        entries: prometheus.NewDesc(
            prometheus.BuildFQName(namespace, "arp", "entries"),
            "ARP entries by device",
            []string{"device"}, nil,
        ),
        logger: logger,
    }, nil
}

// collector.go
var (
    factories              = make(map[string]func(logger log.Logger) (Collector, error))
    initiatedCollectorsMtx = sync.Mutex{}
    initiatedCollectors    = make(map[string]Collector)
    collectorState         = make(map[string]*bool)
    forcedCollectors       = map[string]bool{} // collectors which have been explicitly enabled or disabled
)

func registerCollector(collector string, isDefaultEnabled bool, factory func(logger log.Logger) (Collector, error)) {
    var helpDefaultState string
    if isDefaultEnabled {
        helpDefaultState = "enabled"
    } else {
        helpDefaultState = "disabled"
    }

    flagName := fmt.Sprintf("collector.%s", collector)
    flagHelp := fmt.Sprintf("Enable the %s collector (default: %s).", collector, helpDefaultState)
    defaultValue := fmt.Sprintf("%v", isDefaultEnabled)

    flag := kingpin.Flag(flagName, flagHelp).Default(defaultValue).Action(collectorFlagAction(collector)).Bool()
    collectorState[collector] = flag

    factories[collector] = factory
}
```

`registerCollector` 函数，在接收到采集项注册调用后，会做下列事情：

- 绑定采集项对应的终端启停命令，node_exporter help 信息中的 `--[no-]collector.xxxx` 便是通过这种形式来实现
- 填充采集指标启停状态：`collectorState[collector] = flag`
- 填充采集指标创建工厂方法：`factories[collector] = factory`

通过注册组件，搜

## 参考

- [node_exporter](https://github.com/prometheus/node_exporter)
- [procfs](https://pkg.go.dev/github.com/prometheus/procfs)
