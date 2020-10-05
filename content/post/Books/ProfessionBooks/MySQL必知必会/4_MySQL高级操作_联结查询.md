---
title: "MySQL必知必会 - 联结查询"
date: 2018-10-29 21:21:59
lastmod: 2018-10-29 21:21:59
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "联结查询"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

## 子查询

SQL允许创建子查询，即嵌套在其他查询中的查询。

```sql
MariaDB [test]> select cust_name, cust_contact from customers where cust_id in (select cust_id from orders where order_num in (select order_num from orderitems where prod_id = "TNT2"));
+----------------+--------------+
| cust_name      | cust_contact |
+----------------+--------------+
| Coyote Inc.    | Y Lee        |
| Yosemite Place | Y Sam        |
+----------------+--------------+
2 rows in set (0.00 sec)
```

子查询还可以根据外部表中的字段对本表进行过滤。

<!--more-->

```sql
MariaDB [test]> select cust_name, cust_state, (select count(*)
    ->                                         from orders where customers.cust_id = orders.cust_id) as orders
    ->          from customers group by cust_name;
+----------------+------------+--------+
| cust_name      | cust_state | orders |
+----------------+------------+--------+
| Coyote Inc.    | MI         |      2 |
| E Fudd         | IL         |      1 |
| Mouse House    | OH         |      0 |
| Wascals        | IN         |      1 |
| Yosemite Place | AZ         |      1 |
+----------------+------------+--------+
5 rows in set (0.00 sec)
```

## 联结

`联结`是利用sql的select能执行的最重要的操作，很好地理解联结及其语法是学习sql的一个极为重要的组成部分

`联结`是一种机制，用来在一条select与剧中关联表，使用特殊的语法，可以联结多个表返回一组输出，联结在运行时关联表中正确的行。

### 创建联结

```sql
MariaDB [test]> select vend_name, prod_name, prod_price from vendors, products where vendors.vend_id = products.vend_id order by vend_name, prod_name;
+-------------+----------------+------------+
| vend_name   | prod_name      | prod_price |
+-------------+----------------+------------+
| ACME        | Bird seed      |      10.00 |
| ACME        | Carrots        |       2.50 |
| ACME        | Detonator      |      13.00 |
| ACME        | Safe           |      50.00 |
| ACME        | Sling          |       4.49 |
| ACME        | TNT (1 stick)  |       2.50 |
| ACME        | TNT (5 sticks) |      10.00 |
| Anvils R Us | .5 ton anvil   |       5.99 |
| Anvils R Us | 1 ton anvil    |       9.99 |
| Anvils R Us | 2 ton anvil    |      14.99 |
| Jet Set     | JetPack 1000   |      35.00 |
| Jet Set     | JetPack 2000   |      55.00 |
| LT Supplies | Fuses          |       3.42 |
| LT Supplies | Oil can        |       8.99 |
+-------------+----------------+------------+
14 rows in set (0.00 sec)
```

上面的操作是，从vendors中找出厂商的名字与products表中的数据组合。此处需使用完全限定名，否则无法分辨字段属于哪张表。

在联结两个表时，实际上是将第一个表中的每一行与第二个表中的每一行配对。where子句作为过滤条件，它只包含那些匹配给定条件(这里是联结条件)的行。

如果没有给定联结条件`vendors.vend_id = products.vend_id`，将返回两张表的笛卡儿积。

```sql
MariaDB [test]> select vend_name, prod_name, prod_price from vendors, products order by vend_name, prod_name;
+----------------+----------------+------------+
| vend_name      | prod_name      | prod_price |
+----------------+----------------+------------+
| ACME           | .5 ton anvil   |       5.99 |
| ACME           | 1 ton anvil    |       9.99 |
| ACME           | 2 ton anvil    |      14.99 |
| ACME           | Bird seed      |      10.00 |
| ACME           | Carrots        |       2.50 |
| ACME           | Detonator      |      13.00 |
| ACME           | Fuses          |       3.42 |
| ACME           | JetPack 1000   |      35.00 |
| ACME           | JetPack 2000   |      55.00 |
| ACME           | Oil can        |       8.99 |
| ACME           | Safe           |      50.00 |
| ACME           | Sling          |       4.49 |
| ACME           | TNT (1 stick)  |       2.50 |
| ACME           | TNT (5 sticks) |      10.00 |
| Anvils R Us    | .5 ton anvil   |       5.99 |
| Anvils R Us    | 1 ton anvil    |       9.99 |
| Anvils R Us    | 2 ton anvil    |      14.99 |
| Anvils R Us    | Bird seed      |      10.00 |
| Anvils R Us    | Carrots        |       2.50 |
| Anvils R Us    | Detonator      |      13.00 |
| Anvils R Us    | Fuses          |       3.42 |
| Anvils R Us    | JetPack 1000   |      35.00 |
······
+----------------+----------------+------------+
84 rows in set (0.00 sec)
```

> 应该保证所有联结都有where子句，否则MySQL将返回比想要的数据多得多的数据。

### 多表联结

下面的例子执行的结果都是返回订购产品"TNT2"的客户列表，不同之处在于第一条语句使用了三次where子句条件，第二条语句使用了两次联结操作，语法更简洁明了。

```sql
MariaDB [test]> select cust_name, cust_contact
                from customers
                where cust_id in (select cust_id
                                  from orders
                                  where order_num in (select order_num
                                                      from orderitems
                                                      where prod_id = "TNT2"));
+----------------+--------------+
| cust_name      | cust_contact |
+----------------+--------------+
| Coyote Inc.    | Y Lee        |
| Yosemite Place | Y Sam        |
+----------------+--------------+
2 rows in set (0.00 sec)

MariaDB [test]> select cust_name, cust_contact
                from customers, orders, orderitems
                where customers.cust_id = orders.cust_id
                and orders.order_num = orderitems.order_num
                and orderitems.prod_id = "TNT2";
+----------------+--------------+
| cust_name      | cust_contact |
+----------------+--------------+
| Coyote Inc.    | Y Lee        |
| Yosemite Place | Y Sam        |
+----------------+--------------+
2 rows in set (0.00 sec)

```

## 高级联结

### 自联结

sql除了可以给列名和计算字段起别名外，还允许给表名起别名。这样做能够缩短sql语句，同时允许在单条select语句中多次使用相同的表。

如下面的例子，找出生产 **TNT2** 产品的厂商的所有产品。

此处要注意的是当使用 **p1.prod_id, p1.prod_name** 作为列展示时，where子句中的过滤条件不能为 **p2.prod_id = "TNT2"**，否则得不到正确的结果。

```sql
MariaDB [test]> select prod_id, prod_name
                from products
                where vend_id in (select vend_id
                                  from products
                                  where prod_id = "TNT2");
+---------+----------------+
| prod_id | prod_name      |
+---------+----------------+
| DTNTR   | Detonator      |
| FB      | Bird seed      |
| FC      | Carrots        |
| SAFE    | Safe           |
| SLING   | Sling          |
| TNT1    | TNT (1 stick)  |
| TNT2    | TNT (5 sticks) |
+---------+----------------+
7 rows in set (0.01 sec)

MariaDB [test]> select p1.prod_id, p1.prod_name
                from products as p1, products as p2
                where p1.vend_id = p2.vend_id and p2.prod_id = "TNT2";
+---------+----------------+
| prod_id | prod_name      |
+---------+----------------+
| DTNTR   | Detonator      |
| FB      | Bird seed      |
| FC      | Carrots        |
| SAFE    | Safe           |
| SLING   | Sling          |
| TNT1    | TNT (1 stick)  |
| TNT2    | TNT (5 sticks) |
+---------+----------------+
7 rows in set (0.00 sec)

MariaDB [test]> select p1.prod_id, p1.prod_name
                from products as p1, products as p2
                where p1.vend_id = p2.vend_id and p1.prod_id = "TNT2";
+---------+----------------+
| prod_id | prod_name      |
+---------+----------------+
| TNT2    | TNT (5 sticks) |
| TNT2    | TNT (5 sticks) |
| TNT2    | TNT (5 sticks) |
| TNT2    | TNT (5 sticks) |
| TNT2    | TNT (5 sticks) |
| TNT2    | TNT (5 sticks) |
| TNT2    | TNT (5 sticks) |
+---------+----------------+
7 rows in set (0.00 sec)
```

> 用自联结而不用子查询，自联结通常作为外部语句用来代替从相同表中检索数据时使用的子查询语句，处理联结的速度远比处理子查询快。

### 内部联结与外部联结

`inner join`关键字为内部联结，使用效果和where子句的效果一样。

`left outer join` 或 `right outer join` 为外部联结。外部联结能够得到得到所有的结果，关键在于关键字`left`和`right`。

在语句 **from customers left outer join orders** 中，会匹配customers表中所有的数据，如果条件不匹配，则其他字段使用 **NULL** 填充。

`right`同`left`，只是主表位置在右侧。

```sql
MariaDB [test]> select customers.cust_id, orders.order_num
                from orders, customers
                where customers.cust_id = orders.cust_id;
+---------+-----------+
| cust_id | order_num |
+---------+-----------+
|   10001 |     20005 |
|   10001 |     20009 |
|   10003 |     20006 |
|   10004 |     20007 |
|   10005 |     20008 |
+---------+-----------+
5 rows in set (0.00 sec)

MariaDB [test]> select customers.cust_id, orders.order_num
                from customers inner join orders on customers.cust_id = orders.cust_id;
+---------+-----------+
| cust_id | order_num |
+---------+-----------+
|   10001 |     20005 |
|   10001 |     20009 |
|   10003 |     20006 |
|   10004 |     20007 |
|   10005 |     20008 |
+---------+-----------+
5 rows in set (0.00 sec)

MariaDB [test]> select customers.cust_id, orders.order_num
                from customers left outer join orders on customers.cust_id = orders.cust_id;
+---------+-----------+
| cust_id | order_num |
+---------+-----------+
|   10001 |     20005 |
|   10001 |     20009 |
|   10002 |      NULL |
|   10003 |     20006 |
|   10004 |     20007 |
|   10005 |     20008 |
+---------+-----------+
6 rows in set (0.00 sec)

MariaDB [test]> select customers.cust_id, orders.order_num
                from customers right outer join orders on customers.cust_id = orders.cust_id;
+---------+-----------+
| cust_id | order_num |
+---------+-----------+
|   10001 |     20005 |
|   10001 |     20009 |
|   10003 |     20006 |
|   10004 |     20007 |
|   10005 |     20008 |
+---------+-----------+
5 rows in set (0.00 sec)
```

### 组合查询

- 在单个查询中从不同的表返回类似结构的数据；
- 对单个表执行多个查询，按单个查询返回数据。

```sql
MariaDB [test]> select vend_id, prod_id, prod_price from products where prod_price <= 5;
+---------+---------+------------+
| vend_id | prod_id | prod_price |
+---------+---------+------------+
|    1003 | FC      |       2.50 |
|    1002 | FU1     |       3.42 |
|    1003 | SLING   |       4.49 |
|    1003 | TNT1    |       2.50 |
+---------+---------+------------+
4 rows in set (0.00 sec)

MariaDB [test]> select vend_id, prod_id, prod_price from products where vend_id in (1001, 1002);
+---------+---------+------------+
| vend_id | prod_id | prod_price |
+---------+---------+------------+
|    1001 | ANV01   |       5.99 |
|    1001 | ANV02   |       9.99 |
|    1001 | ANV03   |      14.99 |
|    1002 | FU1     |       3.42 |
|    1002 | OL1     |       8.99 |
+---------+---------+------------+
5 rows in set (0.00 sec)
```

当使用`union`关键字连接两个select子句时，如果是在不同的表中使用，推荐使用`union`。相同表使用`and`或`or`等操作更简单。

```sql
MariaDB [test]> select vend_id, prod_id, prod_price from products where vend_id in (1001, 1002)
                union
                select vend_id, prod_id, prod_price from products where prod_price <= 5;
+---------+---------+------------+
| vend_id | prod_id | prod_price |
+---------+---------+------------+
|    1001 | ANV01   |       5.99 |
|    1001 | ANV02   |       9.99 |
|    1001 | ANV03   |      14.99 |
|    1002 | FU1     |       3.42 |
|    1002 | OL1     |       8.99 |
|    1003 | FC      |       2.50 |
|    1003 | SLING   |       4.49 |
|    1003 | TNT1    |       2.50 |
+---------+---------+------------+
8 rows in set (0.00 sec)

MariaDB [test]> select vend_id, prod_id, prod_price from products where vend_id in (1001, 1002) or prod_price <= 5;
+---------+---------+------------+
| vend_id | prod_id | prod_price |
+---------+---------+------------+
|    1001 | ANV01   |       5.99 |
|    1001 | ANV02   |       9.99 |
|    1001 | ANV03   |      14.99 |
|    1003 | FC      |       2.50 |
|    1002 | FU1     |       3.42 |
|    1002 | OL1     |       8.99 |
|    1003 | SLING   |       4.49 |
|    1003 | TNT1    |       2.50 |
+---------+---------+------------+
8 rows in set (0.00 sec)
```

默认情况下，`union`会自动去除重复的数据，如果想要展示所有的结果，需要使用`union all`。

```sql
MariaDB [test]> select vend_id, prod_id, prod_price from products where vend_id in (1001, 1002) 
                union all
                select vend_id, prod_id, prod_price from products where prod_price <= 5;
+---------+---------+------------+
| vend_id | prod_id | prod_price |
+---------+---------+------------+
|    1001 | ANV01   |       5.99 |
|    1001 | ANV02   |       9.99 |
|    1001 | ANV03   |      14.99 |
|    1002 | FU1     |       3.42 |
|    1002 | OL1     |       8.99 |
|    1003 | FC      |       2.50 |
|    1002 | FU1     |       3.42 |
|    1003 | SLING   |       4.49 |
|    1003 | TNT1    |       2.50 |
+---------+---------+------------+
9 rows in set (0.00 sec)
```

## 小结

- 注意使用的联结类型，一般使用内部联结。
- 保证使用正确的联结条件，否则将返回不正确的数据。
- 应该总是提供联结条件，否则会得到笛卡儿积。
- 在联结多个表时，最好分别测试每个联结。