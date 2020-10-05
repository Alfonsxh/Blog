---
title: "MySQL必知必会 - MySQL"
date: 2018-10-29 21:21:59
lastmod: 2018-10-29 21:21:59
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "MySQL"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

DBMS可以分为两类

- 一类为基于共享文件系统的DBMS，包括 `Microsoft Access` 和 `FileMaker`用于桌面用途。
- 一类为基于客户机-服务器的数据库。服务器部分是负责所有数据访问和处理的软件，运行在数据库服务器的计算机上。关于数据的添加、删除和更新的所有请求都是由服务器软件完成。客户机是与用户打交道的软件。

<!--more-->

## MySQL基本操作

### 连接

本地连接时，只需输入`mysql -uusername -ppassword`，`-u`后面为用户密码，`-p`后面为用户密码。

远程连接时，需要进行两步操作。

- 开启远程访问

```sql
MariaDB [(none)]> grant all on *.* to username@'%' identified by 'password';
MariaDB [(none)]> flush privileges;
MariaDB [(none)]> exit
```

- 开启远程访问的端口，默认是3306端口

```shell
> sudo iptables -I INPUT 4 -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT
```

### 选择数据库

在执行任意数据库操作前，需要选择一个数据库，使用`USE`关键字完成。

```sql
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| mysql              |
| test               |
+--------------------+
2 rows in set (0.00 sec)

MariaDB [(none)]> use test;
Database changed
```

展示数据库下的表。

```sql
MariaDB [test]> show tables;
+----------------+
| Tables_in_test |
+----------------+
| customers      |
| orderitems     |
| orders         |
| productnotes   |
| products       |
| vendors        |
+----------------+
6 rows in set (0.00 sec)
```

### show

`show`命令可以查看数据库服务器下的数据库、表、列、状态等信息。

```sql
MariaDB [test]> show columns from customers;    # 查看customers表中的列信息
+--------------+-----------+------+-----+---------+----------------+
| Field        | Type      | Null | Key | Default | Extra          |
+--------------+-----------+------+-----+---------+----------------+
| cust_id      | int(11)   | NO   | PRI | NULL    | auto_increment |
| cust_name    | char(50)  | NO   |     | NULL    |                |
| cust_address | char(50)  | YES  |     | NULL    |                |
| cust_city    | char(50)  | YES  |     | NULL    |                |
| cust_state   | char(5)   | YES  |     | NULL    |                |
| cust_zip     | char(10)  | YES  |     | NULL    |                |
| cust_country | char(50)  | YES  |     | NULL    |                |
| cust_contact | char(50)  | YES  |     | NULL    |                |
| cust_email   | char(255) | YES  |     | NULL    |                |
+--------------+-----------+------+-----+---------+----------------+
9 rows in set (0.00 sec)

MariaDB [test]> show create table customers;  # 查看创建customers表时的命令
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table     | Create Table                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| customers | CREATE TABLE `customers` (
  `cust_id` int(11) NOT NULL AUTO_INCREMENT,
  `cust_name` char(50) NOT NULL,
  `cust_address` char(50) DEFAULT NULL,
  `cust_city` char(50) DEFAULT NULL,
  `cust_state` char(5) DEFAULT NULL,
  `cust_zip` char(10) DEFAULT NULL,
  `cust_country` char(50) DEFAULT NULL,
  `cust_contact` char(50) DEFAULT NULL,
  `cust_email` char(255) DEFAULT NULL,
  PRIMARY KEY (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10006 DEFAULT CHARSET=latin1 |
+-----------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### select

为了使用select命令检索表数据，必须至少给出两条信息————想要什么，以及从什么地方选择。

#### 简单的select命令

```sql
MariaDB [test]> select prod_id, prod_name, prod_price from products;  # 选择多个列
+---------+----------------+------------+
| prod_id | prod_name      | prod_price |
+---------+----------------+------------+
| ANV01   | .5 ton anvil   |       5.99 |
| ANV02   | 1 ton anvil    |       9.99 |
| ANV03   | 2 ton anvil    |      14.99 |
| DTNTR   | Detonator      |      13.00 |
| FB      | Bird seed      |      10.00 |
| FC      | Carrots        |       2.50 |
| FU1     | Fuses          |       3.42 |
| JP1000  | JetPack 1000   |      35.00 |
| JP2000  | JetPack 2000   |      55.00 |
| OL1     | Oil can        |       8.99 |
| SAFE    | Safe           |      50.00 |
| SLING   | Sling          |       4.49 |
| TNT1    | TNT (1 stick)  |       2.50 |
| TNT2    | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
14 rows in set (0.00 sec)

MariaDB [test]> select * from products; # 选择所有的行
+---------+---------+----------------+------------+----------------------------------------------------------------+
| prod_id | vend_id | prod_name      | prod_price | prod_desc                                                      |
+---------+---------+----------------+------------+----------------------------------------------------------------+
| ANV01   |    1001 | .5 ton anvil   |       5.99 | .5 ton anvil, black, complete with handy hook                  |
| ANV02   |    1001 | 1 ton anvil    |       9.99 | 1 ton anvil, black, complete with handy hook and carrying case |
| ANV03   |    1001 | 2 ton anvil    |      14.99 | 2 ton anvil, black, complete with handy hook and carrying case |
| DTNTR   |    1003 | Detonator      |      13.00 | Detonator (plunger powered), fuses not included                |
| FB      |    1003 | Bird seed      |      10.00 | Large bag (suitable for road runners)                          |
| FC      |    1003 | Carrots        |       2.50 | Carrots (rabbit hunting season only)                           |
| FU1     |    1002 | Fuses          |       3.42 | 1 dozen, extra long                                            |
| JP1000  |    1005 | JetPack 1000   |      35.00 | JetPack 1000, intended for single use                          |
| JP2000  |    1005 | JetPack 2000   |      55.00 | JetPack 2000, multi-use                                        |
| OL1     |    1002 | Oil can        |       8.99 | Oil can, red                                                   |
| SAFE    |    1003 | Safe           |      50.00 | Safe with combination lock                                     |
| SLING   |    1003 | Sling          |       4.49 | Sling, one size fits all                                       |
| TNT1    |    1003 | TNT (1 stick)  |       2.50 | TNT, red, single stick                                         |
| TNT2    |    1003 | TNT (5 sticks) |      10.00 | TNT, red, pack of 10 sticks                                    |
+---------+---------+----------------+------------+----------------------------------------------------------------+
14 rows in set (0.00 sec)
```

#### 选择不同的行

`distinct`关键字指示MySQL只返回不同的值。它对所有的列都适用，如果给出`select distinct vend_id, prod_price from products;`这样的命令，除非是指定的两个字段的值完全不同，否则所有行都将被检索出来。

```sql
MariaDB [test]> select distinct vend_id from products;
+---------+
| vend_id |
+---------+
|    1001 |
|    1002 |
|    1003 |
|    1005 |
+---------+
4 rows in set (0.00 sec)

MariaDB [test]> select distinct vend_id, prod_price from products;
+---------+------------+
| vend_id | prod_price |
+---------+------------+
|    1001 |       5.99 |
|    1001 |       9.99 |
|    1001 |      14.99 |
|    1003 |      13.00 |
|    1003 |      10.00 |
|    1003 |       2.50 |
|    1002 |       3.42 |
|    1005 |      35.00 |
|    1005 |      55.00 |
|    1002 |       8.99 |
|    1003 |      50.00 |
|    1003 |       4.49 |
+---------+------------+
12 rows in set (0.00 sec)
```

### limit

`limit`关键字能够限制返回的结果数量，使返回值只返回规定的行。

```Sql
MariaDB [test]> select * from products limit 5;  # 限制显示5行的内容
+---------+---------+--------------+------------+----------------------------------------------------------------+
| prod_id | vend_id | prod_name    | prod_price | prod_desc                                                      |
+---------+---------+--------------+------------+----------------------------------------------------------------+
| ANV01   |    1001 | .5 ton anvil |       5.99 | .5 ton anvil, black, complete with handy hook                  |
| ANV02   |    1001 | 1 ton anvil  |       9.99 | 1 ton anvil, black, complete with handy hook and carrying case |
| ANV03   |    1001 | 2 ton anvil  |      14.99 | 2 ton anvil, black, complete with handy hook and carrying case |
| DTNTR   |    1003 | Detonator    |      13.00 | Detonator (plunger powered), fuses not included                |
| FB      |    1003 | Bird seed    |      10.00 | Large bag (suitable for road runners)                          |
+---------+---------+--------------+------------+----------------------------------------------------------------+
5 rows in set (0.00 sec)

MariaDB [test]> select * from products limit 5,5;  # 限制显示从第5行起(包括第5行)之后5行的内容
+---------+---------+--------------+------------+---------------------------------------+
| prod_id | vend_id | prod_name    | prod_price | prod_desc                             |
+---------+---------+--------------+------------+---------------------------------------+
| FC      |    1003 | Carrots      |       2.50 | Carrots (rabbit hunting season only)  |
| FU1     |    1002 | Fuses        |       3.42 | 1 dozen, extra long                   |
| JP1000  |    1005 | JetPack 1000 |      35.00 | JetPack 1000, intended for single use |
| JP2000  |    1005 | JetPack 2000 |      55.00 | JetPack 2000, multi-use               |
| OL1     |    1002 | Oil can      |       8.99 | Oil can, red                          |
+---------+---------+--------------+------------+---------------------------------------+
5 rows in set (0.00 sec)
```

#### 完全限定表名

```sql
MariaDB [test]> select products.prod_name from test.products;
+----------------+
| prod_name      |
+----------------+
| .5 ton anvil   |
| 1 ton anvil    |
| 2 ton anvil    |
| Detonator      |
| Bird seed      |
| Carrots        |
| Fuses          |
| JetPack 1000   |
| JetPack 2000   |
| Oil can        |
| Safe           |
| Sling          |
| TNT (1 stick)  |
| TNT (5 sticks) |
+----------------+
14 rows in set (0.00 sec)
```

### order by

`order by`关键字用于对选择的数据进行排序，可以选择默认排序、选择非选择的列进行排序、选择多个列进行排序。

```sql
MariaDB [test]> select prod_name from products limit 6; # 默认排序
+--------------+
| prod_name    |
+--------------+
| .5 ton anvil |
| 1 ton anvil  |
| 2 ton anvil  |
| Detonator    |
| Bird seed    |
| Carrots      |
+--------------+
6 rows in set (0.00 sec)

MariaDB [test]> select prod_name from products order by prod_name limit 6;  # 选择选择的列排序
+--------------+
| prod_name    |
+--------------+
| .5 ton anvil |
| 1 ton anvil  |
| 2 ton anvil  |
| Bird seed    |
| Carrots      |
| Detonator    |
+--------------+
6 rows in set (0.00 sec)

MariaDB [test]> select prod_name from products order by vend_id limit 6; # 选择非选择的列排序
+---------------+
| prod_name     |
+---------------+
| .5 ton anvil  |
| 1 ton anvil   |
| 2 ton anvil   |
| Fuses         |
| Oil can       |
| TNT (1 stick) |
+---------------+
6 rows in set (0.00 sec)
```

在按照多个列进行排序时，排序完全按照所规定的顺序进行。例如在执行下面命令时，仅在存在多行具有相同的`prod_price`值才对`prod_name`进行排序。如果`prod_price`列中所有的值都是唯一的，则不会按照`prod_name`进行排序。

```sql
MariaDB [test]> select prod_id, prod_price, prod_name from products order by prod_price,prod_name limit 6; # 选择多个列进行排序
+---------+------------+---------------+
| prod_id | prod_price | prod_name     |
+---------+------------+---------------+
| FC      |       2.50 | Carrots       |
| TNT1    |       2.50 | TNT (1 stick) |
| FU1     |       3.42 | Fuses         |
| SLING   |       4.49 | Sling         |
| ANV01   |       5.99 | .5 ton anvil  |
| OL1     |       8.99 | Oil can       |
+---------+------------+---------------+
6 rows in set (0.00 sec)
```

### desc

MySQL默认的排序方式为升序排序，`desc`关键字用来指定排序的方向为逆序。值得注意的是`desc`只应用到直接位于其前面的列名。

```sql
MariaDB [test]> select prod_id, prod_price, prod_name from products order by prod_price desc, prod_name limit 6;  # 按照prod_price列的逆序排列
+---------+------------+--------------+
| prod_id | prod_price | prod_name    |
+---------+------------+--------------+
| JP2000  |      55.00 | JetPack 2000 |
| SAFE    |      50.00 | Safe         |
| JP1000  |      35.00 | JetPack 1000 |
| ANV03   |      14.99 | 2 ton anvil  |
| DTNTR   |      13.00 | Detonator    |
| FB      |      10.00 | Bird seed    |
+---------+------------+--------------+
6 rows in set (0.00 sec)

MariaDB [test]> select prod_id, prod_price, prod_name from products order by prod_price, prod_name desc limit 6;  # 按照prod_price正序排列后，对数据进行prod_name的逆序排序
+---------+------------+---------------+
| prod_id | prod_price | prod_name     |
+---------+------------+---------------+
| TNT1    |       2.50 | TNT (1 stick) |
| FC      |       2.50 | Carrots       |
| FU1     |       3.42 | Fuses         |
| SLING   |       4.49 | Sling         |
| ANV01   |       5.99 | .5 ton anvil  |
| OL1     |       8.99 | Oil can       |
+---------+------------+---------------+
6 rows in set (0.00 sec)
```

### where

`where`关键字为检索的数据设置过滤条件。`where`的位置应当位于`order by`子句的后面。

|操作符|说明|
|:---:|:---:|
|=|等于|
|<>|不等于|
|!=|不等于|
|<|小于|
|<=|小于等于|
|>|大于|
|>=|大于等于|
|bwtween|在指定两值之间|

#### 简单过滤

单引号或双引号用来限定字符串，例如过滤条件为字符串时，必须使用单引号或双引号。

```sql
MariaDB [test]> select prod_name,prod_price from products where prod_name = "fuses";    # 字符串过滤条件
+-----------+------------+
| prod_name | prod_price |
+-----------+------------+
| Fuses     |       3.42 |
+-----------+------------+
1 row in set (0.00 sec)

MariaDB [test]> select prod_name,prod_price from products where vend_id != 1003;
+--------------+------------+
| prod_name    | prod_price |
+--------------+------------+
| .5 ton anvil |       5.99 |
| 1 ton anvil  |       9.99 |
| 2 ton anvil  |      14.99 |
| Fuses        |       3.42 |
| JetPack 1000 |      35.00 |
| JetPack 2000 |      55.00 |
| Oil can      |       8.99 |
+--------------+------------+
7 rows in set (0.00 sec)
```

#### 进阶过滤

MySQL允许给出多个where子句，以`and`子句或者`or`子句的方式使用。

`and操作符`给where子句附加条件。

`or操作符`指示MySQL检索匹配任一条件的行。

```sql
MariaDB [test]> select vend_id,prod_name,prod_price from products where vend_id = 1003 and prod_price <= 10;
+---------+----------------+------------+
| vend_id | prod_name      | prod_price |
+---------+----------------+------------+
|    1003 | Bird seed      |      10.00 |
|    1003 | Carrots        |       2.50 |
|    1003 | Sling          |       4.49 |
|    1003 | TNT (1 stick)  |       2.50 |
|    1003 | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
5 rows in set (0.01 sec)

MariaDB [test]> select vend_id, prod_name,prod_price from products where vend_id = 1003 or prod_price <= 10;
+---------+----------------+------------+
| vend_id | prod_name      | prod_price |
+---------+----------------+------------+
|    1001 | .5 ton anvil   |       5.99 |
|    1001 | 1 ton anvil    |       9.99 |
|    1003 | Detonator      |      13.00 |
|    1003 | Bird seed      |      10.00 |
|    1003 | Carrots        |       2.50 |
|    1002 | Fuses          |       3.42 |
|    1002 | Oil can        |       8.99 |
|    1003 | Safe           |      50.00 |
|    1003 | Sling          |       4.49 |
|    1003 | TNT (1 stick)  |       2.50 |
|    1003 | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
11 rows in set (0.00 sec)
```

`()操作符`允许两者结合以进行复杂和高级的过滤。

```sql
MariaDB [test]> select vend_id, prod_name,prod_price from products where vend_id = 1003 or vend_id = 1002 and  prod_price <= 10;
+---------+----------------+------------+
| vend_id | prod_name      | prod_price |
+---------+----------------+------------+
|    1003 | Detonator      |      13.00 |
|    1003 | Bird seed      |      10.00 |
|    1003 | Carrots        |       2.50 |
|    1002 | Fuses          |       3.42 |
|    1002 | Oil can        |       8.99 |
|    1003 | Safe           |      50.00 |
|    1003 | Sling          |       4.49 |
|    1003 | TNT (1 stick)  |       2.50 |
|    1003 | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
9 rows in set (0.00 sec)

MariaDB [test]> select vend_id, prod_name,prod_price from products where (vend_id = 1003 or vend_id = 1002) and  prod_price <= 10;
+---------+----------------+------------+
| vend_id | prod_name      | prod_price |
+---------+----------------+------------+
|    1003 | Bird seed      |      10.00 |
|    1003 | Carrots        |       2.50 |
|    1002 | Fuses          |       3.42 |
|    1002 | Oil can        |       8.99 |
|    1003 | Sling          |       4.49 |
|    1003 | TNT (1 stick)  |       2.50 |
|    1003 | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
7 rows in set (0.00 sec)
```

`in操作符`指定条件范围，范围中的每个条件都可以进行匹配。类似于`or操作符`，但比它更清楚且直观。

```sql
MariaDB [test]> select vend_id, prod_name,prod_price from products where vend_id = 1003 or vend_id = 1002;
+---------+----------------+------------+
| vend_id | prod_name      | prod_price |
+---------+----------------+------------+
|    1003 | Detonator      |      13.00 |
|    1003 | Bird seed      |      10.00 |
|    1003 | Carrots        |       2.50 |
|    1002 | Fuses          |       3.42 |
|    1002 | Oil can        |       8.99 |
|    1003 | Safe           |      50.00 |
|    1003 | Sling          |       4.49 |
|    1003 | TNT (1 stick)  |       2.50 |
|    1003 | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
9 rows in set (0.00 sec)

MariaDB [test]> select vend_id, prod_name,prod_price from products where vend_id in (1002, 1003);
+---------+----------------+------------+
| vend_id | prod_name      | prod_price |
+---------+----------------+------------+
|    1003 | Detonator      |      13.00 |
|    1003 | Bird seed      |      10.00 |
|    1003 | Carrots        |       2.50 |
|    1002 | Fuses          |       3.42 |
|    1002 | Oil can        |       8.99 |
|    1003 | Safe           |      50.00 |
|    1003 | Sling          |       4.49 |
|    1003 | TNT (1 stick)  |       2.50 |
|    1003 | TNT (5 sticks) |      10.00 |
+---------+----------------+------------+
9 rows in set (0.00 sec)
```

`not操作符`否定它之后所跟的任何条件。

```sql
MariaDB [test]> select vend_id, prod_name,prod_price from products where vend_id not in (1002, 1003);
+---------+--------------+------------+
| vend_id | prod_name    | prod_price |
+---------+--------------+------------+
|    1001 | .5 ton anvil |       5.99 |
|    1001 | 1 ton anvil  |       9.99 |
|    1001 | 2 ton anvil  |      14.99 |
|    1005 | JetPack 1000 |      35.00 |
|    1005 | JetPack 2000 |      55.00 |
+---------+--------------+------------+
5 rows in set (0.00 sec)
```

#### 通配符过滤

`like操作符`目的是在搜索子句中使用通配符。

`%通配符`表示任何字符出现任意次数。

```sql
MariaDB [test]> select prod_id,prod_name from products where prod_name like "tpa%"; # 检索以tpa开头的字段
Empty set (0.00 sec)

MariaDB [test]> select prod_id,prod_name from products where prod_name like "%tpa%";    # 检索中间含有tpa的字段
+---------+--------------+
| prod_id | prod_name    |
+---------+--------------+
| JP1000  | JetPack 1000 |
| JP2000  | JetPack 2000 |
+---------+--------------+
2 rows in set (0.00 sec)
```

`_通配符`只匹配单个字符而不是多个字符。

```sql
MariaDB [test]> select prod_id,prod_name from products where prod_name like "_et%"; # 匹配以_et开头的字符
+---------+--------------+
| prod_id | prod_name    |
+---------+--------------+
| DTNTR   | Detonator    |
| JP1000  | JetPack 1000 |
| JP2000  | JetPack 2000 |
+---------+--------------+
3 rows in set (0.00 sec)
```

> 注意：
> - 通配符搜索的处理一般要比其他搜索所花的时间更长。
> - 不要过度使用通配符。如果其他操作符能达到相同的目的，应该使用其他操作符。
> - 尽可能不将通配符放置在搜索模式的开始处。
> - 注意通配符的位置，放置不当可能不会返回想要的数据。

#### 正则表达式过滤

`regexp操作符`用来表示通过正则表达式进行过滤。

`regexp`和`like`有所区别，`like`是匹配完整的数据，`regexp`匹配的是部分数据。例如当匹配 **JetPack 1000** 时， **like jetpack** 匹配结果为空，**like jetpack%** 才能匹配到。而 **regexp 'jetpack'** 能够匹配上。

```sql
MariaDB [test]> select prod_id,prod_name from products where prod_name like "jet";
Empty set (0.00 sec)

MariaDB [test]> select prod_id,prod_name from products where prod_name like "jet%";
+---------+--------------+
| prod_id | prod_name    |
+---------+--------------+
| JP1000  | JetPack 1000 |
| JP2000  | JetPack 2000 |
+---------+--------------+
2 rows in set (0.00 sec)

MariaDB [test]> select prod_id,prod_name from products where prod_name regexp "jet";
+---------+--------------+
| prod_id | prod_name    |
+---------+--------------+
| JP1000  | JetPack 1000 |
| JP2000  | JetPack 2000 |
+---------+--------------+
2 rows in set (0.00 sec)
```

正则使用`|符号`进行or匹配。

```sql
MariaDB [test]> select prod_id,prod_name from products where prod_name regexp "1000|2000";
+---------+--------------+
| prod_id | prod_name    |
+---------+--------------+
| JP1000  | JetPack 1000 |
| JP2000  | JetPack 2000 |
+---------+--------------+
2 rows in set (0.00 sec)
```

使用`[]`进行范围匹配。

```sql
MariaDB [test]> select prod_id,prod_name from products where prod_id regexp "anv0[1-9]";
+---------+--------------+
| prod_id | prod_name    |
+---------+--------------+
| ANV01   | .5 ton anvil |
| ANV02   | 1 ton anvil  |
| ANV03   | 2 ton anvil  |
+---------+--------------+
3 rows in set (0.00 sec)
```

匹配特殊字符时，使用`\\反斜杠`进行转义。这里不使用一个`\`的原因在于，MySQL自己解释一个，正则表达式库解释另一个。

```sql
MariaDB [test]> select * from vendors where vend_name regexp "\\.";
+---------+--------------+-----------------+-----------+------------+----------+--------------+
| vend_id | vend_name    | vend_address    | vend_city | vend_state | vend_zip | vend_country |
+---------+--------------+-----------------+-----------+------------+----------+--------------+
|    1004 | Furball Inc. | 1000 5th Avenue | New York  | NY         | 11111    | USA          |
+---------+--------------+-----------------+-----------+------------+----------+--------------+
1 row in set (0.01 sec)
```

字符类

|类|说明|
|:---:|:---|
|[:alnum:]|任意字母和数字([a-zA-Z0-9])|
|[:alpha:]|任意字符([a-zA-Z])|
|[:blank:]|空格和制表([\\\\t])|
|[:cntrl:]|ASCII控制字符(ASCII 0到31和127)|
|[:digit:]|任意数字([0-9])|
|[:xdigit:]|任意十六进制数字([a-fA-F0-9])|
|[:print:]|任意可打印字符|
|[:graph:]|与[:print:]相同，但不包括空格|
|[:lower:]|任意小写字母([a-z])|
|[:upper:]|任意大写字母([A-Z])|
|[:punct:]|既不在[:alnum:]又不在[:cntrl:]中的任意字符|
|[:space:]|包括空格在内的任意空白字符([\\\\f\\\\n\\\\r\\\\t\\\\v])|

重复元字符

|元字符|说明|
|:---|:---|
|*|0个或多个匹配|
|+|1个或多个匹配(等于{1,})|
|?|0个或1个匹配(等于{0,1})|
|{n}|指定数目的匹配|
|{n,}|不少于指定数目的匹配|
|{n,m}|匹配数目的范围(m不超过255)|

```sql
MariaDB [test]> select prod_name from products where prod_name regexp "\\([0-9] sticks?\\)"; # 匹配stick，末尾的s出现0次或1次
+----------------+
| prod_name      |
+----------------+
| TNT (1 stick)  |
| TNT (5 sticks) |
+----------------+
2 rows in set (0.00 sec)

MariaDB [test]> select prod_name from products where prod_name regexp "[[:digit:]]{4}"; # 匹配数字出现4次
+--------------+
| prod_name    |
+--------------+
| JetPack 1000 |
| JetPack 2000 |
+--------------+
2 rows in set (0.00 sec)
```

定位元字符

|元字符|说明|
|:---|:---|
|^|文本的开始|
|$|文本的结束|
|[[:<:]]|词的开始|
|[[:>:]]|词的结尾|

```sql
MariaDB [test]> select prod_name from products where prod_name regexp "g[[:>:]]"; # 匹配以g结尾的单词
+-----------+
| prod_name |
+-----------+
| Sling     |
+-----------+
1 row in set (0.00 sec)

MariaDB [test]> select prod_name from products where prod_name regexp "[[:<:]]j";  # 匹配以j开头的单词
+--------------+
| prod_name    |
+--------------+
| JetPack 1000 |
| JetPack 2000 |
+--------------+
2 rows in set (0.00 sec)
```