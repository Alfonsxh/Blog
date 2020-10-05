---
title: "MySQL必知必会 - 使用存储过程"
date: 2018-10-29 21:21:59
lastmod: 2018-10-29 21:21:59
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "使用存储过程"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

`存储过程(Stored Procedure)`：一组可编程的函数，是为了完成特定功能的SQL语句集，经`编译`创建并`保存在数据库中`，用户可通过指定存储过程的名字并给定参数(需要时)来调用执行。

为什么需要使用存储过程：

- 简单、安全、高性能。
- 将重复性很高的一些操作，封装到一个存储过程中，简化了对这些SQL的调用。
- 不要求反复建立一系列处理步骤，保证了数据的完整性。
- 批量处理

<!--more-->

## 创建并使用存储过程

使用`create procedure FUNC`来创建存储过程。

```sql
MariaDB [test]> delimiter //        # 修改束标识为//
MariaDB [test]> create procedure productprincing()
                begin
                    select avg(prod_price) as priceaverage
                    from products;
                end //
Query OK, 0 rows affected (0.01 sec)

MariaDB [test]> delimiter ;     # 修改结束标识为;
MariaDB [test]> call productprincing();         # 调用存储过程
+--------------+
| priceaverage |
+--------------+
|    16.133571 |
+--------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.00 sec)
```

在创建存储过程时，还可以加入参数

- `IN输入参数`：表示调用者向过程传入值
- `OUT输出参数`：表示过程向调用者传出值(可以返回多个值)
- `INOUT输入输出参数`：既表示调用者向过程传入值，又表示过程向调用者传出值

```sql
MariaDB [test]> delimiter //
MariaDB [test]> create procedure MaxPrice(      # 获取特定vend_id下最高价格
                    in vendId int,
                    out maxPrice decimal(8,2)
                )
                begin
                    select max(prod_price)
                    from products
                    where vend_id = vendId
                    into maxPrice;
                end//
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> call MaxPrice(1001, @max)//
Query OK, 1 row affected (0.01 sec)

MariaDB [test]> select @max//
+-------+
| @max  |
+-------+
| 14.99 |
+-------+
1 row in set (0.00 sec)
```

## 删除存储过程

使用`drop procedure FUNC`来删除存储过程。

```sql
MariaDB [test]> drop procedure if exists MaxPrice//
Query OK, 0 rows affected (0.00 sec)
```