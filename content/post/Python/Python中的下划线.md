---
title: "Python中的下划线"
date: 2019-07-04 23:06:17
lastmod: 2019-07-04 23:06:17
draft: false
keywords: ["Python"]
description: "Python中的下划线"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

python中的变量命名可以是：**var**、**_var**、**__var**。

<!--more-->

今天看到一个很震惊的例子：

![under_line](/images/Python/python下划线/under_line.png)

输出居然为 `hello`！！！

对于 **Test** 类来说，本身的 **__ar** 变量在访问时，为了防止子类对 **"私有成员变量"** 进行覆盖，会被解释器解析为 **_Test__ar** 变量。如上图所示，所以输出为None。

但是，对于print方法里的 **__arga** 变量来说，都没有定义过，怎么还能输出？

官方的解释是，**在类环境中，带有双下划线的变量，不管是不是类成员变量，都会被改为 _ClassName__arg 这种形式！**

![double_line_class_value](/images/Python/python下划线/double_line_class_value.png)

有点变态了...

## 参考

- [private-variables-and-class-local-references](https://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references)