---
title: "图解密码技术 - SSL/TLS"
date: 2018-08-18 10:52:18
lastmod: 2018-08-18 11:07:34
draft: true
keywords: ["Books", "图解密码技术"]
description: "SSL/TLS"
tags: ["Books", "图解密码技术"]
categories: ["Books", "图解密码技术"]
author: "Alfons"
---

`传输层安全性协议(Transport Layer Security,TLS)`以及其前身`安全套接层(Secure Socket Layer, SSL)`是一种安全协议，目的是为互联网通信，提供安全及数据完整性保障。

从技术上讲`TLS 1.0`与`SSL 3.0`差异很小，`TLS 1.0`可以说是`SSL 3.1`。

现在主要使用的是`TLS 1.2`版本，于2008年8月发表。

`TLS 1.3`版本于2018年8月发表。

<!--more-->

## 使用SSL/TLS进行通信

`TLS协议`由`TLS记录协议(TLS record protocol)`和`TLS握手协议(TLS handshake procotol)`叠加而成的。

底层的`TLS记录协议(TLS record protocol)`负责对数据进行加密，上层的`TLS握手协议(TLS handshake procotol)`负责加密意外的其他操作。

![14-TLS-Protocol](/images/Books/ProfessionBooks/图解密码技术/14-TLS-Protocol.png)

### TLS记录协议


### TLS握手协议

#### 握手协议

#### 密码规格变更协议

#### 警告协议

#### 应用数据协议