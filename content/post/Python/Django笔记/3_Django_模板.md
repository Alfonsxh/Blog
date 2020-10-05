---
title: "Django--模板"
date: 2018-11-27 16:24:15
lastmod: 2018-11-27 21:07:00
draft: false
keywords: ["Python", "Django笔记"]
description: "Django--模板"
tags: ["Python", "Django笔记"]
categories: ["Python", "Django笔记"]
author: "Alfons"
---

**Django** 中的视图要么返回一个包含被请求页面内容的 **HttpResponse** 对象，或者抛出一个异常。

<!--more-->

## render函数

**Django** 通过 **render** 函数返回模板。函数如下：

```python
def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
```

参数说明：

- **request** - 固定参数， **views.py**的函数中的第一个参数。
- **template_name** - **template** 目录下定义的文件，默认实在根目录下的 **template** 目录下查找模板，如果需要在各个应用对应的 **template** 目录下查找，则需要在 **setting.py** 中的 **TEMPLATE** 设置中更改 **APP_DIRS** 为 **True**。
- **context** - 要传入模板文件中 **jinja** 对象所使用的数据，默认是字典格式。
- **content_type** - 返回给浏览器时，看到的 **Content-Type** 的类型。
- **status** - http的响应代码，默认为200。
- **using** - 使用的模板引擎的名称。

可以看到 **render** 是将模板对象做了一些处理以后，最终还是返回了 **HttpResponse** 对象的实例。

## 模板使用

### 创建模板文件

```html
// polls/templates/polls/index.html
{% if lastest_question_list %}
    <ul>
        {% for question in lastest_question_list %}
            <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
        {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

如上，在 **polls/templates/polls/** 文件夹下创建 **index.html** 文件，里面包含了 [jinja](http://jinja.pocoo.org/) 语句。遍历question列表，生成对应问题的链接，点击后跳转。

```html
 <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

这句的作用是，不使用硬编码方式跳转，这里会在 **viewsname** 中查找 **detail** 对应的url路径，后面跟的是捕获的参数。这种方式的好处是，当修改 **urlpatterns** 中的url路径时，不需要对网页文件中引用到的内容进行修改。

同时，这里使用了命名空间的方式，使url定位到 **polls** 应用下的 **detail** url调用。这样做的好处是，防止有多个不同的应用下出现相同的 **viewsname**。

### 使用rendor传入模板数据

然后，在 **views.py** 的函数中，使用 **rendor** 函数，将参数 **lastest_question_list** 传入模板。

```python
def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')
    context = {
        'lastest_question_list': lastest_question_list
    }
    return render(request, 'polls/index.html', context = context)
```

如上，是取了所有的问题，并将问题的列表作为参数传入模板文件中。

![template_index_chrome](/images/Python/Django笔记/3_templates_index_html.png)

## 抛出404错误

假如，在 **views.py** 中的函数运行时发生错误时,或者用户所作的操作无法对应实现时，一般的做法是返回 **404** 错误页面。

返回404页面的方法有两种，一种是自己做异常处理，另一种是使用 **get_object_or_404** 函数，它的作用是在对 **model** 对象进行get操作时，如果发生异常，则返回404错误页面，否则返回所取到的值。

第一种方式：

```python
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

第二种方式：

```python
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

上面的两种方式的效果是一样的，都是在问题对象中，根据问题id取得问题的内容，对模板进行渲染。第二种方式更加简洁一些，推荐使用！