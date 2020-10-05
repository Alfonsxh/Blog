---
title: "Beautiful Soup使用手册"
date: 2018-11-29 19:29:58
lastmod: 2018-11-29 19:29:58
draft: false
keywords: ["Python", "爬虫"]
description: "Beautiful Soup使用手册"
tags: ["Python", "爬虫"]
categories: ["Python", "爬虫"]
author: "Alfons"
---

**Beautiful Soup**作用是处理从网页爬下来的数据，如果说 **scrapy**是辆车，那么 **Beautiful Soup**就是车轮。

<!--more-->

## 安装

```shell
pip install beautifulsoup4
```

## 使用

### 创建beautifulsoup对象

**Beautiful Soup**对象的创建方式有几种。

使用 **字符串**初始化：

```python
from bs4 import BeautifulSoup

html_content = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="title story" name="dromouse story">The Dormouse's story</p>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            ;and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
    </body>
</html>
"""

soup = BeautifulSoup(html_content)
```

使用 **文件**初始化：

```python
soup = BeautifulSoup(open('index.html'))
```

### Beautiful Soup 四大对象

**Beautiful Soup**将html文档转换成一个复杂的树形结构，每个节点都是python对象，所有对象可以归纳为四种: **Tag**、**NavigableString**、**BeautifulSoup**、**Comment**。

#### Tag

**Tag**对象与 **XML**或 **HTML**原生文档中的tag相同。tag中有两个重要的属性：**name**、**attributes**。

```python
p_tag = soup.p
print("type(p_tag) -> ", type(p_tag))           # tag的类型为 <class 'bs4.element.Tag'>
print("p_tag.name -> ", p_tag.name)             # tag的名称为 p
print("p_tag.attrs -> ", p_tag.attrs)           # 使用.attrs的方式获取tag的所有属性 {'class': ['title', 'story'], 'name': 'dromouse story'}
print("p_tag['class'] -> ", p_tag["class"])     # 也可以使用这种方式获取特定属性的内容 ['title', 'story']
print("p_tag['name'] -> ", p_tag["name"])       # dromouse story
```

> 多值属性: html中有些属性可以包含多个属性值，**Beautiful Soup**会对比任何版本的 html 定义，如果该属性属于某个版本，则返回类型为list，否则，返回的是字符串。例如上面的 **class** 和 **name** 属性。

此外， **Beautiful Soup**还支持添加和删除某个属性。

```python
p_tag["newer"] = "new story name not know"
print("p_tag -> ", p_tag)       # <p class="title story" name="dromouse story" newer="new story name not know">The Dormouse's story</p>

del p_tag["newer"]
print("p_tag -> ", p_tag)       # <p class="title story" name="dromouse story">The Dormouse's story</p>
```

#### NavigableString

**NavigableString**对象表示的是tag中的字符串。

```python
print("p_tag.string -> ", p_tag.string)                     # The Dormouse's story
print("type(p_tag.string) -> ", type(p_tag.string))         # <class 'bs4.element.NavigableString'>

p_tag.string.replace_with("No longer bold")     # 替换tag中包含的字符串
print("p_tag -> ", p_tag)            # <p class="title story" name="dromouse story">No longer bold</p>
```

> 如果想在Beautiful Soup之外使用 NavigableString 对象,需要调用 unicode() 方法,将该对象转换成普通的Unicode字符串,否则就算Beautiful Soup已方法已经执行结束,该对象的输出也会带有对象的引用地址.这样会浪费内存.

#### BeautifulSoup

**BeautifulSoup**对象表示的是一个文档的全部内容，它没有 **name** 和 **attribute**属性，使用 **.name**查看时，会返回 一个值为 **document**的特殊属性。

```python
print("type(soup) -> ", type(soup))     # <class 'bs4.BeautifulSoup'>
print("soup.name - > ", soup.name)      # [document]
```

#### Comment

**Comment**表示的是注释部分。它是一个特殊类型的 **NavigableString**对象，也是通过 **.string**方式获取。有时会通过判断是否是 **Comment**对象的方式来判断是否是tag内字符串，而不是注释。

```python
from bs4.element import Comment

markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup, 'lxml')
comment = soup.b.string
print(type(comment))        # <class 'bs4.element.Comment'>
if type(comment) == Comment:
    print(comment)          # Hey, buddy. Want to buy a used parser?
```

### 遍历文档树

#### 子节点

一个 **Tag**可以包含多个字符串或其他的 **Tag**，**Beautiful Soup**提供了许多操作和遍历子节点的属性。

可以通过属性的方式获取 **Tag**下的子节点，子节点为 html文档中第一次出现的节点。

```python
print("soup.head -> ", soup.head)       # <head><title>The Dormouse's story</title></head>
print("soup.title -> ", soup.title)     # <title>The Dormouse's story</title>
print("soup.head.title -> ", soup.head.title)   # <title>The Dormouse's story</title>
```

##### .contents 和 .children

通过tag的 **.contents** 属性可以获取tag的子节点列表。通过 **.children**属性获取的是tag子节点的 **列表的迭代器**。

此外，字符串没有 **.contents** 属性，所以通过 **.contents** 无法获得tag的字符串内容。但通过 **.children**可以。

```python
body_tag = soup.body
contents = body_tag.contents
print("type(contents) -> ", type(contents))     # <class 'list'>

children = body_tag.children
print("type(children) -> ", type(children))     # <class 'list_iterator'>
```

##### .descendants

**.contents** 和 **.children**获取的都是目标的 **直接节点**，而 **.descendants**获取的是tag的子孙节点。**.descendants**返回的是一个 **生成器**。

```python
descendants = body_tag.descendants
print("type(descendants) -> ", type(descendants))       #  <class 'generator'>
```

##### .strings 和 .stripped_strings

通过 **.string**属性获取的tag内必须只有一个 **NavigableString**类型的子节点，如果含有多个，那么 **.string**将返回 **None**。

```python
print("soup.html.string -> ", soup.html.string)     # None
```

如果包含多个，可以通过 **.strings** 属性来获取，或者通过 **.stripped_strings**属性，去除空格或空行。

```python
html_strings = soup.html.strings
print("type(html_strings) -> ", type(html_strings))         # <class 'generator'>

html_stripped_strings = soup.html.stripped_strings
print("type(html_stripped_strings) -> ", type(html_stripped_strings))       # <class 'generator'>
```

#### 父节点

每个tag都含有自己的父节点，文档顶层的节点的父节点是 **BeautifulSoup** 对象， **BeautifulSoup**对象的父节点为None。通过 **.parent**属性可以获取节点的父节点，**.parents**属性获取节点的所有父辈节点。

```python
p_tag = soup.p
p_parent = p_tag.parent
print("type(p_parent) -> ", type(p_parent))     # <class 'bs4.element.Tag'>
print("type(soup.parent) -> ", type(soup.parent))       # <class 'NoneType'>

for parent in p_tag.parents:
    if parent is None:
        print("None")
    else:
        print(parent.name)

# body
# html
# [document]
```

#### 兄弟节点

通过 **.previous_sibling** 获取目标节点的上一个兄弟节点，通过 **.next_sibling** 获取目标节点的下一个兄弟节点。

```python
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>", "lxml")
print("sibling_soup.b.previous_sibling -> ", sibling_soup.b.previous_sibling)   # None
print("sibling_soup.b.next_sibling -> ", sibling_soup.b.next_sibling)           # <c>text2</c>
print("sibling_soup.c.previous_sibling -> ", sibling_soup.c.previous_sibling)   # <b>text1</b>
print("sibling_soup.c.next_sibling -> ", sibling_soup.c.next_sibling)           # None
```

但是，很多情况下，兄弟节点会出现意想不到的结果，原因在于tag之前还存在着类似于 **换行符**这样的标志。

```python
print("p_tag.next_sibling -> ", p_tag.next_sibling)     # 返回 \n 换行符
print("p_tag.next_sibling.next_sibling -> ", p_tag.next_sibling.next_sibling)
print("p_tag.next_sibling.next_sibling.next_sibling -> ", p_tag.next_sibling.next_sibling.next_sibling)     # 返回 \n 换行符
print("p_tag.next_sibling.next_sibling.next_sibling.next_sibling -> ", p_tag.next_sibling.next_sibling.next_sibling.next_sibling)   #  <p class="story">...</p>
```

和 **.parents** 类似，通过 **.next_siblings** 和 **.previous_siblings**可以获取所有的兄弟节点。

```python
print("type(p_tag.previous_siblings) -> ", type(p_tag.previous_siblings))       # <class 'generator'>
print("type(p_tag.next_siblings) -> ", type(p_tag.next_siblings))       # <class 'generator'>
```

#### 兄弟元素

**兄弟元素** 和 **兄弟节点** 略有不同。

**兄弟节点** 指的是同一级的节点，**兄弟元素**依靠的是解释器解析的顺序。例如：

```html
<p>
...
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
    and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
...
</p>
```

上面html片段中，两个**a**标签和 **and**字符串属于 **兄弟节点**，而第一个 **a**标签的下一个元素为 **Lacie**。

**兄弟元素** 通过 **.next_element**、**.previous_element**、**.next_elements**、**.previous_elements**获取，用法同之前的父节点和兄弟节点类似。

### 搜索文档树

**Beautiful Soup**有很多的搜索方法:

| 方法名                       | 作用                                  |
| :--------------------------- | :------------------------------------ |
| **find_all()**               | 查找所有符合条件的tag列表             |
| **find()**                   | 查找所有符合条件的tag对象             |
| **find_parents()**           | 查找所有符合条件的tag父节点列表       |
| **find_parent()**            | 查找所有符合条件的tag父节点           |
| **find_next_siblings()**     | 向后查找所有符合条件的tag兄弟节点列表 |
| **find_next_sibling()**      | 向后查找所有符合条件的tag兄弟节点     |
| **find_previous_siblings()** | 向前查找所有符合条件的tag兄弟节点列表 |
| **find_previous_sibling()**  | 向前查找所有符合条件的tag兄弟节点     |
| **find_all_next()**          | 向后查找所有符合条件的元素列表        |
| **find_next()**              | 向后查找所有符合条件的元素            |
| **find_all_previous()**      | 向前查找所有符合条件的元素列表        |
| **find_previous()**          | 向前查找所有符合条件的元素            |

**find()** 和 **find_all()** 是其中比较常用了两个，其他的方法使用类似。

#### find_all()

**find_all** 的作用是搜索当前tag的所有子tag节点，并判断是否符合某些特征，并返回它们的列表。这些特征包括：tag的name、节点的属性、节点的字符串或者这些特征的混合。

```python
def find_all(self, name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)
```

其中 **name**、**attrs**、**text** 参数可以接收 **字符串**、**正则表达式**、**列表**、**True**、**方法**类型的变量。

```python
import re

print('soup.find_all("title") -> ', soup.find_all("title"))     # 使用字符串搜索
print('soup.find_all(re.compile("tit")) -> ', soup.find_all(re.compile("tit")))     # 使用正则表达式搜索，返回tag名称中包含 'tit' 的tag
print('soup.find_all(["a", "title"]) -> ', soup.find_all(["a", "title"]))       # 使用列表搜索，返回所有的a、title标签

for tag in soup.find_all(True):     # 打印所有的tag
    print(tag.name)


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


print('soup.find_all(has_class_but_no_id) -> ', soup.find_all(has_class_but_no_id))     # 使用方法搜索，打印出有class属性没有id属性的所有tag
```

以上是通过 **name**参数进行过滤，有时也需要通过keyword参数来进行过滤。

```python
print('soup.find_all(id="link2") -> ', soup.find_all(id="link2"))  # 返回属性中id="link2"的tag对象  [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
```

有些属性命中含有特殊符号的不能通过这种方式过滤，使用attrs能够实现。

```python
data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', "lxml")
# data_soup.find_all(data-foo="value")      # 语句异常
print('data_soup.find_all(attrs={"data-foo": "value"}) -> ', data_soup.find_all(attrs={"data-foo": "value"}))   # 使用attrs的字典属性
```

另一个是 **class**属性，因为 **class** 是python中的关键字，在过滤时使用 **class_** 代替。

```python
print('soup.find_all("a", class_="body")) -> ', soup.find_all("a", class_="sister"))

# [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
#  <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>,
#  <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
```

**limit**参数的作用是限制查找出的tag数目。

```python
print('soup.find_all("a", class_="body", limit=1)) -> ', soup.find_all("a", class_="sister", limit=1))

# [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
```

#### find()

**find()** 方法的使用和 **find_all()** 类似，查找出来的结果为单一的tag对象。如果没有找到， **find**将会返回 **None**， **find_all**将会返回 **空列表**。

其他的搜索方法，用法大多大同小异。

## 参考

[Beautiful Soup 4.2.0 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/index.html)