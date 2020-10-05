---
title: "深入理解Python特性 - 1-Python简洁之道"
date: 2019-08-11 14:35:42
lastmod: 2019-08-11 14:35:42
draft: false
keywords: ["Books", "深入理解Python特性"]
description: "1-Python简洁之道"
tags: ["Books", "深入理解Python特性"]
categories: ["Books", "深入理解Python特性"]
author: "Alfons"
---

## 断言(assert)

断言是python程序中用于内部自检的方式之一，如声明一些代码中不可能出现的条件。如果触发了某个条件，即意味着程序中存在相应的bug。

语法规则为：`assert 判断语句, 异常提示`。

<!--more-->

```python
try:
    # a = True
    a = False

    assert a, ValueError("value error")

except Exception as e:
    print(e)

output:
value error
```

注意：

- **不使用断言验证数据**，如果在命令行中加入 `-O` 或 `-OO` 标识，或修改CPython中的 **PYTHONOPTIMIZE** 环境变量，都会全局禁用断言。
- **避免写出永不失败的断言**，例如 `assert (count==10, "error value")`，判断时，断言会将后面的元组当作判断条件，此时永远为真。

## 列表、字典中的逗号

逗号 `,` 的使用很大程度上可以避免一些常见的错误，例如在列表中，前后字符串元素中间如果缺少了逗号，将会把两个元素进行合并。

```python
list_a = ["Alfons", "Bob", "John"]
list_b = [
    "Alfons",
    "Bob"
    "John"
]
list_c = [
    "Alfons",
    "Bob",
    "John",  # 最后一个元素末尾加上逗号
]

list_a -> ['Alfons', 'Bob', 'John']
list_b -> ['Alfons', 'BobJohn']         # 元素合并了
list_c -> ['Alfons', 'Bob', 'John']
```

- 合理的格式化以及逗号的放置能让列表、字典和集合常量更容易维护。
- Python中的字符串拼接功能有时很方便，但有时又会引入一些难以发现的Bug。

建议使用 **括号** 进行字符串的拼接。

```python
str_a = "hello " \
        "world"
str_b = ("hello"
         "world2")

str_a -> hello world
str_b -> helloworld2
```

## 上下文和with语句

通过在类中实现 `__enter__` 和 `__exit__` 方法，能够使得一个对象作为上下文管理器，通过 **with** 关键字进行调用。

当执行流程进入with语句上下文时，会调用 `__enter__` 获取资源，离开with语句时，会调用 `__exit__` 释放资源。

```python
class Indenter:
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, text):
        print("\t" * self.level + text)


with Indenter() as indent:
    indent.print("hi")
    with indent:
        indent.print("Alfons")
        with indent:
            indent.print("Welcome")
    indent.print("Good Bye")

output:
	hi
		Alfons
			Welcome
	Good Bye
```

- with语句他哦你谷歌哦上下文管理器封装 `try...finally` 语句的标准用法来简化异常处理。
- with语句一般用来管理系统资源的安全获取和释放。资源首先由with语句获取，并在执行离开with上下文时自动释放。
- 有效的使用with有助于避免资源泄漏的问题，让代码更加易于阅读。

## 下划线、双下划线

- **前置单下划线_var**: 命名约定，用来表示该名称进在内部使用。一般对解释器没有特殊含义，只对程序员起提示作用。
- **后置单下划线var_**: 命名约定，避免与Python关键字冲突，例如 `class -> class_`。
- **前置双下划线__var**: 在类环境中使用时会触发名称改写，对Python解释器有特殊含义。
- **前后双下划线__var__**: 表示由Python语言定义的特殊方法。在自定义的属性中避免使用此种命名格式。
- **单下划线_**: 有时用作临时或无意义变量的名称。

对于 **前置双下划线__var**，有些特别的地方。**在类中所有前置双下划线的变量都会被解释器进行名称改写**。

```python
_Test__value = "hello"


class Test:
    def func(self):
        return __value


print(Test().func())

# 返回的结果
hello
```

## 字符串格式化方法

Python2、Python3中有多种字符串格式化的方法，选择喜欢的格式化方法即可。

```python
name = "Alfons"
error = 12345678

# 旧式字符串格式化
# str_a = "Hey %s, this is a 0x%x error!" % (name, error)
str_a = "Hey %(name)s, this is a 0x%(error)x error!" % dict(name=name, error=error)
print(str_a)

# 新式字符串格式化
str_b = "Hey {name}, this is a 0x{error:x} error!".format(name=name, error=error)
print(str_b)

# 字符串字面值插值,Python3.6+
str_c = f"Hey {name}, this is a 0x{error:x} error!"
print(str_c)

# 模板字符串
from string import Template

str_d = Template("Hey $name, this is a $error error!")
print(str_d.substitute(name=name, error=hex(error)))
```