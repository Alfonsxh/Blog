---
title: "Python json解析错误处理"
date: 2019-01-05 15:07:21
lastmod: 2019-01-05 15:07:21
draft: false
keywords: ["Python"]
description: "Python json解析错误处理"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

在处理Json字符串时，当在Json原始数据中出现某些 **空格** 时，可能会出现 **json.decoder.JSONDecodeError** 的错误。

<!--more-->

```python
import json

error_json = '{"name": "Tom\0"}'
json_result = json.loads(error_json)

# output
Traceback (most recent call last):
  File "/home/xxxxxx/PycharmProjects/Python/Json/JsonParserError.py", line 9, in <module>
    json_result = json.loads(error_json)
  File "/usr/lib/python3.6/json/__init__.py", line 354, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3.6/json/decoder.py", line 339, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python3.6/json/decoder.py", line 355, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Invalid control character at: line 1 column 14 (char 13)

```

这是由于默认情况下，**json** 模块使用的是严格匹配，即参数 **strict默认为True**。

> If ``strict`` is false (true is the default), then control
> characters will be allowed inside strings.  Control characters in
> this context are those with character codes in the 0-31 range,
> including ``'\\t'`` (tab), ``'\\n'``, ``'\\r'`` and ``'\\0'``.

在上面的代码中，出现的json中包含了空格，导致了解析出错，只需要将 **strict=Fasle** 加上就行。

```python
import json

error_json = '{"name": "Tom\0"}'
# json_result = json.loads(error_json)
json_result = json.loads(error_json, strict = False)

# output
Process finished with exit code 0
```