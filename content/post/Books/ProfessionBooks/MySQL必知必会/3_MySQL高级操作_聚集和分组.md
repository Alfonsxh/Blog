---
title: "MySQL必知必会 - 聚集和分组"
date: 2018-10-29 21:21:59
lastmod: 2018-10-29 21:21:59
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "聚集和分组"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

## 创建计算字段

`Concat()`函数用来拼接不同的列。

`as`关键字用来给字段或值取一个别名。 

```sql
MariaDB [test]> select concat(vend_name, '(', vend_country, ')') as vend_title from vendors;
+------------------------+
| vend_title             |
+------------------------+
| Anvils R Us(USA)       |
| LT Supplies(USA)       |
| ACME(USA)              |
| Furball Inc.(USA)      |
| Jet Set(England)       |
| Jouets Et Ours(France) |
+------------------------+
6 rows in set (0.00 sec)
```

<!--more-->

MySQL算术操作符

|操作符|说明|
|:---:|:---:|
|+|加|
|-|减|
|*|乘|
|/|除|

```sql
MariaDB [test]> select * from orderitems;
+-----------+------------+---------+----------+------------+
| order_num | order_item | prod_id | quantity | item_price |
+-----------+------------+---------+----------+------------+
|     20005 |          1 | ANV01   |       10 |       5.99 |
|     20005 |          2 | ANV02   |        3 |       9.99 |
|     20005 |          3 | TNT2    |        5 |      10.00 |
|     20005 |          4 | FB      |        1 |      10.00 |
|     20006 |          1 | JP2000  |        1 |      55.00 |
|     20007 |          1 | TNT2    |      100 |      10.00 |
|     20008 |          1 | FC      |       50 |       2.50 |
|     20009 |          1 | FB      |        1 |      10.00 |
|     20009 |          2 | OL1     |        1 |       8.99 |
|     20009 |          3 | SLING   |        1 |       4.49 |
|     20009 |          4 | ANV03   |        1 |      14.99 |
+-----------+------------+---------+----------+------------+
11 rows in set (0.00 sec)

MariaDB [test]> select *,quantity*item_price as expanded_price from orderitems;
+-----------+------------+---------+----------+------------+----------------+
| order_num | order_item | prod_id | quantity | item_price | expanded_price |
+-----------+------------+---------+----------+------------+----------------+
|     20005 |          1 | ANV01   |       10 |       5.99 |          59.90 |
|     20005 |          2 | ANV02   |        3 |       9.99 |          29.97 |
|     20005 |          3 | TNT2    |        5 |      10.00 |          50.00 |
|     20005 |          4 | FB      |        1 |      10.00 |          10.00 |
|     20006 |          1 | JP2000  |        1 |      55.00 |          55.00 |
|     20007 |          1 | TNT2    |      100 |      10.00 |        1000.00 |
|     20008 |          1 | FC      |       50 |       2.50 |         125.00 |
|     20009 |          1 | FB      |        1 |      10.00 |          10.00 |
|     20009 |          2 | OL1     |        1 |       8.99 |           8.99 |
|     20009 |          3 | SLING   |        1 |       4.49 |           4.49 |
|     20009 |          4 | ANV03   |        1 |      14.99 |          14.99 |
+-----------+------------+---------+----------+------------+----------------+
11 rows in set (0.00 sec)
```

## 使用函数

`SQL`支持利用函数来处理数据，函数一般在数据上执行，它给数据的转换和处理提供了方便。

### 文本处理函数

|函数|说明|
|:---|:---|
|Left(string, number_of_chars)|返回串左边的字符|
|Right(string, number_of_chars)|返回串右边的字符|
|Length(string)|返回串的长度|
|Locate(string)|找出串的一个子串|
|Lower(string)|将串转换为小写|
|Upper(string)|将串转换为大写|
|LTrim(string)|去掉串左侧的空格|
|RTrim(string)|去掉串右侧的空格|
|Soundex(string)|返回串的语音值！！|
|SubString(string, start, length)|返回子串的字符|

```sql
MariaDB [test]> select cust_name, cust_contact from customers where cust_contact = "Y lie";
Empty set (0.00 sec)

MariaDB [test]> select cust_name, cust_contact from customers where soundex(cust_contact) = soundex("Y lie"); # soundex() 函数将输入转换为语音编码，通过这种方式找到听起来像的值匹配。
+-------------+--------------+
| cust_name   | cust_contact |
+-------------+--------------+
| Coyote Inc. | Y Lee        |
+-------------+--------------+
1 row in set (0.01 sec)

MariaDB [test]> select SubString(cust_name, 1, 5) from customers; # 选择从第一个字符开始的五个字符
+----------------------------+
| SubString(cust_name, 1, 5) |
+----------------------------+
| Coyot                      |
| Mouse                      |
| Wasca                      |
| Yosem                      |
| E Fud                      |
+----------------------------+
5 rows in set (0.00 sec)
```

### 日期和时间处理函数

日期和时间采用相应的数据类型和特数的格式存储，以便能快速和有效地排序或过滤，并且节省物理存储空间。

|函数|说明|
|:---|:---|
|AddDate()|增加一个日期(天、周等)|
|AddTime()|增加一个时间(时、分等)|
|CurDate()|返回当前日期|
|CurTime()|返回当前时间|
|DateDiff()|计算两个日期之差|
|Date_Add()|高度灵活的日期运算函数|
|Date_Format()|返回一个格式化的日期或字符串|
|DayOfWeek()|对于一个日期，返回对应的星期几|
|Now()|返回当前的日期和时间|
|Date()|返回如期时间的日期部分|
|Year()|返回一个日期的年份部分|
|Month()|返回一个日期的月份部分|
|Day()|返回一个日期的天数部分|
|Time()|返回一个日期时间的时间部分|
|Second()|返回一个时间的秒部分|
|Minute()|返回一个时间的分钟部分|
|Hour()|返回一个时间的小时部分|

```sql
MariaDB [test]> select * from orders;
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     20005 | 2005-09-01 00:00:00 |   10001 |
|     20006 | 2005-09-12 00:00:00 |   10003 |
|     20007 | 2005-09-30 00:00:00 |   10004 |
|     20008 | 2005-10-03 00:00:00 |   10005 |
|     20009 | 2005-10-08 00:00:00 |   10001 |
+-----------+---------------------+---------+
5 rows in set (0.00 sec)

MariaDB [test]> select order_num, AddDate(order_date,interval 1 second) as order_date, cust_id from orders;
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     20005 | 2005-09-01 00:00:01 |   10001 |
|     20006 | 2005-09-12 00:00:01 |   10003 |
|     20007 | 2005-09-30 00:00:01 |   10004 |
|     20008 | 2005-10-03 00:00:01 |   10005 |
|     20009 | 2005-10-08 00:00:01 |   10001 |
+-----------+---------------------+---------+
5 rows in set (0.00 sec)

MariaDB [test]> select * from orders where date(order_date) between "2005-09-11" and "2005-10-04";  # 如果想要的只是日期，则使用date()函数
+-----------+---------------------+---------+
| order_num | order_date          | cust_id |
+-----------+---------------------+---------+
|     20006 | 2005-09-12 00:00:00 |   10003 |
|     20007 | 2005-09-30 00:00:00 |   10004 |
|     20008 | 2005-10-03 00:00:00 |   10005 |
+-----------+---------------------+---------+
3 rows in set (0.00 sec)
```

### 数值处理函数

|函数|说明|
|:---|:---|
|Abs()|返回一个数的绝对值|
|Cos()|返回一个角度的余弦|
|Exp()|返回一个书店指数值|
|Mod()|返回余数|
|Pi()|返回圆周率|
|Rand()|返回一个随机数|
|Sin()|返回一个角度的正弦|
|Sqrt()|返回一个数的平方根|
|Tan()|返回一个角度的正切|

### 聚集函数

用于统计行组上。

|函数|说明|
|:---|:---|
|AVG()|返回某列的平均值|
|COUNT()|返回某列的行数|
|MAX()|返回某列的最大值|
|MIN()|返回某列的最小值|
|SUM()|返回某列值之和|

```sql
MariaDB [test]> select avg(prod_price) as avg_price from products where vend_id = 1001; # 返回指定厂商产品的平均价格
+-----------+
| avg_price |
+-----------+
| 10.323333 |
+-----------+
1 row in set (0.00 sec)

MariaDB [test]> select count(*) as num_cust from customers;
+----------+
| num_cust |
+----------+
|        5 |
+----------+
1 row in set (0.00 sec)
```

在使用聚集函数时吗，默认是对所有的值进行处理，`DISTINCT`关键字的作用是，剔除那些相同的值。

```sql
MariaDB [test]> select avg(prod_price) as avg_price from products where vend_id = 1003;
+-----------+
| avg_price |
+-----------+
| 13.212857 |
+-----------+
1 row in set (0.00 sec)

MariaDB [test]> select avg(distinct prod_price) as avg_price from products where vend_id = 1003;
+-----------+
| avg_price |
+-----------+
| 15.998000 |
+-----------+
1 row in set (0.00 sec)
```

select语句可以根据需要不同的需求组合聚集函数。

```sql
MariaDB [test]> select count(*) as num_items, min(prod_price) as price_min, max(prod_price) as price_max, avg(prod_price) as price_avg from products;
+-----------+-----------+-----------+-----------+
| num_items | price_min | price_max | price_avg |
+-----------+-----------+-----------+-----------+
|        14 |      2.50 |     55.00 | 16.133571 |
+-----------+-----------+-----------+-----------+
1 row in set (0.00 sec)
```

### 小结

MySQL支持一系列的聚集函数，可以使用多种方法使用他们以返回所需的结果。MySQL内部的聚集函数比一般在客户端应用程序中的函数高效。

## 数据分组

### GROUP BY

分组是在select语句的`GROUP BY`子句中建立的。`GROUP BY`子句指示MySQL分组数据，然后对`每个组`而不是整个结果集进行聚集。

```sql
MariaDB [test]> select vend_id, count(*) as prod_num from products; 
+---------+----------+
| vend_id | prod_num |
+---------+----------+
|    1001 |       14 |
+---------+----------+
1 row in set (0.00 sec)

MariaDB [test]> select vend_id, count(*) as prod_num from products group by vend_id; 
+---------+----------+
| vend_id | prod_num |
+---------+----------+
|    1001 |        3 |
|    1002 |        2 |
|    1003 |        7 |
|    1005 |        2 |
+---------+----------+
4 rows in set (0.00 sec)

MariaDB [test]> select vend_id, count(*) as prod_num from products group by vend_id, prod_price; 
+---------+----------+
| vend_id | prod_num |
+---------+----------+
|    1001 |        1 |
|    1001 |        1 |
|    1001 |        1 |
|    1002 |        1 |
|    1002 |        1 |
|    1003 |        2 |
|    1003 |        1 |
|    1003 |        2 |
|    1003 |        1 |
|    1003 |        1 |
|    1005 |        1 |
|    1005 |        1 |
+---------+----------+
12 rows in set (0.00 sec)
```

在使用`GROUP BY`子句前，需要注意一些规定。

- `GROUP BY`子句可以包含任意数目的列。
- `GROUP BY`子句可以使用多个列进行分组，同`ORDER BY`子句的规则类似。
- `GROUP BY`子句必须出现在`WHERE`子句之后，`ORDER BY`子句之前。

### HAVING

`HAVING`关键字用来过滤分组。

`HAVING`支持所有的`WHERE`操作符。

`HAVING`和`WHERE`最大的区别在于，`WHERE`在数据分组前进行过滤，`HAVING`在数据分组后进行过滤。

```sql
MariaDB [test]> select vend_id, count(*) as prod_num from products group by vend_id; # 仅分组
+---------+----------+
| vend_id | prod_num |
+---------+----------+
|    1001 |        3 |
|    1002 |        2 |
|    1003 |        7 |
|    1005 |        2 |
+---------+----------+
4 rows in set (0.00 sec)

MariaDB [test]> select vend_id, count(*) as prod_num from products group by vend_id having count(*) >= 3; # 通过having过滤
+---------+----------+
| vend_id | prod_num |
+---------+----------+
|    1001 |        3 |
|    1003 |        7 |
+---------+----------+
2 rows in set (0.00 sec)

MariaDB [test]> select vend_id, count(*) as prod_num from products where prod_price >= 10 group by vend_id having count(*) >= 3; # 经过where过滤后再经过having过滤
+---------+----------+
| vend_id | prod_num |
+---------+----------+
|    1003 |        4 |
+---------+----------+
1 row in set (0.00 sec)
```

## select子句顺序

|子句|说明|是否必须使用|
|:---|:---|:---|
|SELECT|要返回的列或表达式|是|
|FROM|从中检索的表名|仅在从表中选择数据时使用|
|WHERE|行级过滤|否|
|GROUP BY|分组说明|尽在按组计算聚集时使用|
|HAVING|组级过滤|否|
|ORDER BY|输出排序|否|
|LIMIT|要检索的行数|否|