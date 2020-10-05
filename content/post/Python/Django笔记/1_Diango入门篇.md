---
title: "Django入门篇1-模型和admin用户"
date: 2018-11-09 00:26:41
lastmod: 2018-11-27 21:07:00
draft: false
keywords: ["Python", "Django笔记"]
description: "Django入门篇1-模型和admin用户"
tags: ["Python", "Django笔记"]
categories: ["Python", "Django笔记"]
author: "Alfons"
---

## 项目与应用

> `项目`是一个网站使用的配置和应用的集合。项目可以包含很多个应用。应用可以被很多个项目使用。
> `应用`是一个专门做某件事的网络应用程序——比如博客系统，或者公共记录的数据库，或者简单的投票程序。

在Django中，使用`startproject`来创建项目，使用`startapp`来创建应用。

<!--more-->

```shell
django-admin startproject mysite      # 创建项目

python manage.py startapp polls        # 创建应用
```

此时，整个项目的结构为

```shell
$ tree ./mysite/
./mysite/           # 项目文件夹
├── manage.py
├── mysite
│   ├── __init__.py
│   ├── settings.py     # Django 项目的配置文件。
│   ├── urls.py     # Django 项目的 URL 声明
│   └── wsgi.py     # 作为项目运行在 WSGI 兼容的Web服务器上的入口
└── polls           # 应用文件夹
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## 设置urls

在Django中，每个应用也可以含有各自的`URLconf`进行url映射。

为了创建`URLconf`，需要在应用`polls`中创建一个`urls.py`文件，此时目录结构应为如下所示。

```shell
$ tree ./polls/
./polls/
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
├── urls.py
└── views.py
```

在`polls/urls.py`文件中添加如下代码：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

在`mysite/urls.py`文件的`urlpatterns`列表中插入一个`include()`，如下：

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

此时，可以通过访问`http://127.0.0.1:8000/polls/`访问(**前提是在polls/views.py中实现了index响应**)。

## 设置模型

### 模型创建

Django中的模型有点类似于创建整个应用的数据库结构，在应用的`models.py`文件中实现。

模型有点类似于`SQLAlchemy`中的ORM，重点有三个方面。

- 编辑 models.py 文件，改变模型。
- 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
- 运行 python manage.py migrate 来应用数据库迁移。

在`models.py`文件中设置模型参数。

```python
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choidce_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
```

运行`makemigrations`改变生成的迁移文件。

```shell
$ python manage.py makemigrations polls
Migrations for 'polls':
  polls/migrations/0001_initial.py
    - Create model Choice
    - Create model Question
    - Add field question to choice
```

运行`migrate`迁移数据。

```shell
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Applying polls.0001_initial... OK
```

非常重要的一点，也是和 **SQLAlchemy ORM** 最大的区别是，Django中的数据迁移不需要重新删除和创建表！

### 为模型添加数据

Django通过为站点管理人员创建统一的内容编辑界面，使得公众页面和内容发布者页面完全分离。

首先，创建一个管理员账户。

```shell
$ python manage.py createsuperuser
```

接下来按要求输入用户名、密码等信息。

在`polls/admin.py`文件中，注册要在管理员界面上添加的模块。

```python
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
```

如上，添加了表`Question`和表`Choice`。

再次启动服务时，打开管理员登陆页面`http://127.0.0.1:8000/admin/`，登陆后展示如下：

![Django_admin_manage](/images/Python/Django笔记/1_Django_admin_manage.png)

通过页面可以增加、修改、删除表中的数据。也可以通过SQL命令在数据库中手动添加。