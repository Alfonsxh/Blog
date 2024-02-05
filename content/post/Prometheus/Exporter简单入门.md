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

编写 Exporter，有许多种语言的实现，下面以 Go 框架为基础。

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

总体概括，主要有下面三个步骤：

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
  
