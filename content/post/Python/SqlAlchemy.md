---
title: "SqlAlchemy使用"
date: 2019-01-28 14:17:43
lastmod: 2019-01-28 15:17:03
draft: false
keywords: ["Python", "SqlAlchemy"]
description: "SqlAlchemy使用"
tags: ["Python", "SqlAlchemy"]
categories: ["Python", "SqlAlchemy"]
author: "Alfons"
---

**SqlAlchemy(Sql炼金术？)** 是Python下的一款 **ORM(Object Relational Mapping 对象关系映射)框架**，框架建立在数据库API之上，使用关系对象映射进行数据库操作。将对象转换为sql，然后调用数据库API执行sql并获取结果。

<!--more-->

## pymysql

**pymysql** 是python下的一款数据库操作API模块，用户使用时，需要自己完成数据库连接、数据库语句编写、同步数据库、关闭数据库等操作。

基本操作流程如下：

- 1.创建数据库连接。
- 2.获取游标对象。
- 3.执行sql命令。
- 4.获取命令结果。
- 5.关闭数据库。

```python
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost","testuser","test123","TESTDB" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print ("Database version : %s " % data)

# 关闭数据库连接
db.close()
```

值得注意的是，在使用多线程进行操作同一数据库对象时，需要用户自行加锁，否则会出现下面的问题：

> mysql error sql: Packet sequence number wrong - got 1 expected 2
for this sql query:

解决问题的方式有两种：

- 每个线程使用独立的数据库连接对象，但这种方式在对于并发量特别大的时候，会造成很大的效率问题。
- 在操作数据库连接对象前，加锁。这种方式需要留心死锁问题，尤其是某些数据库操作调用了其他操作时。

还有另一种方案，使用 **SqlAlchemy**。

## SqlAlchemy Core

**SqlAlchemy** 在使用时有两种方式，一种是 **SQLAlchemy Core** 使用原生的sql语句对数据库进行操作，另一种为使用 **SQLAlchemy ORM** 的方式。

### 连接

**SqlAlchemy** 模块在使用时，需要有一个引擎负责和数据库服务器交互。

```python
from sqlalchemy import create_engine

engine = create_engine("dialect[+driver]://user:password@host/dbname[?key=value..]", echo = True)
```

连接不同的数据库需要不同的参数：

- **dialect** - 表示连接数据库的名字，可以为 **mysql**、**oracle**等等。
- **driver** - 可有可无，表示的是连接数据库所使用的API，对于mysql可以选择 **pyodbc**、**pymssql**、**pymysql**等。
- **user:password** - 数据库登陆的用户名和密码。
- **host/dbname** - 数据库的地址以及所使用的目标数据库的名字。
- **[?key=value..]** - 登陆数据库时的一些其他选项。

> **echo** 参数的意义是，为 **True** 时，会在执行语句时，打印出对应的sql执行语句。

#### 各类型数据库进行连接

PostgreSQL进行连接:

```python
# default
engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')

# psycopg2
engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

# pg8000
engine = create_engine('postgresql+pg8000://scott:tiger@localhost/mydatabase')
```

Mysql进行连接:

```python
# default
engine = create_engine('mysql://scott:tiger@localhost/foo')

# mysql-python
engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')

# MySQL-connector-python
engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')

# OurSQL
engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')
```

SQLite进行连接：

```python
# sqlite use memory
engine = create_engine('sqlite:///:memory:', echo=True)

# sqlite use file
engine=create_engine('sqlite:///./cnblogblog.db',echo=True)
```

### 定义和创建表

在 **SqlAlchemy** 中，列通常由对象 **Column** 关联，并且多条列被关联到一个 **Table** 对象。一个 **Table对象** 以及与它关联的 **子对象** 的集合被称为 **数据库元数据**。

我们所定义的 **Table对象** 都处于一个 **MetaData对象的目录中**。在使用 **Table对象** 创建表时，有两种方式，都和sql语句 **SQL CREATE TABLE** 类似。

```python
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

engine = create_engine("sqlite:///./memory.db", echo = True)

metadata = MetaData(engine)

# 第一种方式：table_obj.create()
users = Table("users", metadata,
              Column("id", Integer, autoincrement = True, default = 0, primary_key = True, comment = "用户ID"),
              Column("name", String, comment = "用户名"),
              Column("fullname", String, comment = "用户全名"))
users.create()

addresses = Table("addresses", metadata,
                  Column("id", Integer, primary_key = True),
                  Column("user_id", None, ForeignKey("users.id")),
                  Column("email_address", String, nullable = False)
                  )
addresses.create()

# 第二种方式：metadata.create_all(engine)
metadata.create_all(engine)
```

总结起来的步骤就是：

- 创建数据库引擎
- 定义元数据并绑定引擎
- 通过 **Table对象** 建表， **Column对象** 添加表字段
- 通过例子中的两种方式创建表结构

对于已经存在的表，可以使用 **autoload** 参数在加载时自动生成 **Table对象**。如下所示：

```python
users = Table("users", metadata, autoload = True)
addresses = Table("addresses", metadata, autoload = True)
```

### Insert操作

数据的插入有几种方式，主要区别在于待插入数据的设置方式。

```python
conn = engine.connect()

ins1 = users.insert(values = [dict(name = "alfons", fullname = "alfons_xh"), {"id": 1, "name": "alfons", "fullname": "alfons_xh"}])
conn.execute(ins1)

ins2 = users.insert().values([dict(id = 2, name = "alfons", fullname = "alfons_xh"), {"id": 3, "name": "alfons", "fullname": "alfons_xh"}])
conn.execute(ins2)

ins3 = users.insert()
ins3.execute(dict(id = 4, name = "alfons", fullname = "alfons_xh"), {"id": 5, "name": "alfons", "fullname": "alfons_xh"})

conn.execute("insert into users (name, fullname) values ('alfons', 'alfons_xh'), ('alfons', 'alfons_xh')")

conn.execute("insert into users (name, fullname) values (?, ?)", ('alfons', 'alfons_xh'), ('alfons', 'alfons_xh'))

conn.execute(users.insert(), dict(id = 10, name = "alfons", fullname = "alfons_xh"), {"id": 11, "name": "alfons", "fullname": "alfons_xh"})
```

总结起来大致三种方式：

- 使用 **Table对象** 的 **insert方法**
- 使用引擎的 **connect对象**，其中 **connect对象** 又分为两种方式
  - 直接使用sql语句执行
  - 绑定 **insert方法**。

在进行插入操作时，会使用 **?** 作为占位符，有些命令会使用默认值作为字段的默认值，有些则不会，需要通过观察打印出的执行sql。

### Select操作

**SqlAlchemy** 中的查找操作有两种方式。

```python
conn = engine.connect()

# 第一种方式，使用 Table 对象的 select方法
# SELECT users.id, users.name, users.fullname FROM users WHERE id < 5 order by name
sel1 = users.select(whereclause = "id < 5 order by name")
rows = conn.execute(sel1).fetchall()
print(rows)

# 第二种方式，使用 sqlalchemy.sql 中的 select对象
from sqlalchemy.sql import select

# SELECT users.id, users.name, users.fullname FROM users WHERE id > 5
sel2 = select([users], whereclause = "id > 5")
rows = conn.execute(sel2).fetchall()
print(rows)
```

两种方式殊途同归，**Table对象** 中的select最终调用的仍是 sqlalchemy.sql 中的 select对象。

此外，在查询时可以附加不同的条件进行筛选条件，通过 **where以及其他方法**，用法如下所示，三种方式效果都一样。

```python
from sqlalchemy.sql import select, and_

conn = engine.connect()

# SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address FROM users, addresses WHERE users.id = addresses.user_id AND users.id = ? ORDER BY users.name
# sel = select([users, addresses]).where(and_(users.c.id == addresses.c.user_id, users.c.id == 102)).order_by(users.c.name)
# sel = select([users, addresses]).where((users.c.id == addresses.c.user_id) & (users.c.id == 102)).order_by(users.c.name)
sel = select([users, addresses]).where(users.c.id == addresses.c.user_id).where(users.c.id == 102).order_by(users.c.name)
resultProxy = conn.execute(sel)
for result in resultProxy:
    print(result)
```

如上面的例子所示，**select** 中为需要选择的内容，可以为整个表：**users、addresses**，也可以为某些字段：**users.id、users.name、addresses.user_id**。多个字段使用列表包装。

条件判断语句可以在同一个 **where** 中，使用 **and_、or_、not_** 或者使用 **&、|、！** 等符号，也可以使用多个 **where**，但效果只能是 **and** 了。

值得注意的是，**where** 以及其他表达式中需要使用 **Table对象** 的 **.c属性** 来获取表对应的字段。如 **users** 表中的 **id** 字段，需要使用 **users.c.id** 的方式来获取。查看源码，可以发现，**c** 其实代表的是 **columns方法**，获取的是所有的字段。然后通过取属性的方式可以得到对应的字段。

```python
@_memoized_property
def columns(self):
    """A named-based collection of :class:`.ColumnElement` objects
    maintained by this :class:`.FromClause`.

    The :attr:`.columns`, or :attr:`.c` collection, is the gateway
    to the construction of SQL expressions using table-bound or
    other selectable-bound columns::

        select([mytable]).where(mytable.c.somecolumn == 5)

    """

    if '_columns' not in self.__dict__:
        self._init_collections()
        self._populate_column_collection()
    return self._columns.as_immutable()

c = property(attrgetter('columns'),
             doc="An alias for the :attr:`.columns` attribute.")
```

### 使用Textual SQL

**sqlalchemy.sql** 中 **text** 的用法和直接使用sql语句的方式差不多，只不过 **text** 中的判断参数更加的具体，可以指定参数的类型等。

```python
from sqlalchemy.sql import text
from sqlalchemy.sql import bindparam

# 1、使用text
sel = text("select * from users where users.id < :a").bindparams(bindparam('a', value=1000, type_= Integer))
res = engine.execute(sel).fetchall()
for c in res:
    print(c.id, c.name)
# res = engine.execute(sel, a = 1000).fetchall()

# 2、使用sql语句
sel = "select * from users where users.id < 1000"
res = engine.execute(sel).fetchall()
```

如上所示，在使用text构成sql语句时，使用了 **:a** 对 **users.id** 的上界进行了占位，使用 **bindparam对象** 对a进行绑定，设置a的值和类型。而直接使用sql语句时，则没有这种设置方式。

> 使用 **SqlAlchemy core** 与 **pymysql** 最大的区别在于 **返回的结果**。
> 对于 **SqlAlchemy core** 来说，返回的内容是 **RowProxy** 对象的实例，用户可以通过获取属性的方式得到想要的数据，如上面的 **c.id、c.name**。
> 对于 **pymysql** 来说，返回的是一个 **tuple**，用户只能通过 **res[index]** 的方式，按照顺序获取结果。

## SqlAlchemy ORM

**SQLAlchemy Object Relational Mapper(SQLAlchemy对象关系映射)** 提出了一个方案，使用用户自定义的python类与数据库的表关联，这些类的实例就代表了数据库中的一行(row)。

**SqlAlchemy ORM** 与 **SqlAlchemy core** 最大的区别是， **ORM** 对数据库的表进行了 **高度的抽象**，让使用者感觉不是在操作数据库，而是在操作 **Python对象**。

#todo

### 连接

### 创建表对象

### 查询

## 性能

性能方面，**SqlAlchemy core** 和 **SqlAlchemy ORM** 多少都有将原始数据抽象的过程，将数据从数据库服务器读取出来后，还有一步将数据转换为对象的过程。在写入数据库时，同样也由将操作的对象转换成sql语句的过程，造成了速度上的劣势。而 **pymysql** 更接近直接使用sql命令，速度方面基本没太大的影响。

比较了一下 **pymysql模块**、**SqlAlchemy模块**、**SqlAlchemy Orm**的执行效率。

- 系统：**Ubuntu 18.04 虚拟机**
- CPU：**Intel(R) Core(TM) i5-4590 CPU @ 3.30GHz**
- 测试数据：**2万条**，分十次，每次 **2千**，插入方式为单条插入。

|      模块      | 平均时间 |
| :------------: | :------: |
|  pymysql模块   |  3.55's  |
| SqlAlchemy模块 |  5.22's  |
| SqlAlchemy Orm | 13.01's  |

## 参考

- [Engine Configuration](https://docs.sqlalchemy.org/en/latest/core/engines.html)
- [SQLAlchemy 1.3 Documentation](https://docs.sqlalchemy.org/en/latest/)