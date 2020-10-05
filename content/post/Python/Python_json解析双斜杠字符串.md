---
title: "Python json解析双斜杠字符串"
date: 2019-05-25 23:58:22
lastmod: 2019-05-25 23:58:22
draft: false
keywords: ["Python"]
description: "Python json解析双斜杠字符串"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

有时候在处理requests返回的结果时，会出现中文unicode编码为双斜杠的情况。

<!--more-->

（现在模拟不出来。。。总之就是上面描述的情况）

在使用json解析时，结果会出现unicode编码，而不是正常的汉字。

在处理时，需要先将字符串进行转换。

```python
import json

content = requests.get(url = target_url).content

res = json.loads(content.encode("unicode_escape"))
```

**unicode_escape** 在unicode中， **\u** 是保留字符，表示后面跟的四个数字，表示一个字符，如果需要将unicode转换为 **六个英文字符**，则可以使用 **unicode_escape** 方式进行转码。

```python
unicode_str = u"\u6211"
str_str = unicode_str.encode("unicode_escape")
print(unicode_str, ' -> ', str_str)

output:
我  ->  b'\\u6211'
```

## 参考

- [unicode_escape](https://www.cnblogs.com/Xjng/p/5093905.html)