---
title: "Python pymysql连接错误"
date: 2019-01-05 15:07:21
lastmod: 2019-01-05 15:07:21
draft: false
keywords: ["Python"]
description: "Python pymysql连接错误"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

在使用pymysql模块与数据库进行交互时，如果长时间进行连接，可能会出现连接中断，导致无法操作数据库的问题。

<!--more-->

一般数据库的连接方式如下:

```python
conn = pymysql.connect(
    host='10.10.0.109',
    port=3306,
    user='mha',
    password='123456',
    database='sbtest',
    charset='utf8'
)

cursor = conn.cursor()
cursor.excute(sql)
result = cursor.fetchall()
cursor.close()
```

这种方式下，如果数据库连接异常关闭了，就会抛出异常:

```python
Traceback (most recent call last):
  File "/src/DataManager/MysqlMiddleware/MysqlParser.py", line 77, in FetchVpnField
    mysql_cur.execute(sql_fetch_one)
  File "/Python3Venv/lib/python3.6/site-packages/pymysql/cursors.py", line 170, in execute
    result = self._query(query)
  File "/Python3Venv/lib/python3.6/site-packages/pymysql/cursors.py", line 328, in _query
    conn.query(q)
  File "/Python3Venv/lib/python3.6/site-packages/pymysql/connections.py", line 515, in query
    self._execute_command(COMMAND.COM_QUERY, sql)
  File "/Python3Venv/lib/python3.6/site-packages/pymysql/connections.py", line 745, in _execute_command
    raise err.InterfaceError("(0, '')")
pymysql.err.InterfaceError: (0, '')
```

处理方式为，每次在使用时，先 **ping** 一下:

```python
conn = pymysql.connect(
    host='10.10.0.109',
    port=3306,
    user='mha',
    password='123456',
    database='sbtest',
    charset='utf8'
)

conn.ping()
cursor = conn.cursor()
cursor.excute(sql)
result = cursor.fetchall()
cursor.close()
```

在 **ping** 的时候，如果发现连接异常，会尝试重新建立连接:

```python
def ping(self, reconnect=True):
    """
    Check if the server is alive.

    :param reconnect: If the connection is closed, reconnect.
    :raise Error: If the connection is closed and reconnect=False.
    """
    if self._sock is None:
        if reconnect:
            self.connect()
            reconnect = False
        else:
            raise err.Error("Already closed")
    try:
        self._execute_command(COMMAND.COM_PING, "")
        self._read_ok_packet()
    except Exception:
        if reconnect:
            self.connect()
            self.ping(False)
        else:
            raise
```