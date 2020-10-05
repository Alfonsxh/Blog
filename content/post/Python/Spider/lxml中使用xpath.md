---
title: "Python lxml模块中使用XPath语句"
date: 2018-11-29 19:29:58
lastmod: 2019-01-13 11:29:53
draft: false
keywords: ["Python", "爬虫"]
description: "Python lxml模块中使用XPath语句"
tags: ["Python", "爬虫"]
categories: ["Python", "爬虫"]
author: "Alfons"
---

**lxml模块** 有很多种功能，不单只有 **XPath** 的方式解析 **xml文档**。

<!--more-->

## XPath

**XPath** 为 **XML** 路径语言(XML Path Language)，它是一种用来确定 xml文档中某部分位置的语言。在前端代码中常使用。

### XPath语法

**XPath** 选择节点的方式有点类似于Linux下选择路径的方式。

| 表达式   | 描述                                                       |
| :------- | :--------------------------------------------------------- |
| nodename | 选取此节点的所有子节点。                                   |
| /        | 从根节点选取。                                             |
| //       | 从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。 |
| .        | 选取当前节点。                                             |
| ..       | 选取当前节点的父节点。                                     |
| @        | 选取属性。                                                 |

例如下面的xml文档：

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<bookstore>

<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>

<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>

</bookstore>
```

| 路径表达式      | 结果                                                                                     |
| :-------------- | :--------------------------------------------------------------------------------------- |
| bookstore       | 选取 bookstore 元素的所有子节点。                                                        |
| /bookstore      | 选取根元素 bookstore。假如路径起始于正斜杠( / )，则此路径始终代表到某元素的绝对路径！    |
| bookstore/book  | 选取属于 bookstore 的子元素的所有 book 元素。                                            |
| //book          | 选取所有 book 子元素，而不管它们在文档中的位置。                                         |
| bookstore//book | 选择属于 bookstore 元素的后代的所有 book 元素，而不管它们位于 bookstore 之下的什么位置。 |
| //@lang         | 选取名为 lang 的所有属性。                                                               |

以上路径表达式所选取的都为目标节点下的所有子节点，如果想要得到特定位置的子节点，需要使用 **[]** 进行选取。选取的方式有以下几种。

| 路径表达式                      | 结果                                                                             |
| :------------------------------ | :------------------------------------------------------------------------------- |
| /bookstore/book[1]              | 按照索引号进行选取，第一个索引为1。选取属于 bookstore 子元素的第一个 book 元素。 |
| /bookstore/book[last()]         | 使用函数。选取属于 bookstore 子元素的最后一个 book 元素。                        |
| /bookstore/book[last()-1]       | 选取属于 bookstore 子元素的倒数第二个 book 元素。                                |
| /bookstore/book[position() < 3] | 选取最前面的两个属于 bookstore 元素的子元素的 book 元素。                        |

## XPath在lxml模块中使用

**lxml模块** 是一款高性能的 **Python XML库**，它构建在两个C库之上: **libxml2** 和 **libxslt**。它们为执行解析、序列化和转换等核心任务提供了主要动力。

### lxml解析html

**lxml模块** 解析html文档的方式有三种：**etree.fromstring**、**etree.HTML**、**etree.parse**。前两种的处理的方式是一样的，输入都为字符串类型，输出都为 **根节点的Element对象**。**etree.parse** 方式输入为文件类型的对象，如文件的名称或路径、文件对象、类文件对象、使用URL路径，输出为 **ElementTree对象**。

```python
from lxml import etree

html_name = "test.html"

html_content = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="title story" name="dromouse story">The Dormouse's story</p>
        Dornouse
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            ;and they lived at the bottom of a well.
        </p>
        Good Story!
        <p class="story">...</p>
    </body>
</html>
"""

root_node_fromstring = etree.fromstring(html_content)   # 对象为sting类型，返回Element对象
root_node_HTML = etree.HTML(html_content)       # 对象为string类型，返回Element对象
root_node_parse = etree.parse(html_name)        # 对象为文件类型对象，返回ElementTree对象
```

### Element对象

**lxml模块** 将 **html文档** 中的tag节点都当作了 **Element对象** 处理。**Element对象** 中现在只关注它的几个属性，以及 **xpath方法** 。

| 属性       | 说明                                                                                        |
| :--------- | :------------------------------------------------------------------------------------------ |
| attrib     | Element对象中的属性字典，可以使用get(), set(), keys(), values() 和 items() 函数来存取属性。 |
| base       | Element对象的基础URI，如果使用parse，会显示为文档的路径，如果URI不知道的话，会设置成None。  |
| nsmap      | Namespcae prefix，所有的父节点的命名空间声明字典。                                          |
| prefix     | 命名空间前缀。                                                                              |
| sourceline | Element对象在解析时在原文档中的行位置，不知道时为None。                                     |
| tag        | Element对象的tag名称。                                                                      |
| tail       | 与下一个Element对象之间的字符串，如果下一个Element对象不存在，则为None。                    |
| text       | 与第一个子节点之间的字符串变量。                                                            |

**xpath()方法** 的作用是按照xpath语法找到对应的 **Element对象** 列表，后续的操作都在这个列表中展开。

```python
html_name = "test.html"
root_node_parse = etree.parse(html_name)

a_node_list = root_node_parse.xpath("//p/a")
for a_node in a_node_list:
    print('{a_base} {a_line}: <{a_tag} href="{a_href}" class="{a_class}" id="{a_id}">{a_text}</{a_tag}>'.format(
        a_base = a_node.base,
        a_line = a_node.sourceline,
        a_tag = a_node.tag,
        a_href = a_node.attrib["href"],
        a_class = a_node.attrib["class"],
        a_id = a_node.attrib["id"],
        a_text = a_node.text))

# test.html 10: <a href="http://example.com/elsie" class="sister" id="link1">None</a>
# test.html 11: <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
# test.html 13: <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
```

在使用 **xpath方法** 时，xpath语句的作用对象为整个的文档，并不是以当前的 **Element对象** 为root节点！如果要以当前的 **Element对象** 为root节点，需要使用 **.** 语句。

```python
p_node_list = root_node_parse.xpath("//p")
for p_node in p_node_list:
    a_node_list = p_node.xpath("./a")   # 使用当前的 Element对象 
    for a_node in a_node_list:
        print('{a_base} {a_line}: <{a_tag} href="{a_href}" class="{a_class}" id="{a_id}">{a_text}</{a_tag}>'.format(
            a_base = a_node.base,
            a_line = a_node.sourceline,
            a_tag = a_node.tag,
            a_href = a_node.attrib["href"],
            a_class = a_node.attrib["class"],
            a_id = a_node.attrib["id"],
            a_text = a_node.text))

# test.html 10: <a href="http://example.com/elsie" class="sister" id="link1">None</a>
# test.html 11: <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
# test.html 13: <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
```

其他的 **XPath语法** 使用方式一样。

### xpath选择兄弟节点

```html
<div id="info">
        <span class="pl">制片国家/地区:</span> 美国<br/>
        <span class="pl">语言:</span> 英语<br/>
        <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2014-01-18(圣丹斯电影节)">2014-01-18(圣丹斯电影节)</span> / <span property="v:initialReleaseDate" content="2015-09-18(美国)">2015-09-18(美国)</span><br/>
        <span class="pl">片长:</span> <span property="v:runti/following::*me" content="88">88分钟</span><br/>
        <span class="pl">又名:</span> 虱子<br/>
        <span class="pl">IMDb链接:</span> <a href="http://www.imdb.com/title/tt2490326" target="_blank" rel="nofollow">tt2490326</a><br>
</div>
```

例如上面的例子，想要获取制片国家和语言的信息，但这部分信息不在 **span** 标签中，而是处于 **span和br** 之间。

首先，我们找到 **制片国家/地区** 这个节点

```python
country = root_node.xpath("//div[contains(@id, 'info')]/span[contains(@class, 'pl') and contains(text(), '制片国家/地区:')]")
```

国家对应的属性为 **text()**，并且是在tag后面的属性。xpath中，对于相邻属性，有 **following**、**following-sibling**、**preceding**、**preceding-sibling** 四种方式获取。对于上面的例子来说，可以使用 **following**、**following-sibling**。

```python
country_1 = root_node.xpath("//div[contains(@id, 'info')]/span[contains(@class, 'pl') and contains(text(), '制片国家/地区:')]/following::text()")
print(country_1)

# output:

[' 美国', '\n        ', '语言:', ' 英语', '\n        ', '上映日期:', ' ', '2014-01-18(圣丹斯电影节)', ' / ', '2015-09-18(美国)', '\n        ', '片长:', ' ', '88分钟', '\n        ', '又名:', ' 虱子', '\n        ', 'IMDb链接:', ' ', 'tt2490326', '\n', '\n']

country_2 = root_node.xpath("//div[contains(@id, 'info')]/span[contains(@class, 'pl') and contains(text(), '制片国家/地区:')]/following-sibling::text()")
print(country_2)

# output:

[' 美国', '\n        ', ' 英语', '\n        ', ' ', ' / ', '\n        ', ' ', '\n        ', ' 虱子', '\n        ', ' ', '\n']
```

**following** 方式获取的是后继所有 **tag** 中的 **text()**。而 **following-sibling** 获取的是 **同等级的兄弟节点的内容**。

**preceding**、**preceding-sibling** 为前驱节点，用法和上面的一样。

另外，还有几个：

- **parent::** - 取当前节点的 **父节点**。
- **child::** - 取当前节点的 **子节点**。
- **ancestor::** - 取当前节点的 **父节点、祖父节点等**。
- **descendant::** - 取当前节点的 **子节点、子孙节点**。

## 参考

[lxml etree API](https://lxml.de/api/index.html)
[xpath路径表达式笔记](http://www.ruanyifeng.com/blog/2009/07/xpath_path_expressions.html)
[W3school XPath 教程](http://www.w3school.com.cn/xpath/index.asp)