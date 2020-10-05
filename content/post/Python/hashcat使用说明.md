---
title: "Hashcat使用说明"
date: 2018-09-28 21:51:01
lastmod: 2018-09-28 22:01:27
draft: false
keywords: ["Python", "hashcat"]
description: "Hashcat使用说明"
tags: ["Python", "hashcat"]
categories: ["Python", "hashcat"]
author: "Alfons"
---

`hashcat`是目前世界上最快的密码破解工具，能够破译众多类型的密码，可以使用CPU，也可以使用GPU作为计算单元。

<!--more-->

## 破解基础命令

| 选项                | 描述                                                           | 使用                     |
| :------------------ | :------------------------------------------------------------- | :----------------------- |
| -m                  | 设置待破解文件类型，WPA/WPA2类型为2500                         | -m 2500                  |
| -a                  | 破解模式                                                       |
| --runtime           | 指定程序运行时间X，单位秒                                      | --runtime=X              |
| --session           | 指定一个特殊的hashcat会话名称                                  | --session=mysession      |
| --restore           | 从restore文件中恢复会话状态                                    |
| --restore-disable   | 会话时不使用restore文件                                        |
| --restore-file-path | 指定特殊的restore文件路径，默认路径在`.hashcat/session/`下     | --restore-file-path=path |
| --outfile           | 破解出的hash存放路径                                           | -o outfile.txt           |
| --show              | 展示破解文件中已破解的hash                                     |
| --left              | 展示破解文件中未破解出的hash                                   |
| --increment         | 设置自动变长模式开关，密码长度由用户指定，不能在字典破解模式下 |
| --increment-min     | 最短密码长度                                                   | --increment-min=8        |
| --increment-max     | 最长密码长度                                                   | --increment-max=13       |
| --cpu-affinity      | 使用CPU破解时，使用特定的CPU进行破解                           | --cpu-affinity=1,2       |
| --segment-size      | 使用字典破解时，字典在内存中的缓存大小，单位MB                 | --segment-size=1024      |
| --gpu-temp-abort    | 中断破解，当GPU达到此温度                                      | --gpu-temp-abort=100     |
| --skip              | 跳过字典前面 X 个密码                                          | --skip X                 |
| --limit             | 只使用字典前 X 个密码                                          | --limit X                |
| --status            | 设置自动刷新hashcat状态开关                                    |
| --status-timer      | 设置自动刷新时间 X                                             | --status-timer=X         |

hashcat启动方式为

```shell
hashcat -a 0 -m 2500 xxxx.hccapx dict1 dict2    # 字典破解模式，普通启动
hashcat -a 3 -m 2500 --session=xxxx xxxx.hccapx ?l?l?d?d?d?d?d?d   # 暴力破解模式以会话方式启动
hashcat --session xxxx --restore    # 以会话形式从restore文件中恢复
```

## 破解模式

hashcat的破解模式有5种。

```shell
0 | Straight      # 字典破解
1 | Combination   # 组合破解
3 | Brute-force   # 暴力破解
6 | Hybrid Wordlist + Mask  # 字典加掩码破解
7 | Hybrid Mask + Wordlist  # 掩码加字典破解
```

### Straight(字典破解 -a 0)

纯字典破解模式，遍历字典文件中的所有密码，对目标破解文件进行匹配。

```shell
hashcat -a 0 -m 2500 xxxx.hccapx dict
```

### Combination(组合破解 -a 1)

组合两个字典文件的内容进行破解，`只支持两个字典文件密码组合`！该模式会将dict1中的密码与dict2中的密码依次组合。

```shell
cat dict1
abc
def
gh

cat dict2
1234
23456

# 组合后需要破解的字典为
abc1234
abc23456
def1234
def23456
gh1234
gh23456

hashcat -a 1 -m 2500 xxxx.hccapx dict1 dict2
```

组合模式进行破解时，如果子字典内密码个数较多的话，整体的字典数量就十分巨大，造成破解时间成倍增加。

### Brute-force(暴力破解 -a 3)

hashcat中自定义了8种默认的字符集。

```shell
l | abcdefghijklmnopqrstuvwxyz      # 全体小写字母
u | ABCDEFGHIJKLMNOPQRSTUVWXYZ      # 全体大写字母
d | 0123456789          # 数字
h | 0123456789abcdef    # 十六进制数字
H | 0123456789ABCDEF    # 十六进制数字大写
s |  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~   # 符号
a | ?l?u?d?s        # 所有字符集
b | 0x00 - 0xff     # 0-255
```

同时也提供四个字符，让用户自定义符号使用。

```shell
 -1, --custom-charset1          | CS   | User-defined charset ?1                              | -1 ?l?d?u
 -2, --custom-charset2          | CS   | User-defined charset ?2                              | -2 ?l?d?s
 -3, --custom-charset3          | CS   | User-defined charset ?3                              |
 -4, --custom-charset4          | CS   | User-defined charset ?4                              |
```

使用时，组合不同的字符集，破译密码。

```shell
# 使用默认字符集
hashcat -a 3 -m 2500 xxxx.hccapx ?l?l?l?l?l?l?l?l  # 密码规则为8位小写字母的组合
hashcat -a 3 -m 2500 xxxx.hccapx ?l?l?l?l?d?d?d?d  # 密码规则为8位，4位小写字母+4位数字的组合

# 使用用户自定义字符集
hashcat -a 3 -m 2500 xxxx.hccapx -1 qwert -2 123456 ?1?1?1?1?2?2?2?2 # 前四位密码为qwert中的组合，后四位密码为12345数字的组合
```

### Hybrid Wordlist + Mask(字典加掩码破解 -a 6)

后两种破解方式结合了字典和规则，与`组合模式(-a 1)`十分类似。

```shell
# 假如使用的字典为dict
cat dict
admin
root
```

假设实际的明文密码为`adminer123456`，则使用的规则为`?l?l?d?d?d?d?d`，即可匹配到明文密码。

```shell
hashcat -a 6 -m 2500 xxxx.hccapx dict1 dict2 dict3 ?l?l?d?d?d?d?d
```

在这种模式下，可以使用多个字典和规则进行组合。

### Hybrid Mask + Wordlist(掩码加字典破解 -a 7)

与字典加掩码模式相反，掩码加字典破解是规则在前，字典在后。

```shell
hashcat -a 7 -m 2500 xxxx.hccapx ?l?l?d?d?d?d?d dict1 dict2 dict3
```

## Hashcat进阶

### pcap包转换为hccapx格式。

三种方式

- 使用cap2hccapx.bin
- 使用Aircrack-ng(1.3版本)的`-j`参数
- [在线](https://hashcat.net/cap2hccapx/)转换

### 显示已破解的密码。

已经破解出的密码，hashcat会默认保存在`.hashcat/hashcat.potfile`文件中，可以通过此文件查看已破解的密码。

![cat_potfile](/images/Python/hashcat使用说明/cat_potfile.jpg)

也可以通过`--show`命令查看特定握手包内破解出的AP的密码。也可以通过`--left`命令查看未破解出的密码。

```shell
$ hashcat -m 2500 helloworld.hccapx --show
c5b769d43cd2c3449c001cb3fd1a666a:0018e7b25200:9cd91730dc8e:helloworld:hello12345

$ hashcat -m 2500 helloworld.hccapx --left
60bdcbb80306cc99b5dd786334edad73:0018e7b25200:9cd91730dc8e:helloworld
c52577dde5a3539890c2393a3f7f8551:0018e7b25200:9cd91730dc8e:helloworld
2394e4c7311821872adc9a8c54503446:0018e7b25200:9cd91730dc8e:helloworld
cba153ab6ee3597e5512dae45ad0ef64:0018e7b25200:9cd91730dc8e:helloworld
812da0113e74622d154d7301679e0481:0018e7b25200:9cd91730dc8e:helloworld
517b035a3a1b1cc29d5abb27aea37b45:0018e7b25200:9cd91730dc8e:helloworld
```

### 设置密码长度。

在使用规则进行破解(暴力破解、掩码组合破解)时，可以通过`--increment`参数激活破解密码长度选项。可以通过`--increment-min`指定最小长度，通过`--increment-max`指定最大长度。

![increment_not_set](/images/Python/hashcat使用说明/increment_not_set.jpg)

可以看到在未设置长度的情况下，总共需要进行 $26^{10} = 141167095653376$ 次密码尝试。

![increment_set_8_9](/images/Python/hashcat使用说明/increment_set_8_9.jpg)

在设置了长度为8时，密码长度明显减少到了 $26^8 = 208827064576$ 次

### 恢复上一次的破解状态。

方法有两种：

第一种在在交互界面中使用`[p]ause`进行暂停。

![stdin_pause](/images/Python/hashcat使用说明/stdin_pause.jpg)

如需恢复，则在交互界面中使用`[r]esume`。

![restore_resume](/images/Python/hashcat使用说明/stdin_resume.jpg)

第二种需要事先指定会话。

首先需要在破解时指定会话`--session=xxx`，默认的`.restore`文件存放在`.hashcat/session/`目录下，如果需要在特殊位置存放缓存文件，需要增加`--restore-file-path`参数。

`.restore`文件为会话缓存文件，存放的是会话最后一次的破解状态，包括会话的执行命令、会话使用的目录、已使用的密码偏移等等。

`hashcat`会根据破解的进度自动保存`restore`文件！

正常退出，在交互界面使用`[q]uit`命令，则会保存最后一次的破解状态。如果异常退出或者强制退出`Ctrl + c`，则`.restore`文件将不记录最后一次的状态。

![restore_format](/images/Python/hashcat使用说明/restore_format.jpg)

```shell
# 启动会话任务helloworld，restore文件存放目录为./restore/helloword.restore
hashcat -a 0 -m 2500 --session helloworld --restore-file-path=./restore/helloword.restore  helloworld.hccapx Top306Million-WPA-probable-v2.txt
```

在界面输入命令参数`q`退出会话任务后，会将破解进度信息自动保存到restore文件中。

![restore_pause](/images/Python/hashcat使用说明/restore_pause.jpg)

存储完后，通过下面命令可以恢复绘画任务之前的状态。

```shell
# 前两个参数必须要填，如果之前是指定目录存放restore文件，则第三个文件也必须要设置
hashcat  --session helloworld --restore --restore-file-path=./restore/helloword.restore
```

![restore_resume](/images/Python/hashcat使用说明/restore_resume.jpg)

可以看见，任务从上一次结束的地方开始进行了！！

## 参考

[hashcat wiki](https://hashcat.net/hashcat/)
[hashcat restore](https://hashcat.net/wiki/doku.php?id=restore)
[hashcat use](https://klionsec.github.io/2017/04/26/use-hashcat-crack-hash/)
[Hybrid Wordlist + Mask](http://www.freebuf.com/column/176660.html)