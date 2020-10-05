---
title: "MySQL必知必会 - 使用索引"
date: 2018-11-05 22:03:45
lastmod: 2018-11-06 23:14:51
draft: false
keywords: ["Books", "MySQL必知必会"]
description: "使用索引"
tags: ["Books", "MySQL必知必会"]
categories: ["Books", "MySQL必知必会"]
author: "Alfons"
---

在数据库中使用索引的目的是为了在查询大数量数据的时候，提升查询效率。

- 索引也是一种表，保存着主键或索引字段，以及一个能将每个记录指向实际表的指针。
- 数据库用户是看不到索引的，它们只是用来加速查询的。
- 数据库搜索引擎使用索引来快速定位记录。

<!--more-->

## 索引的原理

mysql中普遍使用B+Tree做索引。

![btree](/images/Books/ProfessionBooks/MySQL必知必会/btree.jpg)

如果要查找数据项29，在有索引的情况下，只需进行三次IO操作就能找到29对应的项在磁盘中的位置。而在不使用索引的情况下，如果数据量很大的话，那么查找数据项29，则要经过多次的IO操作才能找到对应的项在磁盘中的位置。

## 索引创建

索引的类型：

- **UNIQUE(唯一索引)**：不可以出现相同的值，可以有NULL值。
- **INDEX(普通索引)**：允许出现相同的索引内容。
- **PROMARY KEY(主键索引)**：不允许出现相同的值。
- **FULLTEXT(全文索引)**：可以针对值中的某个单词，但效率不高。
- 组合索引：实质上是将多个字段建到一个索引里，列值的组合必须唯一。

可以在创建表结构时添加索引，也可以在创建完表结构后，使用 **ALTER TABLE** 或者 **CREATE INDEX** 来创建索引。

- **alter table table_name add index index_name (columns_name);**
- **create index on table_name (columns_name);**

```sql
# 1、在创建表时指定索引
MariaDB [test]> CREATE TABLE `customerstest` (
                    `cust_id` int(11) NOT NULL AUTO_INCREMENT,
                    `cust_name` char(50) NOT NULL,
                    `cust_address` char(50) DEFAULT NULL,
                    `cust_city` char(50) DEFAULT NULL,
                    `cust_state` char(5) DEFAULT NULL,
                    `cust_zip` char(10) DEFAULT NULL,
                    `cust_country` char(50) DEFAULT NULL,
                    `cust_contact` char(50) DEFAULT NULL,
                    `cust_email` char(255) DEFAULT NULL,
                    PRIMARY KEY (`cust_id`),
                    INDEX customerIndex (cust_name)
                ) ENGINE=InnoDB AUTO_INCREMENT=10006 DEFAULT CHARSET=latin1;

MariaDB [test]> show index from customerstest;
+---------------+------------+---------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table         | Non_unique | Key_name      | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+---------------+------------+---------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| customerstest |          0 | PRIMARY       |            1 | cust_id     | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerIndex |            1 | cust_name   | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
+---------------+------------+---------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
2 rows in set (0.00 sec)

# 2、使用 ALTER TABLE
mysql> alter table customerstest add index customerAlterIndex (cust_address);
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show index from customerstest;
+---------------+------------+--------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table         | Non_unique | Key_name           | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+---------------+------------+--------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| customerstest |          0 | PRIMARY            |            1 | cust_id      | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerIndex      |            1 | cust_name    | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerAlterIndex |            1 | cust_address | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
+---------------+------------+--------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
3 rows in set (0.01 sec)

# 3、使用 create index
mysql> create index customersCreatIndex on customerstest (cust_city);
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show index from customerstest;
+---------------+------------+---------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table         | Non_unique | Key_name            | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+---------------+------------+---------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| customerstest |          0 | PRIMARY             |            1 | cust_id      | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerIndex       |            1 | cust_name    | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerAlterIndex  |            1 | cust_address | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customersCreatIndex |            1 | cust_city    | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
+---------------+------------+---------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
4 rows in set (0.00 sec)

# 4、唯一索引 unique
mysql> create unique index customersUniqueIndex on customerstest (cust_state);

create table test.customerstest
(
  cust_id      int auto_increment
    primary key,
  cust_name    char(50)  not null,
  cust_address char(50)  null,
  cust_city    char(50)  null,
  cust_state   char(5)   null,
  cust_zip     char(10)  null,
  cust_country char(50)  null,
  cust_contact char(50)  null,
  cust_email   char(255) null,
  constraint customersUniqueIndex unique (cust_state)   # 在数据库表的DDL中，新增呢唯一索引标识
);

# 5、组合索引
mysql> create index customersTogtherIndex on customerstest (cust_state, cust_zip, cust_country);
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show index from customerstest;
+---------------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table         | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+---------------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| customerstest |          0 | PRIMARY               |            1 | cust_id      | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          0 | customersUniqueIndex  |            1 | cust_state   | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customerIndex         |            1 | cust_name    | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerAlterIndex    |            1 | cust_address | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customersCreatIndex   |            1 | cust_city    | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customersTogtherIndex |            1 | cust_state   | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customersTogtherIndex |            2 | cust_zip     | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customersTogtherIndex |            3 | cust_country | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
+---------------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
8 rows in set (0.00 sec)
```

## 删除索引

使用 **drop** 命令删除索引。

- **drop index index_name on table_name;**
- **alter table table_name drop index index_name;**

```sql
mysql> drop index customersTogtherIndex on customerstest;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show keys from customerstest;
+---------------+------------+----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table         | Non_unique | Key_name             | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+---------------+------------+----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| customerstest |          0 | PRIMARY              |            1 | cust_id      | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          0 | customersUniqueIndex |            1 | cust_state   | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customerIndex        |            1 | cust_name    | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customerAlterIndex   |            1 | cust_address | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customersCreatIndex  |            1 | cust_city    | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
+---------------+------------+----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
5 rows in set (0.00 sec)

mysql> alter table customerstest drop index customerAlterIndex;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show keys from customerstest;
+---------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table         | Non_unique | Key_name             | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+---------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| customerstest |          0 | PRIMARY              |            1 | cust_id     | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          0 | customersUniqueIndex |            1 | cust_state  | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
| customerstest |          1 | customerIndex        |            1 | cust_name   | A         |           0 |     NULL | NULL   |      | BTREE      |         |               |
| customerstest |          1 | customersCreatIndex  |            1 | cust_city   | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               |
+---------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
4 rows in set (0.00 sec)
```

## 索引使用建议

- 尽量避免Like的参数以通配符开头，否则数据库引擎会放弃使用索引而进行全表扫描。
- where条件不符合最左前缀原则时，即where子句的条件，最先出现的条件不是索引的字段。
- 尽量避免使用！= 或 <>操作符，否则数据库引擎会放弃使用索引而进行全表扫描。使用>或<会比较高效。
- 应尽量避免在 where 子句中对字段进行表达式操作，这将导致引擎放弃使用索引而进行全表扫描。例如 where index_t + 1 > num;
- 应尽量避免在where子句中对字段进行null值判断，否则将导致引擎放弃使用索引而进行全表扫描。
- 应尽量避免在where子句中使用or来连接条件，否则将导致引擎放弃使用索引而进行全表扫描。使用 **union all** 代替。

## 参考

[MySQL 索引及查询优化总结](https://cloud.tencent.com/developer/article/1004912)