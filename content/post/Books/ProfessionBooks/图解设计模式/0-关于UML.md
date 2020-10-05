---
title: "图解设计模式 - 0-关于UML"
date: 2018-11-27 21:07:00
lastmod: 2018-11-27 21:07:00
draft: false
keywords: ["Books", "图解设计模式"]
description: "0-关于UML"
tags: ["Books", "图解设计模式"]
categories: ["Books", "图解设计模式"]
author: "Alfons"
---

`UML(Unified Modeling Language)统一建模语言`，是让系统可视化、让规格和设计文档化的表现方式。

<!--more-->

## 类图

`UML`中的类图(Class Diagram)用于表示类、接口、实例等之间相互的静态关系。虽然叫`类图`，但图中并不只有类。

![uml_demo](/images/Books/ProfessionBooks/图解设计模式/0_UML_demo_class.png)

图中的长方形表示类，长方形中被横线分为了3个区域：

- 类名
- 字段名
- 方法名

`抽象类`和`抽象方法`的名字用斜体方式显示。

## 接口和实现

![uml_demo_interface](/images/Books/ProfessionBooks/图解设计模式/0_UML_demo_interface.png)

接口的实现使用带箭头的虚线表示。

## 聚合关系

![uml_demo_aggregation](/images/Books/ProfessionBooks/图解设计模式/0_UML_demo_aggregation.png)

`聚合`指的是在一个类的实例是另一个类的成员。在`UML`中，使用带有空心菱形表示聚合关系。

## 可访问性

在`UML`中，通过在字段名和方法名前面加上记号来表示可见性。

- **+** 表示 **public** 字段和方法
- **-** 表示 **private** 字段和方法
- **#** 表示 **protected** 字段和方法
- **~** 表示只有同一包中的类才能访问的方法和字段