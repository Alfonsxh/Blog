---
title: "Redis使用"
date: 2018-12-18 21:21:48
lastmod: 2019-01-13 11:29:53
draft: false
keywords: ["Python", "Redis"]
description: "Redis使用"
tags: ["Python", "Redis"]
categories: ["Python", "Redis"]
author: "Alfons"
---

**Redis** 可以把它当作一个 **存在于内存中、非关系型(nosql)的数据库**。其实现有点儿类似于 **磁盘缓存策略的实现方式**，不过似乎要复杂一点。

<!--more-->

**Redis** 具有一些特点：

- 完全开源
- **数据持久化** - 可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
- 不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
- 支持数据的备份，即master-slave模式的数据备份。
- **性能极高** – Redis能读的速度是110000次/s，写的速度是81000次/s 。
- **丰富的数据类型** – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets数据类型操作。
- **原子** – Redis的所有操作都是原子性的，同时Redis还支持对几个操作全并后的原子性执行。
- **丰富的特性** – Redis还支持 publish/subscribe, 通知, key 过期等等特性。

## 安装

Ubuntu：

```shell
sudo apt-get install redis-server
sudo systemctl start redis.service  // 一般安装好以后就会自动启动服务
```

## 使用

***(这篇记录的只是简单的使用)***

下面操作内容会从 **Redis** 所支持的几种常见的数据格式进行记录，包括：**string**、**hash**、**list**、**set**、**sorted set**。

首先，要进行 **redis** 的存取，得确保 **redis server** 处于开启状态，这点和常用的数据库一样。然后用户通过 **redis-cli** 客户端与 **redis服务器** 进行通信。

```shell
$ redis-cli
127.0.0.1:6379> ping
PONG
```

下面的操作都是在 **redis-cli** 上进行的。

### 通用命令格式

**redis** 命令的基本语法如下：

```shell
127.0.0.1:6379> COMMAND KEY_NAME
```

基本的命令如下：

| 命令                                     | 说明                                               | 返回值                                                                                             |
| :--------------------------------------- | :------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| **del key**                              | 用于key存在时删除key                               | 删除成功返回1，失败返回0。                                                                         |
| **dump key**                             | 序列化给定的key，并返回被序列化的值。              | 失败返回nil                                                                                        |
| **exists key**                           | 检查给定key是否存在                                | 若 key 存在返回 1 ，否则返回 0 。                                                                  |
| **expire key seconds**                   | 为给定的key设置过期时间，以秒计算。                | 设置成功返回1，失败返回0                                                                           |
| **expireat key timestamp**               | 为给定的key设置过期时间，timestamp为时间戳(单位秒) | 设置成功返回1，失败返回0                                                                           |
| **pexpire key milliseconds**             | 设置key的过期时间，以毫秒计算                      | 设置成功返回1，失败返回0                                                                           |
| **pexpireat key milliseconds-timestamp** | 为给定的key设置过期时间，timestamp为时间戳(毫秒级) | 设置成功返回1，失败返回0                                                                           |
| **keys pattern**                         | 找出所有给定过滤条件的key                          | 成功返回所有符合条件的key值，失败返回(empty list or set)                                           |
| **move key db**                          | 将redis中的key移动到指定的数据库中                 | 设置成功返回1，失败返回0                                                                           |
| **persist key**                          | 移除key的过期时间，key将持久保持                   | 设置成功返回1，失败返回0                                                                           |
| **pttl key**                             | 以毫秒为单位返回key的剩余过期时间                  | 当key不存在时返回-2，当key存在但未设置过期时间时返回-1.否则，以毫秒为单位，返回key的剩余生存时间。 |
| **ttl key**                              | 以秒为单位返回key的剩余过期时间                    | 当key不存在时返回-2，当key存在但未设置过期时间时返回-1.否则，以秒为单位，返回key的剩余生存时间。   |
| **randomkey**                            | 随机取出一个key的值                                | 返回随机取出的key                                                                                  |
| **rename key newkey**                    | 重命名key的名字为newkey                            | 如果key不存在，返回 **(error) ERR no such key**，操作成功返回 **OK**                               |
| **renamenx key newkey**                  | 仅当newkey不存在时，将key改名为newkey              | 设置成功返回1，失败返回0                                                                           |
| **type key**                             | 返回key所存储的值的类型                            | key存在返回type，不存在返回none                                                                    |

**redis** 中的 **key_name** 要遵循一定的规范：

- **太长的key值不推荐** - 不仅消耗内存，而且数据中查找的成本很高。
- **太短的key值也不推荐** - 如果key值太短，导致开发的复杂度增加，得不偿失。
- **坚持一种命名方式** - 如 **object-type: id: field** 就不错。

### string

**string** 是 **redis** 最基本的的类型，它可以包含任何数据，包括jpg图片或者序列化的对象，最大能存储512MB。

下面是 **redis** 中 **string类型** 的基本操作命令：

```shell
// set key
127.0.0.1:6379> set one_word "this is a big apple"
OK
// get key
127.0.0.1:6379> get one_word    // 通过key获取value
"this is a big apple"

// getrange key start end
127.0.0.1:6379> getrange one_word 0 5  // 按照范围获取，类似于切片
"this i"
127.0.0.1:6379> getrange one_word 0 -1
"this is a big apple"

// setrange key offset value
127.0.0.1:6379> setrange one_word 0 ww      // 从偏移处替换
(integer) 5
127.0.0.1:6379> get one_word
"wwllo"
127.0.0.1:6379> setrange one_word 6 world
(integer) 11
127.0.0.1:6379> get one_word
"wwllo\x00world"

// getset key value
127.0.0.1:6379> getset one_word "there are same banans"     // 设置新的值，并返回原先旧的值，如果原值不存在，返回nil
"this is a big apple"
127.0.0.1:6379> get one_word
"there are same banans"

// setex key seconds value
127.0.0.1:6379> setex one_word 10 hello        // value关联key时，设置过期时间，单位秒
OK
...
127.0.0.1:6379> get one_word        // 10s后
(nil)

// psetex key milliseconds value
127.0.0.1:6379> psetex six_word 5000 "6"  // 设置key并指定过期时间，毫秒级
OK
...
127.0.0.1:6379> get six_word    // 5000ms后
(nil)

// setnx key value
127.0.0.1:6379> setnx one_word "hello"      // 设置key，如果不存在，修改key对应的value，并返回1，否则返回0
(integer) 1
127.0.0.1:6379> setnx one_word "world"
(integer) 0
127.0.0.1:6379> get one_word
"hello"

// strlen key
127.0.0.1:6379> strlen one_word     // 返回value的字符串长度
(integer) 11

// mset key value [key value...]
127.0.0.1:6379> mset two_word "twoword" third_word "third_word"     // 批量设置
OK
// mget key [key...]
127.0.0.1:6379> mget one_word two_word third_word       // 批量读取
1) "wwllo\x00world"
2) "twoword"
3) "third_word"

// msetnx key value [key value...]
127.0.0.1:6379> msetnx two_word "2" third_word "3"      // 批量设置，当key不存在时返回1，key存在返回0
(integer) 0
127.0.0.1:6379> msetnx two_word "2" third_word "3" four_word "4"
(integer) 0
127.0.0.1:6379> msetnx four_word "4" five_word "5"
(integer) 1

// incr key
127.0.0.1:6379> incr five_word      // 将指定key的数字值增加一，只针对整数值
(integer) 6
127.0.0.1:6379> get five_word
"6"
127.0.0.1:6379> incr one_word       // 非数字变量返回错误
(error) ERR value is not an integer or out of range

// incrby key increment
127.0.0.1:6379> incrby five_word 10     // 增加指定的数字，只针对整数值
(integer) 16
127.0.0.1:6379> get five_word
"16"

// incrbyfloat key increment
127.0.0.1:6379> incrbyfloat five_word 10.23     // 增加指定的浮点数
"26.23"
127.0.0.1:6379> get five_word
"26.23"

127.0.0.1:6379> set five_word 10
OK
127.0.0.1:6379> get five_word
"10"

// decr key
127.0.0.1:6379> decr five_word      // 将指定key的数字值减少一，只针对整数值
(integer) 9
127.0.0.1:6379> get five_word
"9"

// decrby key decrement
127.0.0.1:6379> decrby five_word 8   // 将指定key的数字值减少指定的整数，只针对整数值
(integer) 1
127.0.0.1:6379> get five_word
"1"

// append key value
127.0.0.1:6379> get one_word
"wwllo\x00world"
127.0.0.1:6379> APPEND one_word " !!"   // 在指定key的value末尾追加内容
(integer) 14
127.0.0.1:6379> get one_word
"wwllo\x00world !!"
```

### hash

**hash类型** 是一个 **string类型的field和value的映射表**。通常被用来 **存储对象类型的数据**。

下面是 **redis hash类型** 的基本操作：

```shell
// hset key field value
127.0.0.1:6379> hset hash_1 name alfons     // 设置key的field字段为value，字段之前未设置返回1，字段之前存在返回0
(integer) 1

// hget key field
127.0.0.1:6379> hget hash_1 name    // 通过key和field获取对应的value
"alfons"

// hgetall key
127.0.0.1:6379> hgetall hash_1      // 获取指定key的所有的内容，包括field和value
1) "name"
2) "alfons"

// hkeys key
127.0.0.1:6379> hkeys hash_1        // 获取指定key的所有field
1) "name"

// hvals key
127.0.0.1:6379> hvals hash_1        // 获取指定key的所有value
1) "alfons"

// hlen key
127.0.0.1:6379> hlen hash_1         // 获取指定key的字段数量
(integer) 1

// hexists key field
127.0.0.1:6379> HEXISTS hash_1 name     // 指定key的field是否存在，存在返回1，不存在返回0
(integer) 1
127.0.0.1:6379> HEXISTS hash_1 wechat
(integer) 0

// hmset key field vaule [field value...]
127.0.0.1:6379> hmset hash:user:xh name xh old 20 tel 123456789 like ft school cq lastlogin 12.05       // 批量设置指定key的 field与value数据
OK

// hmget key field [field...]
127.0.0.1:6379> hmget hash:user:xh name old tel     // 批量获取指定key的多个field的value
1) "xh"
2) "20"
3) "123456789"

// hdel key field [field...]
127.0.0.1:6379> hdel hash_1 name tel        // 删除指定key的多个field
(integer) 2
127.0.0.1:6379> hkeys hash_1
1) "like"
2) "school"
3) "lastlogin"
4) "old"
```

### list

说是 **list**，但操作起来类似于 **栈和双端队列**，可以在头和尾插入或删除元素。

基本操作如下：

```shell
// lpush key value [value...]
127.0.0.1:6379> lpush booklist c++ java android     // 向key列表头部插入value
(integer) 3

// lpushx key value
127.0.0.1:6379> lpushx booklist ios     // 向已存在的key列表头部插入元素，key列表不存在返回0
(integer) 5

// lrange key start stop
127.0.0.1:6379> lrange booklist 0 -1        // 获取key列表切片范围内的元素
1) "ios"
3) "android"
4) "java"
5) "c++"
127.0.0.1:6379> lpushx booklist2 ios
(integer) 0

// rpush key value
127.0.0.1:6379> rpush booklist python       // 向key列表尾部插入value
(integer) 5

// rpushx key value
127.0.0.1:6379> rpushx booklist python3     // 向已存在的key列表尾部插入元素，key列表不存在返回0
(integer) 6
127.0.0.1:6379> lrange booklist 0 -1
1) "ios"
2) "android"
3) "java"
4) "c++"
5) "python"
6) "python3"

// llen key
127.0.0.1:6379> llen booklist       // 查看key列表中元素的个数
(integer) 6

// lindex key index
127.0.0.1:6379> lindex booklist 0       // 通过索引值获取元素
"ios"

// lset key index value
127.0.0.1:6379> lset booklist 0 mac-ios     // 通过索引值修改元素值
OK
127.0.0.1:6379> lindex booklist 0
"mac-ios"

// lpop key
127.0.0.1:6379> lpop booklist       // 移除并获取key列表头部的元素
"mac-ios"

// rpop key
127.0.0.1:6379> rpop booklist       // 移除并获取key列表尾部的元素
"python3"
127.0.0.1:6379> lrange booklist 0 -1
1) "android"
2) "java"
3) "c++"
4) "python"

// lrem key counts value
127.0.0.1:6379> lrem booklist 1 c++     // 移除列表中counts个value元素，counts未正数表示从头部开始，负数为从尾部开始，为0表示移除所有value元素
(integer) 1

127.0.0.1:6379> LPUSH booklist go c++ c
(integer) 6
127.0.0.1:6379> lrange booklist 0 -1
1) "c"
2) "c++"
3) "go"
4) "android"
5) "java"
6) "python"

// ltrim key start stop
127.0.0.1:6379> ltrim booklist 2 -1     // 保留指定的切片
OK
127.0.0.1:6379> lrange booklist 0 -1
1) "go"
2) "android"
3) "java"
4) "python"
```

### set

**set类型** 是String类型的无序集合，里面的内容是唯一的。 **redis** 中 **set** 是通过哈希表实现的，所以它的添加、删除、查找操作的时间复杂度都为 **O(1)**。

```shell
// sadd key member
127.0.0.1:6379> sadd nameset Jhon       // 向为key的set中添加元素，成功添加返回1，否则返回0
(integer) 1

// smembers key
127.0.0.1:6379> smembers nameset        // 获取为key的set中的元素
1) "Jhon"

127.0.0.1:6379> sadd nameset Jhon
(integer) 0
127.0.0.1:6379> SMEMBERS nameset
1) "Jhon"
127.0.0.1:6379> sadd nameset Tom
(integer) 1
127.0.0.1:6379> SMEMBERS nameset
1) "Jhon"
2) "Tom"

// srandmeber key counts
127.0.0.1:6379> SRANDMEMBER nameset 0       // 随机返回规定counts数目的元素
(empty list or set)
127.0.0.1:6379> SRANDMEMBER nameset 1
1) "Jhon"
127.0.0.1:6379> SRANDMEMBER nameset 2
1) "Jhon"
2) "Tom"

// scard key
127.0.0.1:6379> scard nameset       // 返回对应key的set中的member个数
(integer) 2

// spop key
127.0.0.1:6379> spop nameset        // 移除并获取名为key的set中随机的一个元素
"Tom"

127.0.0.1:6379> sadd footballclub Tom alfons jim jhon petter pom
(integer) 6
127.0.0.1:6379> sadd bickclub maple alfons coco
(integer) 3

// sdiff key1 [key2 key3...]
127.0.0.1:6379> sdiff footballclub bickclub     // 获取key1与后续keyN的差集，只在key1中有
1) "jim"
2) "petter"
3) "jhon"
4) "Tom"
5) "pom"
127.0.0.1:6379> sdiff  bickclub footballclub
1) "coco"
2) "maple"

// sdiffstore destination key1 [key2 key3...]
127.0.0.1:6379> sdiffstore diffset  bickclub footballclub       // 将差集存储到名为destination的set中
(integer) 2
127.0.0.1:6379> SMEMBERS diffset
1) "coco"
2) "maple"

// sinter key1 [key2 key3...]
127.0.0.1:6379> sinter footballclub bickclub        // 返回指定set中的交集
1) "alfons"

// sinterstore destination key1 [key2 key3...]
127.0.0.1:6379> sinterstore interset footballclub bickclub      // 将指定set的交集存储到名为destination的set中
(integer) 1
127.0.0.1:6379> SMEMBERS interset
1) "alfons"

// sunion key1 [key2 key3...]
127.0.0.1:6379> SUNION footballclub bickclub        // 获取指定key之间的交集
1) "jhon"
2) "petter"
3) "alfons"
4) "Tom"
5) "coco"
6) "jim"
7) "pom"
8) "maple"

// sunionstore destination key1 [key2 key3...]
127.0.0.1:6379> sunionstore unionset footballclub bickclub      // 获取指定key之间的交集并存储到destination中
(integer) 8
127.0.0.1:6379> SMEMBERS unionset
1) "jhon"
2) "petter"
3) "alfons"
4) "Tom"
5) "coco"
6) "jim"
7) "pom"
8) "maple"

// sismember key member
127.0.0.1:6379> SISMEMBER interset tom      // 判断指定的member是否是key中的元素，是返回1，不是返回0
(integer) 0
127.0.0.1:6379> SISMEMBER interset alfons
(integer) 1

// smove source destination memeber
127.0.0.1:6379> smove bickclub footballclub maple       // 将member从source移动到destination
(integer) 1
127.0.0.1:6379> SMEMBERS bickclub
1) "coco"
2) "alfons"
127.0.0.1:6379> SMEMBERS footballclub
1) "jhon"
2) "petter"
3) "alfons"
4) "Tom"
5) "jim"
6) "pom"
7) "maple"

// srem key member1 [member2 member3...]
127.0.0.1:6379> SREM bickclub coco      // 移除指定key中的若干个元素，失败返回0
(integer) 1
127.0.0.1:6379> SMEMBERS bickclub
1) "alfons"
```

### sorted set

和 **set类型** 一样， **sorted set** 同样是元素的集合，且不允许出现相同的元素。不同的是，每个元素会关联一个double类型的分数，通过该分数来给集合中的成员进行排序。

基本操作如下：

```shell
// zadd key score1 member1 [score2 member2 score3 member3...]
127.0.0.1:6379> zadd classset 1 Jhon 2 Tom 3 alfons 4 maple     // 添加多个成员到有序集合中
(integer) 4

// zcard key
127.0.0.1:6379> zcard classset      // 显示指定key中的元素个数
(integer) 4

// zcount key min max
127.0.0.1:6379> zcount classset 2 3         // 获取指定分值之间元素的个数
(integer) 2

// zrange key start stop [withscores]
127.0.0.1:6379> zrange classset 0 -1    // 获取指定key的切片，withscores为需要打印分值
1) "Jhon"
2) "Tom"
3) "alfons"
4) "maple"
127.0.0.1:6379> zrange classset 0 -1 withscores
1) "Jhon"
2) "1"
3) "Tom"
4) "2"
5) "alfons"
6) "3"
7) "maple"
8) "4"

// zlexcount key min max
127.0.0.1:6379> ZLEXCOUNT classset [Jhon [maple     // 获取指定string元素的区间的元素数目
(integer) 4

// zrangebylex key min max
127.0.0.1:6379> ZRANGEBLEX classset [Jhon [alfons       // 通过指定string区间获取元素
1) "Jhon"
2) "Tom"
3) "alfons"

// zrangebyscore
127.0.0.1:6379> zrangebyscore classset 2 4      // 通过指定分值区间获取元素
1) "Tom"
2) "alfons"
3) "maple"

// zscore key member
127.0.0.1:6379> ZSCORE classset maple       // 获取指定成员的分值
"4"

// zrem key member
127.0.0.1:6379> ZREM classset alfons        // 移除指定元素
(integer) 1
127.0.0.1:6379> zrange classset 0 -1
1) "Jhon"
2) "Tom"
3) "maple"

// zremrangebylex key min max
127.0.0.1:6379> zremrangebylex classset [Jhon [Tom      // 通过字符串找到指定位置，移除中间的元素
(integer) 2
127.0.0.1:6379> zrange classset 0 -1
1) "maple"

// zremrangebyrank key start stop
127.0.0.1:6379> zremrangebyrank classset 0 -1       // 以切片的方式移除元素
(integer) 1
```

## 参考

- [Redis 教程](http://www.runoob.com/redis/redis-tutorial.html)