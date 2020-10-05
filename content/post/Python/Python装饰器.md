---
title: "Python装饰器----Decorator"
date: 2019-01-26 11:00:55
lastmod: 2019-03-09 22:05:43
draft: false
keywords: ["Python"]
description: "Python装饰器----Decorator"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

**Python** 的装饰器模式通过 **语法糖** 实现，相较于其他语言的装饰器模式，十分的优雅。

<!--more-->

下面的例子为Python中主要的装饰器实现事例。

## 函数装饰器

在 **Python** 中一切皆对象，是对象就能被装饰，函数也不例外。

### 不带参数的装饰器

作为装饰器的函数可以带有传入参数，也可以不带传入参数。当不带传入参数时，对应的实现如下：

```python
# 斐波纳兹数列
def Memoization(fn):
    cache = dict()

    @wraps(fn)
    def Wrapper(*args):
        result = cache.get(args)

        if result is None:
            result = fn(*args)
            cache[args] = result

        return result

    return Wrapper


@Memoization
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

如上面的例子所示，装饰器函数中不带参数，那么装饰器函数的传入参数即为 **被装饰的函数**。(有点绕)

简单来说：

- 在被装饰之前，调用的是 `fib(100)`。
- 在函数被装饰后
  - 调用的是 `Memoization(fib)(100)`。
  - 由于被装饰了，所以实际上调用的是 `Wrapper(100)`。
  - 在wrapper内部对计算结果进行了缓存，但实际返回的结果仍为 **原始函数 fib** 计算的结果。

### 带参数的装饰器

在带参数的装饰器函数中，传入参数不再是 **被装饰的函数**。

```python
def AddHtmlTag(tag, *args, **kwargs):
    def Decorator(fn):
        css_class = "class=\"{}\"".format(kwargs["css_class"]) if "css_class" in kwargs else ""

        def Wrapper(*args):
            print(fn.__name__)
            return "<{tag} {css}>{fn}</{tag}>".format(tag = tag, css = css_class, fn = fn(*args))

        return Wrapper

    return Decorator


@AddHtmlTag(tag = 'div', css_class = "center")
@AddHtmlTag(tag = 'b', css_class = "black")
def Hello(name):
    return "hello world!" + name


print(Hello("tmo"))

# output
Wrapper
Hello
<div class="center"><b class="black">hello world!tmo</b></div>
```

如上面的例子，生成html中的tag标签。在装饰函数中有自己的传入参数，在装饰时需要添加，如：`@AddHtmlTag(tag = 'b', css_class = "black")`。

**AddHtmlTag函数** 返回一个真正的装饰器函数 **Decorator**，**Decorator** 函数的传入参数为被装饰的函数。

**Decorator** 函数返回的又是一个函数 **Wrapper**，**Wrapper** 函数才是真正实现功能的部分。

(有点绕)

简单来说：

- 在被装饰之前，调用的是 `Hello("tmo")`。
- 在函数被装饰后
  - 调用的是 `AddHtmlTag(tag = 'b', css_class = "black")(Hello)("tmo")`。
  - 其中 `AddHtmlTag(tag = 'b', css_class = "black")` 返回的是 `Decorator`，所以就相当于调用了 `Decorator(Hello)("tmp)`。
  - `Decorator(Hello)`被调用后返回了 `Wrapper`，于是就相当于调用了 `Wrapper("tmo")`。
  - 随着每一层的递进调用，每一层都添加了原函数没有的功能，最终就编程了另一个函数。

值得注意的一点是，多个装饰器调用的顺序，类似于 **入栈出栈**，最开始出现的装饰器先进栈，按照 **先入后出** 的原则，最开始的装饰器在最后才会被执行。

## 类装饰器

**类装饰器** 和 **函数装饰器** 相比，更加的方便了。

```python
class MyApp:
    def __init__(self):
        self.__func_map = dict()

    def Register(self, name):
        def Wrapper(fn):
            self.__func_map[name] = fn
            return fn

        return Wrapper

    def Call(self, name):
        func = self.__func_map.get(name, None)
        if func is not None:
            return func()

        raise Exception("No func exist. -> {}".format(name))


app = MyApp()


@app.Register("/")
def man_page():
    return "This is man page."


@app.Register("/sec")
def sec_page():
    return "This is sec page"


print(app.Call("/"))
print(app.Call("/sec"))

# output
This is man page.
This is sec page
```

如上面的例子，模拟了一般的web框架的路由规则注册。

- 首先新建一个类，作为装饰器使用，类中实现 **注册功能的函数**，以及 **调用功能的函数**。
- 实例化对象 `app = MyApp()`。
- 使用 `app.Register` 装饰函数，作为注册路由功能。
- 后续只需要执行类似于 `app.Call("/")` 的命令就能访问对应的函数了。

## 小结

之前看了用 c++ 以及 Java 对装饰器的实现，只能说，太复杂了！

人生苦短！

## 参考

- [C++装饰器](https://blog.csdn.net/My_heart_/article/details/62238091)
- [Java装饰器](https://juejin.im/post/5add8e9cf265da0b9d77d377)