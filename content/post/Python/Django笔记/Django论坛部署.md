---
title: "Django论坛部署"
date: 2018-07-07 19:12:47
lastmod: 2018-07-07 19:12:47
draft: false
keywords: ["Python", "Django笔记"]
description: "Django论坛部署"
tags: ["Python", "Django笔记"]
categories: ["Python", "Django笔记"]
author: "Alfons"
---

这两天在外部压力的作用下，把之前写的Django框架搭建的留言板部署了一下。本来是觉得，既然代码都已经弄得差不多了，本地运行没什么问题的，部不部署就没什么了。

哈哈哈，还是太天真了。

查看了一下原教程的[部署步骤](https://simpleisbetterthancomplex.com/series/2017/10/16/a-complete-beginners-guide-to-django-part-7.html)，应该问题不大。

服务器去年搭梯子时已经买了。私人部署，域名需不需要，感觉关系不大，可以省略。

OK，开始部署。

<!--more-->

> 有一句说一句，在整个学习过程中，不知道作者是不是故意的，把某个框的宽度设置成了22%，导致代码没办法很好的复制。我只好认为是作者的好意，让读者自己操作一遍，而不是简单复制粘贴。

## 开始部署

就按照原教程的步骤来。

### Version Control

使用的是git进行版本控制。好在之前的代码已经都传到了github，这一步不难。

直接把github上的代码clone下来

```shell
git clone yourProject.git
```

### Project Settings

需要用到的是一个.env文件，这个文件包含了一些特有的信息，代码上传github的时候并没把这个文件上传。

```shell
SECRET_KEY=××××××××××××××××××××××××××××××××××××××××
DEBUG=True
ALLOWED_HOSTS=.localhost,127.0.0.1
```

现在要做的就是新建一个.env文件，内容为setting.py中需要的内容。比如上面的 **SECRET_KEY** 、**DEBUG**、**ALLOWED_HOSTS**。

### Tracking Requirements

就是requirements.txt，还好每次都有存，现在只需要 **pip install -r requirements.txt**

### Domain Name

暂时不需要

### Deployment Strategy

之前已经买好了VPS。装上需要的软件就行了。

有一点需要说明的是，教程里使用的是Ubuntu的服务器，我使用的是Centos的服务器，这导致了后面的一些步骤不能完全照着教程上来。

#### Python 3.6

下载安装python3。

#### PostgreSQL

用的是sqlite3，这一步跳过。

#### NGINX

```shell
yum install nginx
```

#### Supervisor

用不来这个，取代的是使用systemd设置启动服务service来实现。

#### Virtualenv

```shell
pip3.6 install virtualenv
```

#### Application User

添加用户的步骤和教程不一样，详细步骤参考[Centos版本的](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-centos-quickstart)。

#### Django Project Setup

步骤和教程不一样，我只做了git clone以及后面运行manage.py部分。

git clone之前已经做过了。

如果数据库里已经含有了数据，因为我用到是之前测试的数据库，所以会出现下面的情况。提示 **No migrations to apply**。

```shell
python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, boards, contenttypes, sessions
Running migrations:
  No migrations to apply.
```

紧接着拷贝静态文件。

```shell
python manage.py collectstatic


You have requested to collect static files at the destination
location as specified in your settings:

    /home/××××/staticfiles

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes
Copying '/home/××××/venv/lib/python3.6/site-packages/django/contrib/admin/static/admin/css/changelists.css'
Copying '/home/××××/venv/lib/python3.6/site-packages/django/contrib/admin/static/admin/css/forms.css'
...

118 static files copied to '/home/××××/staticfiles'.
```

关键的一部是，需要把之前工程目录下的静态文件static目录下的文件夹链接到'/home/××××/staticfiles'下面。要不然访问时无法加载背景样式。

```shell
cd /home/××××/staticfiles
ln -s /home/××××/myproject/myproject/static/* ./
```

#### Configuring Gunicorn

按照教程上的来，不过路径有所改变。

#### Configuring Supervisor

使用的是systemd实现，具体操作是在 **/etc/systemd/system/** 目录下新建一个myDjango.service。

```txt
[Unit]
Description=YourProjectName
After=httpd.service

[Service]
TimeoutStartSec=0
ExecStart=/home/××××/gunicorn_start

[Install]
WantedBy=multi-user.target
```

然后启动，并设置成开机自启。

```shell
systemctl start myDjango
systemctl enable myDjango
```

#### Configuring NGINX

和教程上有些不同，我这是修改的 **/etc/nginx/nginx.conf**，在原配置文件的基础上，新增教程上的内容。

修改完后重启nginx服务。

```shell
systemctl restart nginx
```

至此，所有步骤结束，可以直接通过地址访问\^-^ [http://155.94.175.66/](http://155.94.175.66/)

## 踩的坑

|错误|原因|解决办法|
|:---:|:---|:---|
|一直提示502|工程的路径问题，因为一直使用的是root通过ssh访问，所以相关的工程都在root目录下，但貌似nginx对root权限有些特殊，所以造成了502错误。|将工程挪到 **/home** 目录下|
|背景样式无法展示|工程使用的样式路径不在staticfiles目录下|将工程使用的样式软连接到staticfiles目录下|
|提示数据库只读或者打开数据库失败|db.sqlite3文件的权限问题|将db.sqlite3文件的用户和用户组设置为boards|
