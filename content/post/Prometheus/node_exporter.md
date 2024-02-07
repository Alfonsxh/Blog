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

## 项目架构

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
```

所有的采集指标都在 [collector](https://github.com/prometheus/node_exporter/tree/master/collector) 目录之下，依赖语言特性，利用在每个指标项对应的 **xxx.go** 文件中的 `init()` 函数，实现自动注册。

注册核心代码：

```go
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

在 `main 函数（node_exporter.go）` 中，会进行 web 服务器 Handler 的创建

```go
// node_exporter.go
http.Handle(*metricsPath, newHandler(!*disableExporterMetrics, *maxRequests, logger))
```

`newHandler` 函数会新建出一个 Http.ServeHTTP 用于响应 API 采集请求。在 `newHandler` 函数中，会新建一个采集对象 **NodeCollector**，实现 [prometheus.Collector](https://pkg.go.dev/github.com/prometheus/client_golang/prometheus#Collector) 的接口。

```go
// collector.go
// NodeCollector implements the prometheus.Collector interface.
type NodeCollector struct {
    Collectors map[string]Collector
    logger     log.Logger
}

// NewNodeCollector creates a new NodeCollector.
func NewNodeCollector(logger log.Logger, filters ...string) (*NodeCollector, error) {
    f := make(map[string]bool)
    for _, filter := range filters {
        enabled, exist := collectorState[filter]
        if !exist {
            return nil, fmt.Errorf("missing collector: %s", filter)
        }
        if !*enabled {
            return nil, fmt.Errorf("disabled collector: %s", filter)
        }
        f[filter] = true
    }
    collectors := make(map[string]Collector)
    initiatedCollectorsMtx.Lock()
    defer initiatedCollectorsMtx.Unlock()
    for key, enabled := range collectorState {
        if !*enabled || (len(f) > 0 && !f[key]) {
            continue
        }
        if collector, ok := initiatedCollectors[key]; ok {
            collectors[key] = collector
        } else {
            collector, err := factories[key](log.With(logger, "collector", key))
            if err != nil {
                return nil, err
            }
            collectors[key] = collector
            initiatedCollectors[key] = collector
        }
    }
    return &NodeCollector{Collectors: collectors, logger: logger}, nil
}

// Describe implements the prometheus.Collector interface.
func (n NodeCollector) Describe(ch chan<- *prometheus.Desc) {
    ch <- scrapeDurationDesc
    ch <- scrapeSuccessDesc
}

// Collect implements the prometheus.Collector interface.
func (n NodeCollector) Collect(ch chan<- prometheus.Metric) {
    wg := sync.WaitGroup{}
    wg.Add(len(n.Collectors))
    for name, c := range n.Collectors {
        go func(name string, c Collector) {
            execute(name, c, ch, n.logger)    // 见下面内容
            wg.Done()
        }(name, c)
    }
    wg.Wait()
}
```

在 `NewNodeCollector` 函数中，会通过过滤条件，将符合要求的采集指标，通过工厂方法，创建出对应的 **采集指标对象**，添加到 `NodeCollector.Collectors` 字典中。

最终 API 采集的请求，会通过 `NodeCollector.Collect` 进行响应。并发遍历 `NodeCollector.Collectors` 字典中采集指标，调用采集指标的 `Update 函数`，进行指标采集。

```go
// collector.go
func execute(name string, c Collector, ch chan<- prometheus.Metric, logger log.Logger) {
    begin := time.Now()
    err := c.Update(ch)
    duration := time.Since(begin)
    var success float64

    if err != nil {
        if IsNoDataError(err) {
            level.Debug(logger).Log("msg", "collector returned no data", "name", name, "duration_seconds", duration.Seconds(), "err", err)
        } else {
            level.Error(logger).Log("msg", "collector failed", "name", name, "duration_seconds", duration.Seconds(), "err", err)
        }
        success = 0
    } else {
        level.Debug(logger).Log("msg", "collector succeeded", "name", name, "duration_seconds", duration.Seconds())
        success = 1
    }
    ch <- prometheus.MustNewConstMetric(scrapeDurationDesc, prometheus.GaugeValue, duration.Seconds(), name)
    ch <- prometheus.MustNewConstMetric(scrapeSuccessDesc, prometheus.GaugeValue, success, name)
}
```

## 指标项实现

每个采集指标项，均在 [collector](https://github.com/prometheus/node_exporter/tree/master/collector) 目录之下。需要实现 `Update` 接口。

```go
// collector.go
// Collector is the interface a collector has to implement.
type Collector interface {
    // Get new metrics and expose them via prometheus registry.
    Update(ch chan<- prometheus.Metric) error
}
```

在 `Update` 接口实现时，通过传入的管道参数，将采集指标的内容输出出去。例如 `arpCollector`:

```go
func (c *arpCollector) Update(ch chan<- prometheus.Metric) error {
    var enumeratedEntry map[string]uint32

    if *arpNetlink {
        var err error

        enumeratedEntry, err = getTotalArpEntriesRTNL()
        if err != nil {
            return fmt.Errorf("could not get ARP entries: %w", err)
        }
    } else {
        entries, err := c.fs.GatherARPEntries()
        if err != nil {
            return fmt.Errorf("could not get ARP entries: %w", err)
        }

        enumeratedEntry = getTotalArpEntries(entries)
    }

    for device, entryCount := range enumeratedEntry {
        if c.deviceFilter.ignored(device) {
            continue
        }
        ch <- prometheus.MustNewConstMetric(
            c.entries, prometheus.GaugeValue, float64(entryCount), device)
    }

    return nil
}
```

## procfs

`procfs` 是从 node_exporter 中抽离出来的模块，node_exporter 中的大部分场景，需要从 `/proc`、`/sys` 目录中读取系统信息。通过 `procfs` 的封装，能够实现系统信息的对象话。在添加指标项时，直接操作的是对象，很大程度上减轻了 Exporter 层的压力。

`procfs` 使用上也很简单，初始化一个 procfs 或者 sysfs 对象，然后直接调用对应的结构体方法即可。如下面的 CPU 信息：

```go
// cpu_linux.go
// NewCPUCollector returns a new Collector exposing kernel/system statistics.
func NewCPUCollector(logger log.Logger) (Collector, error) {
    fs, err := procfs.NewFS(*procPath)
    if err != nil {
        return nil, fmt.Errorf("failed to open procfs: %w", err)
    }

    sysfs, err := sysfs.NewFS(*sysPath)
    if err != nil {
        return nil, fmt.Errorf("failed to open sysfs: %w", err)
    }

    isolcpus, err := sysfs.IsolatedCPUs()
    if err != nil {
        if !os.IsNotExist(err) {
            return nil, fmt.Errorf("Unable to get isolated cpus: %w", err)
        }
        level.Debug(logger).Log("msg", "Could not open isolated file", "error", err)
    }
    ...
}
```

## 总结

- node_exporter 是非常重要的计算机系统信息采集工具
- node_exporter 框架本质上也是按照 "**三板斧**" 来
- 通过 Collector 层的封装，将多个采集指标项合并在一个 Collector 中，实现一个 API 多个指标项的采集，是非常好的 Exporter 实践
- node_exporter 大部分场景可以直接通过 procfs 模块的调用，来实现系统信息的采集。procfs 是非常nice的系统信息对象话模块，减少了解析系统信息的压力

## 参考

- [node_exporter](https://github.com/prometheus/node_exporter)
- [procfs](https://pkg.go.dev/github.com/prometheus/procfs)
