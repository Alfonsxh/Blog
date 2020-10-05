---
title: "Gost科学上网"
date: 2022-09-03T11:52:06+08:00
lastmod: 2022-09-03T11:52:06+08:00
draft: false
keywords: ["科学上网", "Gost", "VPN"]
description: "使用 Gost + https 方式科学上网"
tags: ["科学上网"]                      # 归档 
categories: []                # 分类
author: "Alfons"

comment: true                 # 是否显示评论
---

在一个月内经历两次 VPS 被墙后，痛定思痛，决定放弃 Shadowsocks 的连接方式，转向 `Gost + Https` 的方式。

<!--more-->

## Gost

Gost 是个隧道程序，不过，它强大的地方在于，支持多种协议。这次搭建的梯子主要用到了它的 HTTPS 方式。

## 使用

和Shadowsocks一样，搭建Gost梯子，同样需要服务端和客户端。这里的使用方式我主要参考的是这篇[文章](https://haoel.github.io/)，文章中有些比较模糊的地方，我会尝试说清楚。

### 服务端搭建

服务端搭建，由于使用了 HTTPS 的方式，所以最好是按照标准流程，将服务端完全伪装成一个 网站。

这里需要的内容包括：

- VPS服务器
- 域名
- 证书

我这里的 **VPS服务器** 使用之前的机器，重新安装操作系统 Ubuntu。Centos 系统在注册证书时，需要使用 **certbot** 程序，会比较麻烦。

安装步骤可以直接使用脚本完成，首先 **安装 TCP BBR 拥塞控制算法**、**安装 Docker 服务程序**。

```shell
root@www:/home# ./install.sh

菜单选项

1) 安装 TCP BBR 拥塞控制算法
2) 安装 Docker 服务程序
3) 创建 SSL 证书
4) 安装 Gost HTTP/2 代理服务
5) 安装 ShadowSocks 代理服务
6) 安装 VPN/L2TP 服务
7) 安装 Brook 代理服务
8) 创建证书更新 CronJob
9) 退出
```

安装 SSL 证书时，需要域名，可以去 [Godaddy](https://www.godaddy.com/zh-sg) 上进行购买。

域名购买后，需要将域名和VPS服务器的IP进行绑定，具体步骤如下： 我的域名 -> 域名设置 -> DNS管理 -> DNS记录 -> 添加 VPS IP 地址

![域名设置](/images/杂七杂八/科学上网/域名设置.png)

域名绑定IP后，可以继续在VPS上进入下一步操作，生成SSL证书。直接使用上面安装脚本的方式，或者直接使用命令。

- 安装 certbot 程序

    ```shell
    apt install snapd
    snap install certbot --classic
    ln -s /snap/bin//certbot /bin/certbot
    ```

- 生成 SSL 证书

    ```shell
    certbot certonly -d "your_domain.com" -d "*.your_domain.com" --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
    ```

> PS:
> 生成 SSL 证书时，需要仔细观察命令的输出提示，按照提示进行操作，一般不会有问题。
> 另外，DNS设置会有一定的时延，按照提示进行验证后，再继续下一步操作

完成SSL证书操作后，就会在指定的目录下生成网站需要的证书信息：

```shell
ll /etc/letsencrypt/live/your_domain.com/
total 12
drwxr-xr-x 2 root root 4096 Sep  2 03:27 ./
drwx------ 3 root root 4096 Sep  2 03:27 ../
lrwxrwxrwx 1 root root   36 Sep  2 03:27 cert.pem -> ../../archive/your_domain.com/cert1.pem
lrwxrwxrwx 1 root root   37 Sep  2 03:27 chain.pem -> ../../archive/your_domain.com/chain1.pem
lrwxrwxrwx 1 root root   41 Sep  2 03:27 fullchain.pem -> ../../archive/your_domain.com/fullchain1.pem
lrwxrwxrwx 1 root root   39 Sep  2 03:27 privkey.pem -> ../../archive/your_domain.com/privkey1.pem
-rw-r--r-- 1 root root  692 Sep  2 03:27 README
```

下一步，就可以进行 Gost 程序启动了。Gost 提供了非常简单的docker部署方式。

```shell
#!/bin/bash

DOMAIN="your_domain.com"
USER="your_domain"
PASS="xxxxxxxxxx"
PORT=443

BIND_IP=0.0.0.0
CERT_DIR=/etc/letsencrypt
CERT=${CERT_DIR}/live/${DOMAIN}/fullchain.pem
KEY=${CERT_DIR}/live/${DOMAIN}/privkey.pem

docker rm -f gost
docker run -d --restart=always --name gost \
    -v ${CERT_DIR}:${CERT_DIR}:ro \
    --net=host ginuerzh/gost \
    -L "http2://${USER}:${PASS}@${BIND_IP}:${PORT}?cert=${CERT}&key=${KEY}&probe_resist=code:404&knock=www.google.com"
```

在服务端，我们只需要使用 `-L` 参数，建立本地的代理便可。协议选择为 **http2**。

至此，服务端的基本操作已经完成。SSL证书需要定期进行更新，脚本也提供了选项进行自动化的更新操作。

### 客户端使用

Gost 是一个隧道，它只管理路上的事情，不管你具体如何使用。由于习惯了 Shadowsocks 客户端，因此下面的内容均以 Shadowsocks 的方式进行。

客户端的核心在于：通过Gost在客户端建立与服务端的通道、在客户端建立 Shadowsocks 代理、通过 Shadowsocks 客户端连接本地的 ss 通道。

```shell
┌─────────────┐  ┌─────────────┐            ┌─────────────┐
│ ShadowSocks │  │             │            │             │
│    Client   ├──► Gost Client ├────────────► Gost Server │
│ (PAC Auto)  │  │             │            │             │
└─────────────┘  └─────────────┘            └─────────────┘
```

#### Macos

Macos 系统上， 一直使用的是 [ShadowsocksX-NG](https://github.com/shadowsocks/ShadowsocksX-NG) 程序，改为 Gost 后，需要在本机上通过 **launchctl** 的方式添加定时任务，让 Gost 程序在启动时，自动的给拉起来。操作步骤如下：

- 安装 gost 程序：`brew install gost`
- 新建文件 `/Library/LaunchDaemons/gost.plist`，添加下面的内容

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>gost</string>
        <key>Disabled</key>
        <false/>
        <key>KeepAlive</key>
        <true/>
        <key>ProcessType</key>
        <string>Background</string>
        <key>ProgramArguments</key>
        <array>
        <string>/usr/local/bin/gost</string>
        <string>-L</string>
        <string>ss://aes-128-gcm:123456@127.0.0.1:1080</string>
        <string>-F</string>
        <string>https://your_user:your_passwd@your_domain.com:443</string>
        </array>
        <key>UserName</key>
        <string>root</string>
        <key>GroupName</key>
        <string>wheel</string>
        <key>StandardOutPath</key>
        <string>/tmp/gost.log</string>
        <key>StandardErrorPath</key>
        <string>/tmp/gost.err.log</string>
    </dict>
    </plist>
    ```

- 加载启动

    ```shell
    sudo launchctl load -w /Library/LaunchDaemons/gost.plist
    ```

- 使用 ShadowsocksX-NG 建立本地连接。使用上面配置中的参数，`ss://aes-128-gcm:123456@127.0.0.1:1080`

#### Win

Win 上，使用的是 [shadowsocks-windows](https://github.com/shadowsocks/shadowsocks-windows)。和Macos类似，解决方案，也是 **自启动 Gost 后台程序** + **shadowsocks 本地代理**。

- 下载 Gost 程序 -> [gost-releases](https://github.com/ginuerzh/gost/releases)
- 网上在 win 上添加 自启动服务的方式很多，我这里使用的是 **组策略** 的方式。（可能win的不同版本会限制这种方式，如果不行，可以尝试其他方式）
- **shadowsocks-windows** 连接本地的 shadowsocks 代理

#### iOS

iOS 的设置比较简单，直接使用 [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118)，里面有 https 的选项，按照步骤新建完之后便可。

至于具体怎么获取 shadowrocket 程序，网上有很多方法。

#### Android

Android 有提供 [shadowsocks-android](https://github.com/shadowsocks/shadowsocks-android) 程序，但是它不支持 Gost 方式的调用，因此，需要使用 Gost插件([ShadowsocksGostPlugin](https://github.com/xausky/ShadowsocksGostPlugin))的方式进行。

**ShadowsocksGostPlugin** 插件有些坑，使用说明异常的不清晰，甚至起了干扰。总结了下操作：

- 下载插件 [ShadowsocksGostPlugin-app-release.apk](https://github.com/xausky/ShadowsocksGostPlugin/releases/download/v2.11.0/app-release.apk)
- **shadowsocks-android** 上新建连接，注意点如下：
  - 服务器 - 服务端的域名
  - 远程端口 - 服务端的端口
  - 密码 - **gost**
  - 加密方式 - **RC4-MD5**
  - 插件 - 选择 **ShadowsocksGostPlugin**
  - 插件配置 - `-F https://your_user:your-passwd@#SS_HOST:#SS_PORT`

> PS
> 插件配置 配置中的 **#SS_HOST**、**#SS_PORT** 不用修改！！！
> 插件配置 配置中的 **#SS_HOST**、**#SS_PORT** 不用修改！！！
> 插件配置 配置中的 **#SS_HOST**、**#SS_PORT** 不用修改！！！

## 参考

- [Gost](https://github.com/ginuerzh/gost)
- [科学上网](https://haoel.github.io/)
- [一键安装脚本](https://github.com/haoel/haoel.github.io/blob/master/scripts/install.ubuntu.18.04.sh)
- [ShadowsocksX-NG](https://github.com/shadowsocks/ShadowsocksX-NG)
- [shadowsocks-windows](https://github.com/shadowsocks/shadowsocks-windows)
- [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118)
- [shadowsocks-android](https://github.com/shadowsocks/shadowsocks-android)
- [ShadowsocksGostPlugin-app-release.apk](https://github.com/xausky/ShadowsocksGostPlugin/releases/download/v2.11.0/app-release.apk)
