---
title: "图解设计模式 - 1-Iterator模式"
date: 2018-11-27 21:07:00
lastmod: 2018-11-27 21:07:00
draft: false
keywords: ["Books", "图解设计模式"]
description: "1-Iterator模式"
tags: ["Books", "图解设计模式"]
categories: ["Books", "图解设计模式"]
author: "Alfons"
---

`迭代器模式`用于在数据集合中按照顺序遍历集合，遍历的顺序可以自定义，`从前往后`、`从后往前`、`跳跃式遍历`都可以。

`迭代器模式`是一种对接口编程的思想，迭代的过程不依赖于迭代目标的实现，而是通过迭代器来实现遍历，减少了类与类之间的耦合性。

<!--more-->

## 实例

书中使用了`书`和`书架`的例子来作为该模式的示例。

|名称|说明|
|:---|:---|
|Iterator|迭代器抽象类|
|BookShelfIterator|书架的迭代器类|
|Book|表示书的类|
|BookShelf|表示书架的类|
|Main|测试程序入口函数|

在`Book`类中定义了书的名字，实现了获取书名的方法。

`BookShelf`类中实现了通过索引获取对应书、添加新书的方法。

`BookShelfIterator`类继承于`Iterator`类使用书架实例进行初始化，实现了`HasNext`、`Next`虚方法。

![Iterator](/images/Books/ProfessionBooks/图解设计模式/1_Iterator.png)

代码放在[这里](https://github.com/Alfonsxh/DesignPattern/tree/master/Iterator)。

## 小结

> 不要只是用具体类来编程,要优先使用抽象类和接口来编程。

面向对象的编程方式有些时候会带来很多弊端，比如`强耦合性`、`实现复杂`。

后续编程的方式，应该朝着`面向接口编程`方向发展。