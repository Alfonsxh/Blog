---
title: "图解密码技术 - PGP"
date: 2018-08-18 10:52:18
lastmod: 2018-08-18 10:52:18
draft: false
keywords: ["Books", "图解密码技术"]
description: "PGP"
tags: ["Books", "图解密码技术"]
categories: ["Books", "图解密码技术"]
author: "Alfons"
---

`PGP(Pretty Good Privacy)`是一款密码软件，里面包含了多种加密算法。本章重点介绍的是多种密码技术的组合。

<!--more-->

## 加密与解密

加密的过程：

- 生成和加密会话密钥
  - (1) 用伪随机数生成器生成会话密钥(对称密码)
  - (2) 用公钥密码(接收者的公钥，非对称密码)加密会话密钥
- 压缩和加密消息
  - (3) 压缩消息
  - (4) 使用(1)中的会话密钥加密压缩后的消息
  - (5) 将(2)中加密后的会话密钥和(4)中加密后的压缩的消息合并
  - (6) 将(5)中的结果转换为文本数据

![13-Mixed-Cipher-Encrypt](/images/Books/ProfessionBooks/图解密码技术/13-Mixed-Cipher-Encrypt.png)

解密过程：

- 解密私钥
  - (1) 接收者输入解密口令
  - (2) 口令加盐后经过单向散列函数计算出私钥的解密密钥
  - (3) 通过(2)中的私钥解密密钥解密私钥
- 解密会话密钥
  - (4) 将报文转化为二进制数据
  - (5) 将二进制数据分解成两部分：加密的会话密钥和加密的压缩了的消息
  - (6) 使用(3)中的私钥解密会话密钥
- 解密和解压缩消息
  - (7) 使用(6)中得到的会话密钥解密(5)中分解后的加密的压缩了的消息
  - (8) 对(7)中的消息解压缩
  - (9) 得到原始消息  

![13-Mixed-Cipher-Decrypt](/images/Books/ProfessionBooks/图解密码技术/13-Mixed-Cipher-Decrypt.png)

加密解密过程中的数据流如下所示：

![13-Mixed-Data](/images/Books/ProfessionBooks/图解密码技术/13-Mixed-Data.png)

## 生成和验证数字签名

`PGP`中生成和验证数字签名的过程类似于上节加密解密的过程，不过过程刚好相反。

生成数字签名：

- 解密私钥
  - (1) 接收者输入解密口令
  - (2) 口令加盐后经过单向散列函数计算出私钥的解密密钥
  - (3) 通过(2)中的私钥解密密钥解密私钥
- 生成数字签名
  - (4) 消息经过单向散列函数处理生成散列值
  - (5) 由(4)计算出的散列值经过(3)中的私钥进行签名
  - (6) 将(5)中得到的签名和消息进行拼接
  - (7) 压缩拼接后的消息
  - (8) 数据进行转化
  - (9) 产生报文数据发送

![13-Generate-Signature](/images/Books/ProfessionBooks/图解密码技术/13-Generate-Signature.png)

验证数字签名：

- 恢复发送者发送的散列值
  - (1) 将报文数据转换成二进制数据
  - (2) 解压缩
  - (3) 将解压后的数据分解成签名和消息
  - (4) 使用发送者的公钥解密签名，得到消息的散列值
- 对比散列值
  - (5) 将(3)分解得到的消息经过单向散列函数计算散列值
  - (6) 对比(4)和(5)的散列值
  - (7) 验证(6)中的结果
  - (8) 如果验证通过，则得到原始消息

![13-Check-Signature](/images/Books/ProfessionBooks/图解密码技术/13-Check-Signature.png)

## 生成数字签名并加密以及解密并验证数字签名

此过程主要结合了上面的加密和签名流程。

加密并签名过程：

![13-PGP-Together-Encrypt](/images/Books/ProfessionBooks/图解密码技术/13-PGP-Together-Encrypt.png)

解密并验证签名的过程：

![13-PGP-Together-Decrypt](/images/Books/ProfessionBooks/图解密码技术/13-PGP-Together-Decrypt.png)