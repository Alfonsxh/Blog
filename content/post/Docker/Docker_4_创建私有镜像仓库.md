---
title: "Docker(五) - 创建私有镜像仓库"
date: 2019-05-14
lastmod: 2019-05-14
draft: false
keywords: ["Docker"]
description: "创建私有镜像仓库"
tags: ["Docker"]
categories: ["Docker"]
author: "Alfons"
---

默认情况下，我们下载镜像的位置都是 <https://hub.docker.com>。

在国内，使用上面的仓库地址可能会下载得很慢，使用国内的镜像源在很大程度上会加快下载速度。

<!--more-->

在 `/etc/docker/daemon.json` 文件中添加下面内容：

```shell
$ cat /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}
```

在企业使用时，可能不太希望自己的镜像文件暴露在公网上，这样就催生了 **Docker私有镜像仓库** 的产生。

搭建私有镜像仓库的方式有两种，下面介绍的是我认为更好的一种：在docker容器中搭建docker私有镜像仓库。

## 在docker容器中搭建私有镜像仓库

docker有私有镜像仓库的镜像，使用起来十分的方便，只需几个命令就可以搭建起一个实用的私有仓库。

```shell
$ docker container run -d --name my_registry -v /home/xiaohui/.registry/:/var/lib/registry -p 5000:5000 --restart=always registry
Unable to find image 'registry:latest' locally
latest: Pulling from library/registry
c87736221ed0: Pull complete 
1cc8e0bb44df: Pull complete 
54d33bcb37f5: Pull complete 
e8afc091c171: Pull complete 
b4541f6d3db6: Pull complete 
Digest: sha256:3b00e5438ebd8835bcfa7bf5246445a6b57b9a50473e89c02ecc8e575be3ebb5
Status: Downloaded newer image for registry:latest
872e0619a6b0fe84ffc099de20982c0e8972414991ecb5e682b746b34650a071
```

- **-v** - 指定私有仓库的数据卷映射。
- **-p** - 指定容器与宿主机的端口映射。

### 在宿主机上上传下载镜像

上面的命令就搭建好了一个简单的私有镜像仓库。我们可以上传下载自己的镜像文件了。

```shell
$ docker image tag alfonsxh/jupyter:latest 127.0.0.1:5000/my_jupyter
$ docker image ls -a
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
registry                    latest              f32a97de94e1        5 weeks ago         25.8MB
127.0.0.1:5000/my_jupyter   latest              319e7e409a6a        7 weeks ago         297MB
alfonsxh/jupyter            latest              319e7e409a6a        7 weeks ago         297MB

// 上传镜像至本地仓库
$ docker push 127.0.0.1:5000/my_jupyter
The push refers to repository [127.0.0.1:5000/my_jupyter]
1370fa617ec7: Pushed 
1d08f718d11c: Pushed 
31f774dbb6c4: Pushed 
01234f01aa77: Pushed 
35e69abd31ba: Pushed 
503e53e365f3: Pushed 
latest: digest: sha256:0c081e0c24d3dc9dd1ff3f20c1251d2f9c2c5240ee21d5f97c2df155873742eb size: 1580
```

下载的话，只需要将镜像的来源地址指定到本地的地址就可以了。

```shell
// 从本地私有仓库下载镜像文件
$ docker image ls -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
registry            latest              f32a97de94e1        5 weeks ago         25.8MB
$ docker image pull 127.0.0.1:5000/my_jupyter
Using default tag: latest
latest: Pulling from my_jupyter
6c40cc604d8e: Pull complete 
eb28c72fd5c9: Pull complete 
8b7b7e8a3ec6: Pull complete 
07400c149ca6: Pull complete 
93b52b0b4673: Pull complete 
7ffe8540cda4: Pull complete 
Digest: sha256:0c081e0c24d3dc9dd1ff3f20c1251d2f9c2c5240ee21d5f97c2df155873742eb
Status: Downloaded newer image for 127.0.0.1:5000/my_jupyter:latest
$ docker image ls -a
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
registry                    latest              f32a97de94e1        5 weeks ago         25.8MB
127.0.0.1:5000/my_jupyter   latest              319e7e409a6a        7 weeks ago         297MB

// 如果不想要镜像名前面的一长串地址信息，可以使用tag命令对镜像重新打tag
$ docker image tag 127.0.0.1:5000/my_jupyter:latest my_jupyter
$ docker image ls -a
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
registry                    latest              f32a97de94e1        5 weeks ago         25.8MB
127.0.0.1:5000/my_jupyter   latest              319e7e409a6a        7 weeks ago         297MB
my_jupyter                  latest              319e7e409a6a        7 weeks ago         297MB
```

### 在局域网内上传下载镜像

上面演示的是本机上的操作，对于非宿主机来说，需要进行一些其他的设置才能从私有仓库进行下载。如果不进行设置，则可能会出现下面的问题。

```shell
// 查看私有镜像仓库
$ curl 192.168.2.68:5000/v2/_catalog
{"repositories":["my_jupyter"]}

$ docker pull 192.168.2.68:5000/my_jupyter
Using default tag: latest
Error response from daemon: Get https://192.168.2.68:5000/v2/: http: server gave HTTP response to HTTPS client
```

如上面的命令，尝试从局域网的私有仓库中下载镜像时，会出现 `http: server gave HTTP response to HTTPS client` 的错误。原因在于，私有服务器默认是启用了 **http服务，但客户端这边默认使用的是https进行访问**。

解决方式有两种:

- 一种是在客户端的 `/etc/docker/daemon.json` 配置文件中，添加忽略条件。
- 另一种是在服务端启用https协议。

#### 修改客户端的配置文件

这种方式比较简单，只需要修改 `/etc/docker/daemon.json` 配置文件，在配置文件中添加服务端的域名和端口信息。

```json
{
   "registry-mirrors": ["https://registry.docker-cn.com"],
   "insecure-registries":[
        "192.168.2.68:5000"
    ]
}
```

然后重启docker服务，便能下载了。

```shell
$ systemctl restart docker.service
$ docker pull 192.168.2.68:5000/my_jupyter
Using default tag: latest
latest: Pulling from my_jupyter
6c40cc604d8e: Already exists 
eb28c72fd5c9: Pull complete 
8b7b7e8a3ec6: Pull complete 
07400c149ca6: Pull complete 
93b52b0b4673: Pull complete 
7ffe8540cda4: Pull complete 
Digest: sha256:0c081e0c24d3dc9dd1ff3f20c1251d2f9c2c5240ee21d5f97c2df155873742eb
Status: Downloaded newer image for 192.168.2.68:5000/my_jupyter:latest
```

#### 在服务端启用https服务

(未完，待续)