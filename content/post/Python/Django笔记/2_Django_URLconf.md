---
title: "Django--URLconf"
date: 2018-11-27 16:24:15
lastmod: 2018-11-27 16:24:15
draft: false
keywords: ["Python", "Django笔记"]
description: "Django--URLconf"
tags: ["Python", "Django笔记"]
categories: ["Python", "Django笔记"]
author: "Alfons"
---

`URLconf (URL configuration)`，Django中的 **URL调度器** 使用的是纯python代码，是 **URL路径** 解释到 **Python功能函数** 的映射。

<!--more-->

## urlpatterns设置url路径

**Django**加载Python模块时，会去寻找 **urlpatterns** 参数，它是一个 **django.urls.path()** 或者 **django.urls.re_path()** 对象单例的列表。

```python
urlpatterns = [
    path('articles/<int:year>/', views.year_archive),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
]
```

### django.urls.path()

使用 **path()** 捕获url时，要注意以下几点：

- 在使用 **path()** 匹配url时，使用 **<>** 捕获值。例如上面 **articles/\<int:year\>/**，捕获了int类型的年份信息。
- path部分末尾使用 **/** 结尾，开头不必添加 **/**。

在捕获url时，使用路径转换器可以指定参数的类型。

- **str** - 匹配除路径分隔符 **/** 之外的任何非空字符串。如果转换器未包含在表达式中，则这是默认值。
- **int** - 匹配零或任何正整数，返回一个int。
- **slug** - 匹配由ASCII字母或数字组成的任何slug字符串，以及连字符和下划线字符。例如，**building-your-1st-django-site**。
**uuid** - 匹配格式化的UUID。要防止多个URL映射到同一页面，必须包含短划线并且字母必须为小写。例如，**075194d3-6885-417e-a8a8-6c931e272f00**。返回一个 UUID实例。
**path** - 匹配任何非空字符串，包括路径分隔符 **/**。这使您可以匹配完整的URL路径，而不仅仅是URL路径的一部分str。

除此之外，还可以自定义转换器。

```python
from django.urls import path, register_converter

from . import converters, views

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('articles/2003/', views.special_case_2003),
    path('articles/<yyyy:year>/', views.year_archive),
    ...
]
```

如上，使用 **register_converter** 注册了新的年份转换器 **yyyy**。

### django.urls.re_path()

如果 **path()** 和转换器的组合不能够满足输入的 **URL 样式**，则可以选择使用 **re_path()** 代替 **path()**。

**Python** 中声明为正则表达式的方式为 **(?P\<name\>pattern)**：

- 括号为 **必加项**。
- 其中 **?P** 为声明待捕获参数， **\<name\>** 为要捕获的参数名称。如果不指定捕获参数的话，使用 **?:** 代替。
- **pattern** 为捕获参数的表达式语句。
  
也可以不指定捕获参数，直接使用 **(pattern)**。

```python
re_path(r'^comments/(?:page-(?P<page_number>\d+)/)?$', comments),  # good
```

上面的例子中，如果待匹配的URL地址为 **comments/page-2/**，则会将 **2** 赋值给 **page_number** 参数。

另外，每个 **re_path()** 匹配紧在第一次使用时编译一次，后续再次匹配到时，不会再进行编译！

## 使用其他目录下的URLconfs

在根目录或其他目录下的 **urlpattern** 列表中，使用 **include** 包含其他 **URLconf** 模块。

```python
# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]

# polls/urls.py
from django.urls import path, re_path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name = 'index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name = 'detail'),
    # ex: /polls/5/resultes/
    path('<int:question_id>/resultes/', views.results, name = 'resultes'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name = 'vote'),
]
```

上述例子中，根目录下的 **urls.py** 中添加了应用 **polls** 中的URLconf模块。当访问 **polls/3/resultes/** 时，会在 **polls/urls.py** 下的路径中查找对应的函数功能。

## 反射URL路径

使用 **reverse(viewsname)** 函数，可以根据在 **urlpatterns** 注册的路径中的 **name** 参数，返回 **viewsname** 的 url 地址。

```python
# polls/urls.py
urlpatterns = [
    # ex: /polls/
    path('', views.index, name = 'index'),

    re_path(r'^regex/(?P<year>[0-9]{4})/$', views.regex, name = 'regex'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name = 'detail'),
    # ex: /polls/5/resultes/
    path('<int:question_id>/resultes/', views.results, name = 'resultes'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name = 'vote'),
]

# polls/views.py
def regex(request, year):
    url_path = reverse("detail", args = (year,))
    return HttpResponseRedirect(url_path)
```

上述例子中，在访问 **regex** 函数时，会根据 **detail** 反射出的url路径，进行重定向。例如，访问地址 **polls/regex/1234** 将重定向到地址 **polls/1234/**。