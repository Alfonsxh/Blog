---
title: "MySQL必知必会 - 增删改"
date: 2018-10-29 21:21:59
lastmod: 2018-10-29 21:21:59
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "增删改"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

## 创建和删除数据库

创建数据库的方式有两种，一种登陆后创建，一种使用mysqladmin创建。

```sql
CREATE DATABASE 数据库名;

mysqladmin -u root -p create RUNOOB
```

删除数据库使用`drop databse`命令。

<!--more-->

```sql
drop database <数据库名>;

drop database if exists <数据库名>;         // 删除存在的数据库
```

## 创建、删除、更新表

### 创建表

- `null`值和空字符串不一样。
- 主键`primary key`可以包含多个主键。
- 主键中只能使用不允许null值的列。允许null值的列不能作为唯一标识。
- 每个表只允许一个`auto_increment`列。
- 当人为`insert`的数据覆盖了`auto_increment`的列时(比之前的值大)，下次插入的数据会从较大的值开始计算。
- 通过`default`参数设置默认值。

```sql
MariaDB [test]> create table if not exists customersTest
                (
                  cust_id int not null auto_increment,
                  cust_name char(50) not null,
                  primary key (cust_id)
                ) engine=innodb;

MariaDB [test]> show tables;
+----------------+
| Tables_in_test |
+----------------+
| customers      |
| customersTest  |
| orderitems     |
| orders         |
| productnotes   |
| products       |
| vendors        |
+----------------+
7 rows in set (0.00 sec)
```

### 删除表

需要注意的是，如果目标表中包含了外键，需要先解除对应的外键，才能删除表，否则会发生错误。

```sql
MariaDB [test]> drop table if exists customersTest;
Query OK, 0 rows affected (0.00 sec)

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

### 修改表

使用`alter table`语句，可以对表进行修改。不过建议是开始设计数据库表结构时，尽量准确，避免后续的修改。

`alter table`另一种常见用途是定义外键。

```sql
MariaDB [test]> alter table customersTest add cust_test char(20);  // 添加一个列cust_test
Query OK, 5 rows affected (0.00 sec)               
Records: 5  Duplicates: 0  Warnings: 0

MariaDB [test]> show columns from customersTest;
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
| cust_test    | char(20)  | YES  |     | NULL    |                |
+--------------+-----------+------+-----+---------+----------------+
10 rows in set (0.00 sec)

MariaDB [test]> alter table customersTest drop cust_id;     // 删除cust_id列
Query OK, 5 rows affected (0.00 sec)               
Records: 5  Duplicates: 0  Warnings: 0

MariaDB [test]> show columns from customersTest;
+--------------+-----------+------+-----+---------+-------+
| Field        | Type      | Null | Key | Default | Extra |
+--------------+-----------+------+-----+---------+-------+
| cust_name    | char(50)  | NO   |     | NULL    |       |
| cust_address | char(50)  | YES  |     | NULL    |       |
| cust_city    | char(50)  | YES  |     | NULL    |       |
| cust_state   | char(5)   | YES  |     | NULL    |       |
| cust_zip     | char(10)  | YES  |     | NULL    |       |
| cust_country | char(50)  | YES  |     | NULL    |       |
| cust_contact | char(50)  | YES  |     | NULL    |       |
| cust_email   | char(255) | YES  |     | NULL    |       |
| cust_test    | char(20)  | YES  |     | NULL    |       |
+--------------+-----------+------+-----+---------+-------+
9 rows in set (0.00 sec)
```

复杂表结构的修改一般需要手动删除过程

- 用新的列布局创建一个新表；
- 使用`insert select`从旧表复制数据到新表。如果有必要，可使用转换函数和计算字段；
- 检验包含所需数据的新表；
- 重命名或删除旧表；
- 用旧表原来的名字重命名新表；
- 根据需要，重新创建触发器、存储过程、索引和外键。

重命名表可以使用`rename table`语句。

```sql
rename table customers to customersTest;
```

## 插入、更新、删除数据

### 插入数据

使用`inster`来插入或添加行到数据库表中

- 插入完整的行
- 插入行的一部分
- 插入多行
- 插入某些查询的结果
- 在插入数据时，最好是显示要插入数据的列字段名称。
- 使用单条insert语句处理多个插入比使用多条insert语句块。

```sql
MariaDB [test]> insert into orders(order_date, cust_id) values(Now(), 10003),(Now(), 10004);
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

MariaDB [test]> select * from orders;
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     20005 | 2005-09-01 00:00:00 |   10001 |
|     20006 | 2005-09-12 00:00:00 |   10003 |
|     20007 | 2005-09-30 00:00:00 |   10004 |
|     20008 | 2005-10-03 00:00:00 |   10005 |
|     20009 | 2005-10-08 00:00:00 |   10001 |
|     30000 | 2006-10-27 00:00:00 |   10001 |
|     30001 | 2006-10-27 00:00:00 |   10001 |
|     30002 | 2018-10-27 17:03:09 |   10002 |
|     30005 | 2018-10-27 17:06:47 |   10003 |
|     30006 | 2018-10-27 17:06:47 |   10004 |
+-----------+---------------------+---------+
10 rows in set (0.00 sec)
```

插入检索出来的数据

```sql
MariaDB [test]> select * from ordersTest;
Empty set (0.00 sec)

MariaDB [test]> insert into ordersTest(order_num, order_date, cust_id) select order_num, order_date, cust_id from orders where order_num > 20009;
Query OK, 5 rows affected (0.00 sec)
Records: 5  Duplicates: 0  Warnings: 0

MariaDB [test]> select * from ordersTest;
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     30000 | 2006-10-27 00:00:00 |   10001 |
|     30001 | 2006-10-27 00:00:00 |   10001 |
|     30002 | 2018-10-27 17:03:09 |   10002 |
|     30005 | 2018-10-27 17:06:47 |   10003 |
|     30006 | 2018-10-27 17:06:47 |   10004 |
+-----------+---------------------+---------+
5 rows in set (0.00 sec)
```

### 更新数据

使用`update`语句用来更新表中的数据

- 更新表中特定的行
- 更新表中所有的行

使用的步骤

- 要更新的表名；
- 列名和它们的新值；
- 确定要更新行的过滤条件。

```sql
MariaDB [test]> update ordersTest set cust_id = 10005;
Query OK, 5 rows affected (0.00 sec)
Rows matched: 5  Changed: 5  Warnings: 0

MariaDB [test]> select * from ordersTest;
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     30000 | 2006-10-27 00:00:00 |   10005 |
|     30001 | 2006-10-27 00:00:00 |   10005 |
|     30002 | 2018-10-27 17:03:09 |   10005 |
|     30005 | 2018-10-27 17:06:47 |   10005 |
|     30006 | 2018-10-27 17:06:47 |   10005 |
+-----------+---------------------+---------+
5 rows in set (0.00 sec)
```

### 删除数据

使用`delete`语句进行删除操作，如果需要指定特定的行进行删除，需要提供`where`子句。

```sql
MariaDB [test]> delete from ordersTest;
Query OK, 5 rows affected (0.00 sec)

MariaDB [test]> select * from ordersTest;
Empty set (0.00 sec)
```