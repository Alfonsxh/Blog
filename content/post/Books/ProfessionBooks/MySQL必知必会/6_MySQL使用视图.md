---
title: "MySQL必知必会 - 使用视图"
date: 2018-10-29 21:21:59
lastmod: 2018-10-29 21:21:59
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "使用视图"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

视图是虚拟的表，仅仅是用来查看存储在别处的数据的一种设施，视图本身不包含数据，它们返回的数据是从其他表中检索出来的，在添加或更改这些表中的数据时，视图将返回改变后的数据。

视图的应用：

- 主要同于数据检索(select 语句)，而不用于更新(insert、update和delete)
- 重用SQL语句
- 简化复杂的SQL操作。在编写查询后，可以方便地重用它而不必知道它的基本查询细节
- 使用表的组成部分而不是整个表
- 保护数据。可以给用户授予表的特定部分的访问权限而不是整个表的访问权限
- 更改数据格式和表时。视图可返回与底层表的表示和格式不同的数据
  
性能问题：每次使用视图时，都必须处理查询执行时所需的任一个检索。

<!--more-->

## 创建视图

使用`create view VIEW_NAME as *`来创建视图。

```sql
MariaDB [test]> create view productcustomers
                as
                select cust_name, cust_contact, prod_id
                from customers, orders, orderitems
                where customers.cust_id = orders.cust_id and orderitems.order_num = orders.order_num;
Query OK, 0 rows affected (0.01 sec)

MariaDB [test]> select cust_name, cust_contact, prod_id from productcustomers;
+----------------+--------------+---------+
| cust_name      | cust_contact | prod_id |
+----------------+--------------+---------+
| Coyote Inc.    | Y Lee        | ANV01   |
| Coyote Inc.    | Y Lee        | ANV02   |
| Coyote Inc.    | Y Lee        | TNT2    |
| Coyote Inc.    | Y Lee        | FB      |
| Coyote Inc.    | Y Lee        | FB      |
| Coyote Inc.    | Y Lee        | OL1     |
| Coyote Inc.    | Y Lee        | SLING   |
| Coyote Inc.    | Y Lee        | ANV03   |
| Wascals        | Jim Jones    | JP2000  |
| Yosemite Place | Y Sam        | TNT2    |
| E Fudd         | E Fudd       | FC      |
+----------------+--------------+---------+
11 rows in set (0.00 sec)
```

视图种嵌套视图。

```sql
MariaDB [test]> create view tntproduct
                as
                select * from productcustomers where prod_id = "tnt2";
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> select * from tntproduct;
+----------------+--------------+---------+
| cust_name      | cust_contact | prod_id |
+----------------+--------------+---------+
| Coyote Inc.    | Y Lee        | TNT2    |
| Yosemite Place | Y Sam        | TNT2    |
+----------------+--------------+---------+
2 rows in set (0.01 sec)
```

## 查看视图

使用`show create view VIEW_NAME`可以查看创建视图的语句。

```sql
MariaDB [test]> show create view productcustomers;
+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| View             | Create View                                                                                                                                                                                                                                                                                                                                                                                          | character_set_client | collation_connection |
+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
| productcustomers | CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `productcustomers` AS select `customers`.`cust_name` AS `cust_name`,`customers`.`cust_contact` AS `cust_contact`,`orderitems`.`prod_id` AS `prod_id` from ((`customers` join `orders`) join `orderitems`) where ((`customers`.`cust_id` = `orders`.`cust_id`) and (`orderitems`.`order_num` = `orders`.`order_num`)) | utf8                 | utf8_general_ci      |
+------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+----------------------+
1 row in set (0.00 sec)
```

## 修改视图

使用`creat or replace view VIEW_NAME *`来修改数据库中已存在的视图，如果不存在该视图，则会新建视图。

```sql
MariaDB [test]> create or replace view productcustomers
                as
                select cust_name as cn, cust_contact as cc, prod_id as pi
                from customers, orders, orderitems
                where customers.cust_id = orders.cust_id and orderitems.order_num = orders.order_num;
Query OK, 0 rows affected (0.01 sec)

MariaDB [test]> select * from productcustomers;
+----------------+-----------+--------+
| cn             | cc        | pi     |
+----------------+-----------+--------+
| Coyote Inc.    | Y Lee     | ANV01  |
| Coyote Inc.    | Y Lee     | ANV02  |
| Coyote Inc.    | Y Lee     | TNT2   |
| Coyote Inc.    | Y Lee     | FB     |
| Coyote Inc.    | Y Lee     | FB     |
| Coyote Inc.    | Y Lee     | OL1    |
| Coyote Inc.    | Y Lee     | SLING  |
| Coyote Inc.    | Y Lee     | ANV03  |
| Wascals        | Jim Jones | JP2000 |
| Yosemite Place | Y Sam     | TNT2   |
| E Fudd         | E Fudd    | FC     |
+----------------+-----------+--------+
11 rows in set (0.00 sec)
```

## 删除视图

使用`drop view VIEW_NAME`来删除视图。

```sql
MariaDB [test]> drop view productcustomers;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test]> select * from productcustomers;
ERROR 1146 (42S02): Table 'test.productcustomers' doesn't exist
```