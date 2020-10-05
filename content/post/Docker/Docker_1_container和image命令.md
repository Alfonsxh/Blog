---
title: "Docker(二) - Cli命令: container和image"
date: 2019-03-02
lastmod: 2019-03-22
draft: false
keywords: ["Docker", "Cli"]
description: "docker cli命令基础"
tags: ["Docker"]
categories: ["Docker"]
author: "Alfons"
---

主要记录一些常见的命令使用，避免遗忘。命令行操作的话，个人比较喜欢 `docker image rm xxx` 的方式，不太喜欢直接使用精简命令的方式，例如 `docker rmi xxxx`。

<!--more-->

操作系统：**Ubuntu 18.04**
Docker Version：**18.09.2**

## 镜像

镜像文件可以把它想象成可执行程序的 **二进制文件**，可以直接通过网络的方式下载，也可以自己打包镜像文件。

与镜像相关的操作参数如下所示：

```shell
Commands:
  build       Build an image from a Dockerfile
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Display detailed information on one or more images
  load        Load an image from a tar archive or STDIN
  ls          List images
  prune       Remove unused images
  pull        Pull an image or a repository from a registry
  push        Push an image or a repository to a registry
  rm          Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
```

### 下载镜像

通过 `docker search xxx` 可以在默认的镜像仓库注册服务器 **Doceker Hub** 上搜索目标的镜像信息。

```shell
$ docker search ubuntu
NAME                                                   DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
ubuntu                                                 Ubuntu is a Debian-based Linux operating sys…   9198                [OK]                
dorowu/ubuntu-desktop-lxde-vnc                         Ubuntu with openssh-server and NoVNC            270                                     [OK]
rastasheep/ubuntu-sshd                                 Dockerized SSH service, built on top of offi…   201                                     [OK]
consol/ubuntu-xfce-vnc                                 Ubuntu container with "headless" VNC session…   156                                     [OK]
...
```

通过 `docker image pull xxx` 的方式会从默认的镜像仓库注册服务器 **Docker Hub** 下载对应的镜像文件，如果需要从别的镜像服务器下载的话，可以添加必要的地址，如 `docker image pull hub.c.163.com/public/xxx`。

参数说明：

| 参数                    | 说明                                                                      |
| :---------------------- | :------------------------------------------------------------------------ |
| -a, --all-tags          | 是否下载所有的版本镜像文件，默认为false，只会下载指定的或者最新的镜像文件 |
| --disable-content-trust | 取消镜像的内容校验，默认为true                                            |

另外的一种下载方式是，使用 **run** 命令，它会现在本地查找镜像，如果不存在，会从 **Docker Hub** 上下载下来，再运行。

```shell
$ docker container run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
1b930d010525: Pull complete
Digest: sha256:2557e3c07ed1e38f26e389462d03ed943586f744621577a99efb77324b0fe535
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### 查看镜像信息

#### 查看所有镜像文件的基本信息

使用 **ls** 参数能够列出本机上存在的镜像。

参数说明：

| 参数                | 说明                                        |
| :------------------ | :------------------------------------------ |
| -a, --all           | 显示所有(包括临时文件)镜像文件，默认为false |
| --digests           | 显示镜像的数字摘要，默认为false             |
| -f, --filter filter | 过滤列出的镜像                              |
| --format string     | 控制输出格式，GO语言format，如.ID代表ID信息 |
| --no-trunc          | 对输出结果进行截取，默认为true              |
| -q, --quiet         | 只显示ID信息                                |

```shell
$ docker image ls --digests
REPOSITORY          TAG                 DIGEST                                                                    IMAGE ID            CREATED             SIZE
hello-world         latest              sha256:2557e3c07ed1e38f26e389462d03ed943586f744621577a99efb77324b0fe535   fce289e99eb9        6 weeks ago         1.84kB

$ docker image ls -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              fce289e99eb9        6 weeks ago         1.84kB
```

#### 添加镜像标签

使用 **tag** 参数可以为镜像添加标签(alias)。使用方式为 `docker image tag {oldname} {newname}`

```shell
$ docker image tag hello-world myhello
$ docker image ls -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              fce289e99eb9        6 weeks ago         1.84kB
myhello             latest              fce289e99eb9        6 weeks ago         1.84kB
$ docker container run myhello

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

可以看到会多出一个名为 **myhello** 的镜像文件，镜像ID和之前的 **hello-world** 是一样的。使用起来也是一样的。

#### 查看镜像详细信息

使用 **inspect** 命令可以查看镜像的详细信息。包括制作者、适应架构、各层的数字摘要等。

```shell
$ docker image inspect hello-world:latest
[
    {
        "Id": "sha256:fce289e99eb9bca977dae136fbe2a82b6b7d4c372474c9235adc1741675f587e",
        "RepoTags": [
            "hello-world:latest",
            "myhello:latest"
        ],
        "RepoDigests": [
            "hello-world@sha256:2557e3c07ed1e38f26e389462d03ed943586f744621577a99efb77324b0fe535"
        ],
        "Parent": "",
        "Comment": "",
...
```

使用 **--format** 会根据GO语言format的格式进行解析。

#### 查看镜像的历史信息

```shell
$ docker image history hello-world:latest 
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
fce289e99eb9        6 weeks ago         /bin/sh -c #(nop)  CMD ["/hello"]               0B                  
<missing>           6 weeks ago         /bin/sh -c #(nop) COPY file:f77490f70ce51da2…   1.84kB 
```

### 删除镜像

使用 **rm** 命令可以用来删除已经存在的镜像。

| 参数        | 说明                                 |
| :---------- | :----------------------------------- |
| -f, --force | 强制删除镜像文件，即使有容器依赖关系 |
| --no-prune  | 不要清理未带标签的父镜像             |

在删除镜像时，可以使用镜像名称来删除，也可以使用镜像ID来删除，在使用镜像ID进行删除时，可以只用省略的形式来指明是哪一个镜像文件。

```shell
$ docker image ls -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              latest              47b19964fb50        12 days ago         88.1MB
hello-world         latest              fce289e99eb9        6 weeks ago         1.84kB
myhello             latest              fce289e99eb9        6 weeks ago         1.84kB
$ docker image rm -f 47b
Error response from daemon: conflict: unable to delete 47b19964fb50 (cannot be forced) - image is being used by running container 047c08aa64a4
$ docker container stop hopeful_kare
hopeful_kare
$ docker image rm 47b
Error response from daemon: conflict: unable to delete 47b19964fb50 (cannot be forced) - image is being used by running container 047c08aa64a4
$ docker image rm -f 47b
Untagged: ubuntu:latest
Untagged: ubuntu@sha256:7a47ccc3bbe8a451b500d2b53104868b46d60ee8f5b35a24b41a86077c650210
Deleted: sha256:47b19964fb500f3158ae57f20d16d8784cc4af37c52c49d3b4f5bc5eede49541
$ docker image ls -a
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
hello-world         latest              fce289e99eb9        6 weeks ago         1.84kB
myhello             latest              fce289e99eb9        6 weeks ago         1.84kB
```

当删除的镜像文件有容器正处于 **Up状态** 时，需要先停止与之对应的容器，才能进行删除操作。对于处于 **Exited状态** 的容器对应的镜像文件也无法删除，需要使用 **-f** 参数强制删除，或者在将容器删除后再删除对应的镜像文件。

对于一些遗留下来的镜像文件，或者是一些未被使用过的镜像文件，可以使用 **prune** 命令来进行删除，操作如下：`docker image prune`。

### 删除所有的镜像

可以使用组合命令实现，**ls -q** 列出所有的镜像文件ID，再删除对应的镜像，如果镜像已经创建了容器在运行，需要先删除容器再删除镜像。

```shell
$ docker image rm -f $(docker image ls -aq)
Untagged: haproxy:latest
Untagged: haproxy@sha256:32ac3731d6ba43006a7e00a064d2687d790d4e2420e18be197f440c4baec8f8d
...
```

### 创建镜像

使用 **build** 选项可以根据 **Dockerfile** 描述的方式来创建目标镜像。

```shell
$ cat Dockerfile
FROM python:3.7.2-alpine3.9

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache bash expect gcc musl-dev zeromq-dev \
    && mkdir -p ~/.pip \
    && echo '[global]' > ~/.pip/pip.conf \
    && echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.pip/pip.conf \
    && pip install jupyter

EXPOSE 8888

# 构造镜像
$ docker image build -t my_jupyter .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM python:3.7.2-alpine3.9
3.7.2-alpine3.9: Pulling from library/python
6c40cc604d8e: Already exists 
eb28c72fd5c9: Pull complete 
...
Step 4/4 : CMD jupyter-notebook --ip 0.0.0.0 --port 8888 --allow-root --no-browser
 ---> Running in ba5b3e571487
Removing intermediate container ba5b3e571487
 ---> e97e3e81d0e1
Successfully built e97e3e81d0e1
Successfully tagged my_jupyter:latest

# 查看镜像
$ docker image ls 
REPOSITORY          TAG                  IMAGE ID            CREATED             SIZE
my_jupyter          latest               e97e3e81d0e1        3 minutes ago       298MB
```

`-t` 参数是指定镜像的tag，`.` 表示的是Dockerfile的上下文，在构建时，客户端的docker会将该路径下的所有文件发送到docker服务器！**所以，尽量不要把与构建镜像无关的大文件放在上下文中**！

### 存出和载入镜像

使用 **save** 选项来导出目标镜像，使用 **load** 选项来导入镜像。

```shell
# 导出到本地归档文件中
$ docker image save -o my_jupyer.tar my_jupyter:latest 
$ ll
总用量 301680
drwxrwxr-x  2 xiaohui xiaohui      4096 3月  20 17:08 ./
drwxrwxr-x 15 xiaohui xiaohui      4096 3月   8 10:30 ../
-rw-rw-r--  1 xiaohui xiaohui       446 2月  22 12:01 Dockerfile
-rw-------  1 xiaohui xiaohui 308901376 3月  20 17:08 my_jupyer.tar

# 删除目标镜像
$ docker image rm my_jupyter:latest 
Untagged: my_jupyter:latest
Deleted: sha256:e97e3e81d0e122dafae9dce5137ec95a0d21984b502fa09756e64061b33767e2
Deleted: sha256:3b45659b7dc7e7225e0e00efb689fceb125fa00bf2ef902ff2efd038e1f85074
Deleted: sha256:77c4c2c997fb44fde0b075b6a16a059b156a883f9cbae817d09018cfaa01c822
Deleted: sha256:6af3924c282740de20ba84154d9875058bcfd96dbd73bdc1587c13ea0e1d4cdd
$ docker image ls
REPOSITORY          TAG                  IMAGE ID            CREATED             SIZE

# 导入目标镜像
$ docker image load -i ./my_jupyer.tar 
c3bc0525710f: Loading layer [==================================================>]  218.4MB/218.4MB
Loaded image: my_jupyter:latest
$ docker image ls
REPOSITORY          TAG                  IMAGE ID            CREATED             SIZE
my_jupyter          latest               e97e3e81d0e1        6 minutes ago       298MB
```

## 容器

**容器** 是Docker的另一个核心概念，可以把它想象成 **可执行程序的进程实例**。

与容器相关的命令如下：

```shell
Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  inspect     Display detailed information on one or more containers
  kill        Kill one or more running containers
  logs        Fetch the logs of a container
  ls          List containers
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  prune       Remove all stopped containers
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  run         Run a command in a new container
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes
```

### 启动容器

启动容器有几种方式，可以 **create** 完了之后 **start**，也可以直接 **run**。

**create** 和 **run** 的命令参数基本一致，只挑一些比较常用的参数进行操作，后面如果遇到有用的及时更新。

#### create 后 start

通过 **create命令** 能够创建一个新的容器。

```shell
$ docker create -it --name myubuntutest ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
6cf436f81810: Pull complete 
987088a85b96: Pull complete 
b4624b3efe06: Pull complete 
d42beb8ded59: Pull complete 
Digest: sha256:7a47ccc3bbe8a451b500d2b53104868b46d60ee8f5b35a24b41a86077c650210
Status: Downloaded newer image for ubuntu:latest
ebe4758fcc37d7cc12f79cb878e3ec259091827631aca1ab3fe005d5ce14f629

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
ebe4758fcc37        ubuntu              "bash"                   3 minutes ago       Created                                      myubuntutest
```

同 **run命令** 一样，当本地不存在目标镜像文件时，会从注册服务器下载目标镜像。创建完后可以看到容器列表中已经存在了目标容器，状态为 **Created**，表示为已经创建好了。

使用 **start** 命令启动容器。

```shell
$ docker container start myubuntutest
myubuntutest

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
ebe4758fcc37        ubuntu              "bash"                   11 minutes ago      Up 20 seconds                                myubuntutest
```

可以看见目标容器的状态已由 **Create --> Up**。

#### run

还是比较喜欢 **run命令**。与 **Create** 不一样的地方在于，**run** 命令可以使用 **-d参数** 指定容器后台运行。

当使用 **run命令** 进行容器的创建时，Docker会在后台做下列操作：

- 检查本地是否存在指定的镜像，不存在则从共有的仓库下载；
- 利用镜像创建一个容器，并启动该容器；
- 分配一个文件系统给容器，并在只读镜像层外面挂载一层可读可写层；
- 从宿主主机配置的网桥接口中桥接一个虚拟的接口到容器中去；
- 从网桥的地址池配置一个IP地址给容器；
- 执行用户指定的应用程序；
- 执行完毕后容器自动终止。

```shell
$ docker container run -dit --name mynginx -p 8000:80 nginx
ebe39517d80df1a686f75504776dd807fcfaaba5a4cf0da8b43fe8dde10fea4d

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
ebe39517d80d        nginx               "nginx -g 'daemon of…"   2 minutes ago       Up 2 minutes        0.0.0.0:8000->80/tcp     mynginx

$ curl -s 192.168.2.68:8000
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

如上面的例子，使用了 **-d** 参数使得nginx服务器再后台启动，并设置了宿主主机与容器的端口映射，通过宿主主机的端口便能访问到nginx容器。

使用 **logs命令** 可以在宿主机上查看容器的运行日志信息。

```shell
$ docker container logs -f mynginx
192.168.2.53 - - [18/Feb/2019:08:50:30 +0000] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36" "-"
2019/02/18 08:50:31 [error] 7#7: *1 open() "/usr/share/nginx/html/favicon.ico" failed (2: No such file or directory), client: 192.168.2.53, server: localhost, request: "GET /favicon.ico HTTP/1.1", host: "192.168.2.68:8000", referrer: "http://192.168.2.68:8000/"
192.168.2.53 - - [18/Feb/2019:08:50:31 +0000] "GET /favicon.ico HTTP/1.1" 404 555 "http://192.168.2.68:8000/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36" "-"
192.168.2.68 - - [18/Feb/2019:08:51:10 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.58.0" "-"
192.168.2.53 - - [18/Feb/2019:09:12:34 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36" "-"
```

### 容器状态查看

容器状态查看主要由下面的几个命令：**inspect**、**top**、**stats**。

使用 **inspect** 命令可以查看单个或多个容器的详细信息。和上面介绍的image中的inspect命令使用方法一样。

```shell
$ docker container inspect  mynginx 
[
    {
        "Id": "ebe39517d80df1a686f75504776dd807fcfaaba5a4cf0da8b43fe8dde10fea4d",
        "Created": "2019-02-18T08:50:20.509885669Z",
        "Path": "nginx",
        "Args": [
            "-g",
            "daemon off;"
        ],
        "State": {
            "Status": "running",
            "Running": true,
...
```

使用 **top命令** 可以查看容器内运行的进程状态。

```shell
$ docker container top mynginx 
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                11998               11974               0                   16:50               pts/0               00:00:00            nginx: master process nginx -g daemon off;
systemd+            12078               11998               0                   16:50               pts/0               00:00:00            nginx: worker process
```

使用 **stats命令** 可以查看容器的信息，包括容器ID、名字、CPU、内存使用、存储、网络的统计信息。

```shell
$ docker container stats mynginx
CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
ebe39517d80d        mynginx             0.00%               3.207MiB / 7.767GiB   0.04%               23.5kB / 3.98kB     295kB / 0B          2
```

shell中会一直刷新容器的统计信息。

### 终止容器

使用 **pause命令** 可以暂停容器的运行状态，暂停并不会杀死容器，使用 **unpause命令** 可以恢复已暂停的容器。

```shell
$ docker container pause mynginx
mynginx
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                      PORTS                    NAMES
ebe39517d80d        nginx               "nginx -g 'daemon of…"   24 minutes ago      Up 24 minutes (Paused)      0.0.0.0:8000->80/tcp     mynginx
```

暂停后，容器状态变为 **Up(pause)**,再访问对应的网址将不能访问，**unpause** 后才能恢复。

```shell
$ docker container unpause mynginx
mynginx
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS                    NAMES
ebe39517d80d        nginx               "nginx -g 'daemon of…"   27 minutes ago      Up 27 minutes              0.0.0.0:8000->80/tcp     mynginx
```

停止容器可以使用 **stop命令**，也可以使用 **kill命令**。不同之处在于 **stop命令** 向容器发送的 **SIGTERM信号**，**kill命令** 则发送的是 **SIGKILL信号**。

```shell
$ docker container stop mynginx
mynginx

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS                    NAMES
ebe39517d80d        nginx               "nginx -g 'daemon of…"   32 minutes ago      Exited (0) 2 seconds ago                            mynginx
```

### 删除容器

使用 **rm命令** 可以进行容器的删除操作，注意的是，如果容器处于运行状态，得先停止容器，再删除，或者使用 **-f参数**，强制删除。

```shell
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
2d0518e87654        nginx               "nginx -g 'daemon of…"   8 seconds ago       Up 7 seconds        0.0.0.0:8000->80/tcp     mynginx

$ docker container rm mynginx
Error response from daemon: You cannot remove a running container 2d0518e87654cd1be2cd48a935ea0db3b471a679cdd908a766eaf8dddf28457a. Stop the container before attempting removal or force remove

$ docker container rm -f mynginx
mynginx

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
```

对于已经处于 **Exited状态** 的容器，可以使用 **prune命令** 将它们全部删除。

### 删除所有容器

和删除所有镜像的使用类似。

```shell
$ docker container  rm -f $(docker container ls -aq)
2573c41a6f71
50d74dbb60ed
...
```

### 容器attach和exec

容器启动后，如果想要进入容器进行一些操作的话，可以使用 **attach命令**，也可以使用 **exec命令**。

两者的区别在于，**attach命令** 会接管容器的输入与输出，当退出容器操作时，容器也会退出，有时候会造成不必要的麻烦

```shell
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
1c386715611a        nginx               "nginx -g 'daemon of…"   7 seconds ago       Up 6 seconds        0.0.0.0:8000->80/tcp     mynginx

$ docker container attach mynginx
192.168.2.53 - - [18/Feb/2019:09:31:12 +0000] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36" "-"

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS                    NAMES
1c386715611a        nginx               "nginx -g 'daemon of…"   37 seconds ago      Exited (0) 7 seconds ago                            mynginx
```

建议是使用 **exec命令**。

```shell
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
c89cbdf1287b        nginx               "nginx -g 'daemon of…"   3 seconds ago       Up 3 seconds        0.0.0.0:8000->80/tcp     mynginx

$ docker container exec -it mynginx bash
root@c89cbdf1287b:/# ls
bin  boot  dev	etc  home  lib	lib64  media  mnt  opt	proc  root  run  sbin  srv  sys  tmp  usr  var
root@c89cbdf1287b:/# exit
exit

$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
c89cbdf1287b        nginx               "nginx -g 'daemon of…"   34 seconds ago      Up 33 seconds       0.0.0.0:8000->80/tcp     mynginx
```

### 导入导出容器

// todo

### 端口映射与容器互联

**端口映射** 大多情况下指的是宿主机器和容器间的端口映射，**容器互联** 指的是荣期间的操作。

#### 端口映射

与宿主主机的端口映射，可以使用 **-P(大写)** 随机指定宿主主机上的一个端口。

```shell
$ docker container run -dit --name mynginx -P nginx
2db1ec7c5231c093c1894f55a7aed91e45f298391fa4960e1cfaa74bce471936
$ docker container ls -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
2db1ec7c5231        nginx               "nginx -g 'daemon of…"   3 seconds ago       Up 1 second         0.0.0.0:32768->80/tcp    mynginx
```

使用 **-p(小写)** 根据后续的参数根据指定端口进行映射。支持的格式有：

- **IP:HostPort:ContainerPort** - 指定宿主主机的IP和端口，映射到容器的端口。
- **IP::ContainerPort** - 指定宿主主机的IP，端口随机指定，映射到容器的端口。
- **HostPort:CopntainerPort** - 指定宿主主机 **0.0.0.0:HostPort**，映射到容器的端口。

#### 容器互联

容器间互联可以使用 **--link参数**，使用方式为 `--link ContainerName:Alias`。

这么做的好处是，避免了容器端口在外部网络的暴露。**Docker相当于是在两个容器之间创建了一个虚拟通道，而不用映射它们的端口到宿主主机上。在启动时容器并没有使用-P或-p参数指定端口，避免暴露容器端口到外部网络**。

```shell
$ docker container run -dit --name redis_server redis
5ac6fcefecc3b769edddefd4504aacdd2b36954c1f4de75147ab115b4476d0b9
$ docker container ls 
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
5ac6fcefecc3        redis               "docker-entrypoint.s…"   5 seconds ago       Up 4 seconds        6379/tcp                 redis_server

$ docker exec -it redis_server bash
root@5ac6fcefecc3:/data# redis-cli 
127.0.0.1:6379> get hello
(nil)
127.0.0.1:6379> set hello test
OK
127.0.0.1:6379> get hello
"test"

$ docker container run -it --name redis_client --link redis_server:redis_server redis bash
root@1723b4be0de9:/data# cat /etc/hosts
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
ff00::0	ip6-mcastprefix
ff02::1	ip6-allnodes
ff02::2	ip6-allrouters
172.17.0.8	redis_server 5ac6fcefecc3       # redis_server 对应的为上面设置的redis容器
172.17.0.9	1723b4be0de9
root@1723b4be0de9:/data# redis-cli -h redis_server -p 6379  # 通过-h参数连接远程的redis服务器
redis_server:6379> get hello
"test"
```

// todo: 跨主机的容器通信

### 数据管理

容器间的数据管理主要有两种方式：

- **数据卷(Data Volumes)**: 容器内数据直接映射到宿主主机环境，不同容器间通过宿主主机的本地文件进行交互。
- **数据卷容器(Data Volumes Containers)**: 将数据保存在特定的容器中，通过该容器进行不同容器间的数据交互。

#### 数据卷

数据卷的方式类似于linux下的硬盘挂载(mount)功能：

- 数据卷可以在容器间共享和重用，容器间数据传递将变得高效和方便；
- 对数据卷内数据的修改立马生效，无论是容器内操作还是本地操作；
- 对数据卷的更新不会影响镜像，解耦开应用和数据；
- 卷会一直存在，直到没有容器使用，可以安全的卸载数据卷。

有些容器在创建时会在宿主主机上生成一个数据卷文件夹。这时，可以查找这些数据卷，将文件放置在这个文件夹内即可。其他容器可以挂载这个数据卷实现数据交互。

一般情况下，还是在宿主主机上新建一个数据卷比较合适。

```shell
# 创建数据卷
root@ubuntu:~# cd /var/lib/docker/volumes/
root@ubuntu:/var/lib/docker/volumes# ls
root@ubuntu:/var/lib/docker/volumes# docker volume create test
test
root@ubuntu:/var/lib/docker/volumes# ls
test

# 绑定数据卷
root@ubuntu:/var/lib/docker/volumes# docker container run -dit --name volume_1 --mount source=test,destination=/volume_test nginx
434b5bc52e92b0283171c245539a31fe0cffc961d8faef519308805771a1f875
root@ubuntu:/var/lib/docker/volumes# docker container inspect volume_1
...
 "Mounts": [
            {
                "Type": "volume",
                "Name": "test",
                "Source": "/var/lib/docker/volumes/test/_data",     # 宿主主机数据卷位置
                "Destination": "/volume_test",      # 目标容器的绑定的文件夹
                "Driver": "local",
                "Mode": "z",
                "RW": true,
                "Propagation": ""
            }
        ],
...

# 进入容器查看
root@ubuntu:/var/lib/docker/volumes# docker exec -it volume_1 bash
root@434b5bc52e92:/# ls
bin  boot  dev	etc  home  lib	lib64  media  mnt  opt	proc  root  run  sbin  srv  sys  tmp  usr  var	volume_test
root@434b5bc52e92:/# cd volume_test/
root@434b5bc52e92:/volume_test# ls
```

使用同样的方式在另一个容器中绑定数据卷，便可实现不同容器间的数据交互。

```shell
# 另一个容器绑定相同的数据卷
root@ubuntu:/var/lib/docker/volumes# docker container run -dit --name volume_2 --mount source=test,destination=/volume_test2 nginx
4d9cda1623c2661abfcc02431e6b15685f5ea9825b2f45f9ad0705edf4045250
root@ubuntu:/var/lib/docker/volumes# docker exec -it volume_2 bash
root@4d9cda1623c2:/# cd volume_test2/
root@4d9cda1623c2:/volume_test2# echo "hello" > volume.txt
root@4d9cda1623c2:/volume_test2# cat volume.txt 
hello

# 在宿主主机和另一个容器中打开共享的文件
root@ubuntu:/var/lib/docker/volumes# cd test/_data/
root@ubuntu:/var/lib/docker/volumes/test/_data# ls
volume.txt
root@ubuntu:/var/lib/docker/volumes/test/_data# cat volume.txt 
hello
root@ubuntu:/var/lib/docker/volumes/test/_data# docker exec -it volume_1 bash
root@434b5bc52e92:/# cd volume_test/
root@434b5bc52e92:/volume_test# cat volume.txt 
hello
```

容器绑定数据卷的方式，之前大多使用的是 **-v,--volume**，现在官方推荐的是使用 **--mount参数**。

**--mount参数** 还有其他的参数可以配置，具体请看[官网介绍](https://docs.docker.com/storage/volumes/)。

#### 数据卷容器

**数据卷容器** 需要将一个容器作为数据卷存在，其他的需要数据交互的容器只需都绑定到数据卷容器上即可。

其实，这种做法和数据卷的做法是一样的，不同的是，**数据卷的做法是自己指定了数据卷**。而数据卷容器的做法是，在创建数据卷容器时，会在 **/var/lib/docker/volumes/xxxx/_data** 目录下生成一个数据卷，其他容器绑定的数据卷其实是这个目录下的数据卷！

```shell
# 创建数据卷容器
$ docker container run -it --name dbdata --mount destination=/dbdata ubuntu
root@3d34b551b6c6:/# ls
bin  boot  dbdata  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@3d34b551b6c6:/# cd dbdata/
root@3d34b551b6c6:/dbdata# touch test

# 在宿主主机上查看对应的数据卷
root@ubuntu:~# cd /var/lib/docker/volumes/6678cb75d51cf456b58d5b918bfe8ea21261cfb4307f73c120266b83162e6ba4/_data/
root@ubuntu:/var/lib/docker/volumes/6678cb75d51cf456b58d5b918bfe8ea21261cfb4307f73c120266b83162e6ba4/_data# ls
test

# 1号容器绑定数据卷容器
root@ubuntu:~# docker container run -it --volumes-from dbdata --name db1 ubuntu
root@9ea683e5caec:/# ls
bin  boot  dbdata  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@9ea683e5caec:/# cd dbdata/
root@9ea683e5caec:/dbdata# ls  
test
root@9ea683e5caec:/dbdata# cat test 
root@9ea683e5caec:/dbdata# echo "hello" > test

# 2号容器绑定数据卷
root@ubuntu:~# docker container run -it --volumes-from dbdata --name db2 ubuntu
root@b831ae28c94b:/# cat dbdata/test 
hello
root@b831ae28c94b:/# echo "ubuntu" >> dbdata/test

# 宿主主机查看更改
root@ubuntu:/var/lib/docker/volumes/6678cb75d51cf456b58d5b918bfe8ea21261cfb4307f73c120266b83162e6ba4/_data# cat test 
hello
ubuntu
```

## 参考

- [Use volumes](https://docs.docker.com/storage/volumes/)