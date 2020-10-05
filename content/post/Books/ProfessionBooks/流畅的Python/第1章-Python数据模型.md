---
title: "流畅的Python - 第1章-Python数据模型"
date: 2019-03-09 22:05:43
lastmod: 2019-03-19 22:39:13
draft: false
keywords: ["Books", "流畅的Python"]
description: "第1章-Python数据模型"
tags: ["Books", "流畅的Python"]
categories: ["Books", "流畅的Python"]
author: "Alfons"
---

**魔术方法(magic method)** 是python特殊方法的昵称，形如 `__gititem__` 这样的方法成为特殊方法。

在python的风格中，通常没有 **collection.len()**，取而代之的是 **len(collection)**。关键是collection对象中实现了 `__len__` 方法。

<!--more-->

Python特殊方法分类：

跟运算符无关的特殊方法:

| 类别                    | 方法名                                                                                |
| :---------------------- | :------------------------------------------------------------------------------------ |
| 字符串/字节序列表示形式 | `__repr__`、`__str__`、`__format__`、`__bytes__`                                      |
| 数值转换                | `__abs__`、`__bool__`、`__complex__`、`__int__`、`__float__`、`__hash__`、`__index__` |
| 集合模拟                | `__len__`、`__getitem__`、`__setitem__`、`__delitem__`、`__contains__`                |
| 迭代枚举                | `__iter__`、`__reversed__`、`__next__`                                                |
| 可调用模拟              | `__call__`                                                                            |
| 上下文管理              | `__enter__`、`__exit__`                                                               |
| 实例创建和销毁          | `__new__`、`__init__`、`__del__`                                                      |
| 属性管理                | `__getattr__`、`__getattribute__`、`__setattr__`、`__delattr__`、`__dir__`            |
| 属性描述符              | `__get__`、`__set__`、`__delete__`                                                    |
| 跟类相关的服务          | `__prepare__`、`__instancecheck__`、`__subclasscheck__`                               |

跟运算符相关的特殊方法:

| 类别               | 方法名                                                                                                                                           |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| 一元运算符         | `__neg__ -`、`__pos__ +`、`__abs__ abs()`                                                                                                        |
| 比较运算符         | `__lt__ <`、`__le__ <=`、`__eq__ ==`、`__ne__ !=`、`__gt__ >`、`__ge__ >=`                                                                       |
| 算术运算符         | `__add__ +`、`__sub__ -`、`__mul__ *`、`__truediv__ /`、`__floordiv__ //`、`__mod__ %`、`__divmod__ divmod()`、`__pow__ **`、`__round__ round()` |
| 反向算术运算符     | `__radd__`、`__rsub__`、`__rmul__`、`__rtruediv__`、`__rfloordiv__`、`__rmod__`、`__rdivmod__`、`__rpow__`                                       |
| 增量赋值算术运算符 | `__iadd__`、`__isub__`、`__imul__`、`__itruediv__`、`__ifloordiv__`、`__imod__`、`__ipow__`                                                      |
| 位运算符           | `__invert__ ~`、`__lshift__ <<`、`__rshift__ >>`、`__and__ &`、`__or__ |`、`__xor__ ^`                                                           |
| 反向位运算符       | `__rlshift__`、`__rrshift__`、`__rand__`、`__ror__`、`__rxor__`                                                                                  |
| 增量赋值位运算符   | `__ilshift__`、`__irshift__`、`__iand__`、`__ior__`、`__ixor__`                                                                                  |