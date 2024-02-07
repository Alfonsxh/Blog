---
title: "Exporter简单入门"
date: 2024-02-04T18:16:45+08:00
lastmod: 2024-02-04T18:16:45+08:00
draft: false
keywords: ["Prometheus", "Exporter"]
description: ""
tags: ["Prometheus", "Exporter"]                      # 归档 
categories: ["Prometheus", "Exporter"]                # 分类
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

各个采集端(Exporter)是 Prometheus 的数据来源，在看了多个官方的 exporter 后，总结了一下。

<!--more-->

## 如何编写 Exporter

编写 Exporter，有许多种语言的实现，下面以 Go 框架为基础。

总体概括，Exporter 编写主要有下面三个步骤：

- 「1」创建采集项 Collector。Collector 核心为 Collect 方法，指标项结果处理后，通过 ch 管道传出

    ```go
    type Collector struct {}
    
    func (c *Collector) Describe(ch chan<- *prometheus.Desc) {}
    
    func (c *Collector) Collect(ch chan<- prometheus.Metric) {
        desc := prometheus.NewDesc(
            prometheus.BuildFQName("node", "cpu", "info"),
            "Show CPU information.",
            []string{"label_1", "label_2", "label_3"},
            prometheus.Labels{"Hello": "World"},
        )
        ch <- prometheus.MustNewConstMetric(
            desc,
            prometheus.CounterValue,
            1.0,
            "1.0", "2.0", "3.0",
        )
    }
    ```

- 「2」注册采集项对象。通过框架标准方法注册采集项 Collector

    ```go
    // Create a non-global registry.
    reg := prometheus.NewRegistry()
    _ = reg.Register(c)
    ```

- 「3」绑定HttpHandler，并启动web服务

    ```go
    // Expose metrics and custom registry via an HTTP server
    // using the HandleFor function. "/metrics" is the usual endpoint for that.
    http.Handle("/node_metrics", promhttp.HandlerFor(reg, promhttp.HandlerOpts{Registry: reg}))
    log.Fatal(http.ListenAndServe(":8080", nil))  
    ```
  
Exporter 本质上只是一个web服务。Prometheus 会通过配置中的 API，对 Exporter 发起请求，Exporter 对应的借口进行响应。最终通过触发 `Collector.Collect` 函数进行采集。

在 `Collector.Collect` 函数中，传入的参数是：`ch chan<- prometheus.Metric`。采集指标通过这个管道往调用层传输，最终输出到API结果中。

采集指标 `prometheus.Metric` 也是有一定的结构、类型的。

采集指标主要使用到的类型包括：Gauge、Counter。另外两个 Histogram、Summary，一般不会使用到，这里不讲。

采集指标主要由 **描述信息、值、label、固定label** 组成

初始化指标实例的方法有很多，目前比较主流的方式是：先初始化描述信息、在执行 `Collector.Collect` 动作时，填充其他信息。

```go
desc := prometheus.NewDesc(
    prometheus.BuildFQName("node", "cpu", "info"),
    "Show CPU information.",
    []string{"label_1", "label_2", "label_3"},
    prometheus.Labels{"Hello": "World"},
)

ch <- prometheus.MustNewConstMetric(
    desc,
    prometheus.CounterValue,
    1.0,
    "1.0", "2.0", "3.0",
)
```

`prometheus.NewDesc` 具体参数如下：

```Go
func NewDesc(fqName, help string, variableLabels []string, constLabels Labels) *Desc
```

- **fqName** - 采集指标名称，通过 `prometheus.BuildFQName` 函数生成，也可以自定义
- **help** - 采集指标的 help 信息
- **variableLabels** - 采集指标的 label
- **constLabels** - 固定的采集指标 label

`prometheus.MustNewConstMetric` 具体参数如下：

```Go
func MustNewConstMetric(desc *Desc, valueType ValueType, value float64, labelValues ...string) Metric
```

- **desc** - 描述信息
- **valueType** - 指标值的类型
- **value** - 指标值
- **labelValues** - label 的值

如上面的例子，将输出：

```text
# HELP node_cpu_info Show CPU information.
# TYPE node_cpu_info counter
node_cpu_info{Hello="World",label_1="1.0",label_2="2.0",label_3="3.0"} 1
```

完整事例代码如下：

```go
package main

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "log"
    "net/http"
    "runtime"
)

type Metrics struct {
    cpuTemp        prometheus.Gauge
    goRuntime      prometheus.GaugeFunc
    hdFailures     prometheus.Counter
    hdFailuresFunc prometheus.CounterFunc

    //metrics prometheus.Metric
}

func (c *Metrics) Describe(ch chan<- *prometheus.Desc) {
    ch <- c.cpuTemp.Desc()
    ch <- c.hdFailures.Desc()
    ch <- c.goRuntime.Desc()
}

func (c *Metrics) Collect(ch chan<- prometheus.Metric) {
    c.cpuTemp.Set(65.3)
    ch <- c.cpuTemp

    c.goRuntime.Collect(ch)

    c.hdFailures.Inc()
    ch <- c.hdFailures

    c.hdFailuresFunc.Collect(ch)

    ch <- prometheus.MustNewConstMetric(
        prometheus.NewDesc(
            prometheus.BuildFQName("node", "cpu", "info"),
            "Show CPU information.",
            []string{"label_1", "label_2", "label_3"},
            prometheus.Labels{"Hello": "World"},
        ),
        prometheus.CounterValue,
        1.0,
        "1.0", "2.0", "3.0",
    )
}

func main() {
    m := &Metrics{
        cpuTemp: prometheus.NewGauge(
            prometheus.GaugeOpts{
                Name: "cpu_temperature_celsius",
                Help: "Current temperature of the CPU.",
            },
        ),
        goRuntime: prometheus.NewGaugeFunc(
            prometheus.GaugeOpts{
                Subsystem: "runtime",
                Name:      "goroutines_count",
                Help:      "Number of goroutines that currently exist.",
            },
            func() float64 { return float64(runtime.NumGoroutine()) },
        ),

        hdFailures: prometheus.NewCounter(
            prometheus.CounterOpts{
                Name: "hd_errors_total",
                Help: "Number of hard-disk errors.",
            },
        ),
        hdFailuresFunc: prometheus.NewCounterFunc(
            prometheus.CounterOpts{
                Name: "hd_errors_total_func",
                Help: "Number of hard-disk errors.",
            },
            func() float64 { return 1.0 },
        ),
    }

    // Create a non-global registry.
    reg := prometheus.NewRegistry()
    _ = reg.Register(m)

    //// Create new metrics and register them using the custom registry.
    //m := NewMetrics(reg)

    //// Set values for the new created metrics.
    //m.cpuTemp.Set(65.3)
    //m.hdFailures.With(prometheus.Labels{"device": "/dev/sda"}).Inc()

    // Expose metrics and custom registry via an HTTP server
    // using the HandleFor function. "/metrics" is the usual endpoint for that.
    http.Handle("/metrics", promhttp.HandlerFor(reg, promhttp.HandlerOpts{Registry: reg}))
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## 总结

- Prometheus 的 Exporter 就是一个 Web 服务端，Prometheus 通过定时访问对应的 API 进行指标项的采集
- Exporter 的编写按照上述的 "**三板斧**" 进行
- 最终采集指标的值，通过管道传输到调用层

## 参考

- [client_golang](https://pkg.go.dev/github.com/prometheus/client_golang)