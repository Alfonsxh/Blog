---
title: "Django通用视图"
date: 2018-11-27 16:24:15
lastmod: 2018-11-27 16:24:15
draft: false
keywords: ["Python", "Django笔记"]
description: "Django通用视图"
tags: ["Python", "Django笔记"]
categories: ["Python", "Django笔记"]
author: "Alfons"
---

使用通用视图的好处在于，能够最大程度的重复利用代码，减少代码量，并且方便扩展。

使用 **函数** 的方式实现：

<!--more-->

```python
def index(request):
    all_question = Question.objects.order_by('pub_date')
    context = {
        'all_question': all_question
    }
    return render(request, 'polls/index.html', context = context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'polls/requests.html', {'question': question})  # 转到对应的界面
```

使用 **通用视图** 的方式实现：

```python
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'all_question'
    model = Question        # 模型名称
    # queryset = Question.objects.all()   # 数据set
    ordering = '-pub_date'      # 排序方式


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    context_object_name = 'question'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/requests.html'
    context_object_name = 'question'
```

从上面的代码可以看到，使用 **通用视图**的方式实现时，只需要指定极少的参数即可实现相同的功能。不用自己完成数据的读取，不用自己设置模型的上下文，不用自己渲染模板。

## 通用视图

**Django**类视图的源码位于 **django.views.generic** 包中，其目录结构如下：

```shell
generic/
|—— __init__.py
|—— base.py
|—— dates.py
|—— detail.py
|—— edit.py
|—— list.py
```

各模块的功能如下：

- **base.py** - 主要存放所有类视图的基类 View ，以及一些和数据库操作无关的类视图如 TemplateView、RedirectView。
- **dates.py** - 主要存放用于按时间归档的类视图，如 ArchiveIndexView，一些视图在博客系统中非常有用，例如获取某个日期下的全部文章列表。
- **detail.py** - 主要存放用于从数据库获取单条记录的类视图，例如从数据库中获取某一篇博客文章。
- **edit.py** - 主要包含了表单处理，创建、更新和删除数据库中的单条记录的类视图。
- **list.py** - 主要包含了从数据库中获取多条记录的类视图，例如从数据库中获取全部博客文章列表。

让人惊喜的是，虽然 **Django**中类视图种类繁多，而且继承关系复杂，但是耐下性子来分析，会发现他们条理很清晰，各个类只负责自己所关心的事情，并且命名也严格遵循一定的规则。

例如 **ListView** 视图的继承关系如下：

```shell
ContextMixin --> MultipleObjectMixin +
|                                    |
|                                    | --> BaseListView ----  + 
|                                    |                        |
View ------------------------------- +                        | --> ListView
                                                              |
TemplateResponseMixin --> MultipleObjectTemplateResponseMixin +
```

**DetailView** 视图的继承关系乳腺癌：

```shell
ContextMixin --> SingleObjectMixin - +
|                                    |
|                                    | --> BaseDetailView --  + 
|                                    |                        |
View ------------------------------- +                        | --> DetailView
                                                              |
TemplateResponseMixin --> SingleObjectTemplateResponseMixin - +
```

下面单从 **ListView** 视图从源码角度分析具体的实现。

## ListView

**ListView**继承自 **MultipleObjectTemplateResponseMixin**、**BaseListView**两个父类，具体功能都由对应的父类完成。

```python
class ListView(MultipleObjectTemplateResponseMixin, BaseListView):
    """
    Render some list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """
```

### MultipleObjectTemplateResponseMixin

**MultipleObjectTemplateResponseMixin**类定义了一个变量参数 **template_name_suffix**，表示的是模板名称的后缀。

重写了父类 **TemplateResponseMixin** 的 **get_template_names**获取模板名称函数。

- 如果父类 **TemplateResponseMixin**中的变量 **template_name** 未赋值，则会根据参数在模板列表中添加 **app名称+模块名+模板名称后缀.html** 为模板名的模板文件名。
- 如果父类 **TemplateResponseMixin**中的变量 **template_name** 有赋值，则会追加上述命名方式的模板文件。

```python
class MultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    """Mixin for responding with a template and list of objects."""
    template_name_suffix = '_list'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        try:
            names = super().get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If the list is a queryset, we'll invent a template name based on the
        # app and model name. This name gets put at the end of the template
        # name list so that user-supplied names override the automatically-
        # generated ones.
        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names.append("%s/%s%s.html" % (opts.app_label, opts.model_name, self.template_name_suffix))
        elif not names:
            raise ImproperlyConfigured(
                "%(cls)s requires either a 'template_name' attribute "
                "or a get_queryset() method that returns a QuerySet." % {
                    'cls': self.__class__.__name__,
                }
            )
        return names
```

#### TemplateResponseMixin

**TemplateResponseMixin**类的作用是混合不同预设参数，渲染模板后返回。

类中的变量有：

- **template_name** - 用户指定的模板名称，默认为None。
- **template_engine** - 用户指定的模板引擎，默认为None。
- **response_class** - 定义返回函数，默认为 **TemplateResponse**。
- **content_type** - 定义返回类型，默认为None。

类中的功能函数有：

- **render_to_response** - 根据上下文，指定的模板引擎等，返回渲染后的模板。
- **get_template_names** - 返回模板名称列表，用户未指定 **template_name** 时，返回异常，由子类捕获后，添加默认的模板名称列表。

```python
class TemplateResponseMixin:
    """A mixin that can be used to render a template."""
    template_name = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]
```

### BaseListView

**BaseListView**类继承自 **MultipleObjectMixin**, **View**类。

**BaseListView**类只实现了 **get**请求，会查询model中是否含有数据，如果 **allow_empty**参数设置为False，并且数据为空，则会返回404页面。最后的返回由绑定了的 **TemplateResponseMixin**类中的 **render_to_response**函数处理。

```python
class BaseListView(MultipleObjectMixin, View):
    """A base view for displaying a list of objects."""
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)
```

#### MultipleObjectMixin

**MultipleObjectMixin**类的作用是混合了用户自定义的多个对象。

类中定义的变量参数有：

- **allow_empty** - 是否允许数据为空，默认为True。
- **queryset** - 用于存储查询对象，类型可以为任意 **iterable**对象，默认为None。
- **model** - 指定模型的名称，如果 **queryset**参数用户未指定，则会从指定的模型中读取数据，默认为None。
- **paginate_by** - 分页，指定每页的大小，默认为None。
- **paginate_orphans** - 返回分页时扩展最后一页的最大孤儿项目数量，默认为0。
- **context_object_name** - 取出的模型数据在上下文中的名称，该名称用于渲染时传入模板，默认为None时，会根据一定的规则生成。
- **paginator_class** - 分页处理类，默认为 **Paginator**。
- **page_kwarg** - 分页名称参数，默认为 **'page'**。
- **ordering** - 排序标准，定义了model变量后，可以根据model中的字段名来排序。

实现的功能函数有：

- **get_queryset** - 返回该视图的数据队列，如果设置了排序选项，会返回排序后的数据。
- **get_ordering** - 返回 **ordering**。
- **paginate_queryset** - 返回分页化后的数据，输入参数： **queryset**输入数据， **page_size**每页数据量。
- **get_paginate_by** - 返回 **paginate_by**。
- **get_paginator** - 返回分页处理类的实例。
- **get_paginate_orphans** - 返回 **paginate_orphans**。
- **get_allow_empty** - 返回 **allow_empty**。
- **get_context_object_name** - 返回model在上下文中的名称。
- **get_context_data** - 返回上下文。

```python
class MultipleObjectMixin(ContextMixin):
    """A mixin for views manipulating multiple objects."""
    allow_empty = True
    queryset = None
    model = None
    paginate_by = None
    paginate_orphans = 0
    context_object_name = None
    paginator_class = Paginator
    page_kwarg = 'page'
    ordering = None

    def get_queryset(self):
        """
        Return the list of items for this view.

        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_ordering(self):
        """Return the field or fields to use for ordering the queryset."""
        return self.ordering

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_("Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        """Return an instance of the paginator for this view."""
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_paginate_orphans(self):
        """
        Return the maximum number of orphans extend the last page by when
        paginating.
        """
        return self.paginate_orphans

    def get_allow_empty(self):
        """
        Return ``True`` if the view should display empty lists and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """Get the name of the item to be used in the context."""
        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            return '%s_list' % object_list.model._meta.model_name
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super().get_context_data(**context)
```

##### ContextMixin

**ContextMixin**类包括了一个变量 **extra_context**表示额外的上下文变量。一个功能函数 **get_context_data**，在上下文中添加了 **'view'**代表自身，如果有额外的上下文，也添加。

```python
class ContextMixin:
    """
    A default context mixin that passes the keyword arguments received by
    get_context_data() as the template context.
    """
    extra_context = None

    def get_context_data(self, **kwargs):
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs
```

#### View

**View**类是所有 **视图类**的基类，它只实现了http请求方法的调度和简单的参数检查。

类中参数 **http_method_names**记录了所有允许的http请求类型。

实现的功能函数有：

- **as_view** - 在函数内部定义了 **view**，当执行 **as_view**时，会返回该函数，作为可执行对象。
- **dispatch** - http请求分发函数，会在子类中查找对应的请求属性，例如 **BaseListView**中只实现了 **get**请求方法，则 **BaseListView**只响应get请求。
- **http_method_not_allowed** - 如果请求方法不在规定的方法内，则返回 **HttpResponseNotAllowed**对象实例。
- **options** - 返回视图允许的请求类型。
- **_allowed_methods** - 返回视图允许的请求类型。

```python
class View:
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """Main entry point for a request-response process."""
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning(
            'Method Not Allowed (%s): %s', request.method, request.path,
            extra={'status_code': 405, 'request': request}
        )
        return HttpResponseNotAllowed(self._allowed_methods())

    def options(self, request, *args, **kwargs):
        """Handle responding to requests for the OPTIONS HTTP verb."""
        response = HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]
```

## 使用通用视图

在使用通用视图替换原来的函数实现后，要将 **urls.py**中的路由映射修改：

```python
urlpatterns = [
    # ex: /polls/
    # path('', views.index, name = 'index'),
    path('', views.IndexView.as_view(), name = 'index'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name = 'detail'),
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name = 'results'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name = 'vote'),
]
```

使用 **as_view()**方法替换原来的视图函数，如上面分析， **as_view()**函数调用后会返回一个 **view**方法供调用。

## 总结

**Django**中的通用视图还有很多，如

```python
__all__ = [
    'View', 'TemplateView', 'RedirectView', 'ArchiveIndexView',
    'YearArchiveView', 'MonthArchiveView', 'WeekArchiveView', 'DayArchiveView',
    'TodayArchiveView', 'DateDetailView', 'DetailView', 'FormView',
    'CreateView', 'UpdateView', 'DeleteView', 'ListView', 'GenericViewError',
]
```

熟悉使用通用视图会加快开发速度！

## 参考

[Django类视图源码分析](https://www.zmrenwu.com/post/51/)
[django源码解析通用视图篇之ListView](https://blog.csdn.net/q1403539144/article/details/79844882)