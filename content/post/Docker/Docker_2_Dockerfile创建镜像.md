---
title: "Docker(三) - Dockerfile 创建镜像"
date: 2019-03-08
lastmod: 2019-03-22
draft: false
keywords: ["Docker", "Dockerfile"]
description: "Dockerfile 创建镜像"
tags: ["Docker", "Dockerfile"]
categories: ["Docker"]
author: "Alfons"
---

**Dockerfile** 是一个文本格式的配置文件，用户可以通过使用 **Dockerfile** 文件快速自定义需要的镜像。

**Dockerfile** 由一行一行的命令构成，主体部分包括：**基础镜像信息**、**镜像操作指令**、**容器启动时执行指令**。

<!--more-->

## 镜像创建

创建镜像指令：`docker build -t imagename .`。**.** 表示的是 **Dockerfile** 文件所在的那个目录。

由于docker是 **C/S** 模式的，所以当我们运行 **build** 时，会将 **Dockerfile** 及其上下文发送给服务端，因此不建议将无关的内容和 **Docekrfile** 文件放置在一起。

## 基础镜像信息

使用 **FROM \<image\>** 指令来指定基础镜像，这一条是必须的，并且docker是严格按照顺序执行 **Dockerfile** 中的指令的，**FROM** 指令必须放在所有指令的第一条。

**image** 表示的是基础镜像的位置和名称，默认会先在本地仓库搜索对应镜像，本地没有则会从远程仓库拉取相关镜像。

镜像地址：<https://hub.docker.com/search?q=&type=image>。

可以先从远程仓库pull基础镜像到本地，也可以在build时直接远程仓库下载。

一些有趣的镜像：

- **scratch** - 空镜像，什么都没有，无法pull下来，所有镜像的最基础镜像。
- **busybox** - 临时系统镜像，体积很小，里面包含了大部分的Linux基础命令，测试使用。
- **alpine** - 系统镜像，体积很小，许多应用镜像都使用它作为基础镜像。
- **centos** - 系统镜像，用于生产环境，稳定性强，不过镜像的体积较大。
- **ubuntu** - 系统镜像，用于生产环境，常用于人工智能计算和企业应用。
- **debian** - 系统镜像，用于生产环境。

## 镜像操作指令

|  指令   |                                                 说明                                                 |
| :-----: | :--------------------------------------------------------------------------------------------------: |
|   ARG   |  定义创建镜像过程中所使用的变量，镜像编译完成后，ARG指定的变量的生存期结束。ENV指定的变量不会消失。  |
| VOLUME  | 创建启动容器时的数据卷挂载点，运行容器时可以从本地或其他容器挂载数据卷到此参数指定的数据卷挂载点上。 |
| ONBUILD |                      指定当该镜像作为基础镜像生成子镜像时，自动执行的操作指令。                      |
|   RUN   |                                       在编译镜像时执行的指令。                                       |
|   ADD   |                                添加内容到镜像，能够自动解压tar文件。                                 |
|  COPY   |                                           拷贝文件到镜像。                                           |

**ARG** 指令和 **ENV** 指令最大的不同在于，**ARG指定的变量**  在镜像编译完成后就消失了，而 **ENV** 指令指定的镜像可以作为 **环境变量** 在运行容器时使用。

**RUN** 指令用于生成镜像时对基础镜像的操作，例如大部分应用的镜像，会以某个系统镜像为基础，通过拷贝或者下载对应程序的方式，打包镜像。一般通过 **RUN** 指令进行下载更新软件时，需要注意将下载软件后的残余二进制文件进行清理。

另外大部分镜像使用的字体和时间都不是国内的标准，在制作镜像时，可以将这部分改过来。

**ADD** 指令的功能比 **COPY** 指令要强大，**ADD** 可以将url地址的文件添加到镜像中，也可以在添加完tar文件后，在镜像中自动解压tar文件。而 **COPY** 指令都不支持这两种方式，只能是 **拷贝文件或文件夹到镜像的指定路径**。

那该使用哪一个指令比较好呢？

**ADD** 指令有些时候会令人费解，有时会解压tar文件，有时候又不会。现在推荐的是使用 **COPY** 指令，在一种情况下可以使用 **ADD** 指令：将本地的tar文件打入镜像并解压。例如大部分系统镜像都是这么做的：

```dockerfile
FROM scratch
ADD alpine-minirootfs-20190228-ppc64le.tar.gz /
CMD ["/bin/sh"]
```

## 容器启动时执行指令

|    指令    |                            说明                             |
| :--------: | :---------------------------------------------------------: |
|   EXPOSE   |         声明镜像内监听的端口，并不会完成端口映射。          |
|    ENV     | 指定环境变量，可以在RUN指令中使用，也可以在容器运行时使用。 |
|  WORKDIR   |                       指定工作路径。                        |
| ENTRYPOINT |    指定镜像文件的默认入口命令。如有多条，最后一条生效。     |
|    CMD     |  指定启动容器时的默认执行的命令，如有多条，最后一条生效。   |

**EXPOSE** 指令声明容器启动后的开放端口，似乎没有什么作用，需要暴露端口时，还是需要使用 **-P或者-p** 参数在运行容器时指定。

**ENV** 和 **ARG** 指令最大的区别在于 **ENV** 指定的环境变量可以在容器运行时使用。在运行时使用 **-e** 参数指定环境变量，相同的环境变量会被替换。

### ENTRYPOINT和CMD

在谈及 **ENTRYPOINT** 和 **CMD** 指令之前，要先了解 **exec和shell两种模式**。

#### exec模式

对于 **exec模式**，命令执行在容器内的任务进程就是容器内的 **1号进程**。

```dockerfile
FROM ubuntu
CMD ["top"]
```

```shell
$ docker build -t test .
$ docker container run -dit --rm test
$ docker container exec -it sleepy_northcutt ps aux
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.5  0.0  36596  3176 pts/0    Ss+  06:45   0:00 top
root          6  0.0  0.0  34400  2904 pts/1    Rs+  06:46   0:00 ps aux
```

使用 `CMD/ENTRYPOINT ["cmd1", "cmd2"]` 的方式为 **exec模式**。

另外，在 **exec模式** 中，无法使用系统的环境变量。

```dockerfile
FROM ubuntu
CMD ["echo", "$PATH"]
```

```shell
$ docker build -t test .
$ docker container run -it --rm test
$PATH
```

#### shell模式

对于 **shell模式** 来说，命令执行在容器中的任务进程就不是 **1号进程** 了。

```dockerfile
FROM ubuntu
CMD top
```

```shell
$ docker build -t test .
$ docker container run -dit --rm test
$ docker container exec -it epic_neumann ps aux
USER        PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root          1  0.5  0.0   4628   924 pts/0    Ss+  06:46   0:00 /bin/sh -c top
root          6  0.0  0.0  36596  3172 pts/0    S+   06:46   0:00 top
root          7  0.0  0.0  34400  2856 pts/1    Rs+  06:47   0:00 ps aux
```

使用 **shell模式** 时，docker会以 `/bin/sh -c "task command"` 的方式来执行任务命令，也就是说，容器启动时时先起了一个bash进程，然后才启动我们的任务进程。

在 **shell模式** 中，就可以使用系统的环境变量。

```dockerfile
FROM ubuntu
CMD echo $PATH
```

```shell
$ docker build -t test .
$ docker container run -it --rm test
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

#### ENTRYPOINT和CMD指令使用

**ENTRYPOINT指令** 指向的是容器启动时，默认的执行程序，任务执行的优先级大于 **CMD指令**。

指令的使用方式有两种：

- **exec模式**: `ENTRYPOINT ["command", "param1", "param2"]`
- **shell模式**: `ENTRYPOINT command param1 param2`

**CMD指令** 指向的是容器启动时，执行的程序，不是默认程序。

指令的使用方式有三种：

- **exec模式**: `CMD ["command", "param1", "param2"]`
- **shell模式**: `CMD command param1 param2`
- **作为ENTRYPOINT指令的参数**: `CMD ["param1", "param2"]`

当 **CMD指令** 使用 **exec模式** 时，如果不存在 **ENTRYPOINT指令**，则它作为独立的任务命令执行。当存在 **ENTRYPOINT指令使用exec模式***，它只能作为 **ENTRYPOINT指令** 的任务参数使用。

当 **ENTRYPOINT指令使用shell模式** 时， **CMD指令的内容会被忽略掉**。

例如下面的镜像：

```dockerfile
FROM ubuntu

COPY entrypoint.sh /
ENTRYPOINT ["./entrypoint.sh"]
CMD ["echo", "hello"]
```

使用的 **entrypoint.sh** 脚本如下：

```bash
#!/bin/sh

for i in $@
do
    echo "$i"
done
```

执行：

```shell
$ docker build -t test .
$ docker container run -it --rm test
echo
hello
```

可以看到，执行的结果是 **将CMD指令的内容作为参数传递给了ENTRYPOINT指令**。

### 总结ENTRYPOINT和CMD

|                            |       No ENTRYPOINT        | ENTRYPOINT exec_entry p1_entry |     ENTRYPOINT ["exec_entry", "p1_entry"]      |
| :------------------------- | :------------------------: | :----------------------------: | :--------------------------------------------: |
| No CMD                     |         **error**          | /bin/sh -C exec_entry p1_entry |              exec_entry p1_entry               |
| CMD ["exec_cmd", "p1_cmd"] |      exec_cmd p1_cmd       | /bin/sh -C exec_entry p1_entry |      exec_entry p1_entry exec_cmd p1_cmd       |
| CMD ["p1_cmd", "p2_cmd"]   |       p1_cmd p2_cmd        | /bin/sh -C exec_entry p1_entry |       exec_entry p1_entry p1_cmd p2_cmd        |
| CMD exec_cmd p1_cmd        | /bin/sh -C exec_cmd p1_cmd | /bin/sh -C exec_entry p1_entry | exec_entry p1_entry /bin/sh -C exec_cmd p1_cmd |

## 参考

- [Dockerfile 中的 CMD 与 ENTRYPOINT](https://www.cnblogs.com/sparkdev/p/8461576.html)