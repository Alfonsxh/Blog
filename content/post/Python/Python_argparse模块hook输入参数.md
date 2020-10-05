---
title: "Python argparse 模块 hook 输入参数的几种方式"
date: 2020-08-25 16:35:40
lastmod: 2020-08-25 16:35:40
draft: false
keywords: ["Python"]
description: "Python argparse 模块 hook 输入参数的几种方式"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

> 需求描述：
>
> 用户输入size参数值，如果未给定单位，需要指定默认的size单位。

<!--more-->

最初代码如下:

```python
import argparse


def get_parser():
    parser = argparse.ArgumentParser(description="Test size hook")
    parser.add_argument("-s", "--size",
                        required=True,
                        action="store",
                        dest="size",
                        default="",
                        help="Specify one size, eg: 1T、200GB. "
                             "Default unit is GB. ")
    return parser


def run():
    parser = get_parser()

    args = parser.parse_args()
    print(f"{args.size=}")


if __name__ == '__main__':
    run()
```

运行此程序：

```shell
$ python arg_hook.py --help
usage: arg_hook.py [-h] -s SIZE

Test size hook

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Specify one size, eg: 1T、200GB. Default unit is GB.

$ python arg_hook.py -s 200
args.size='200'

$ python arg_hook.py -s 200MB
args.size='200MB'
```

下面使用三种方式来实现对size进行默认单位设置：

- 在获取完size之后修改
- 使用 **自定义的store action对象**
- 使用 **自定义的Type方法**

## 在获取完size之后修改

这种方式不在argparse中改变参数值，而是参数经过argparse解析之后，再判断并添加对应的参数。

```python
# 1. 使用参数处理之外的方法实现
def convert_size(values, default_unit="GB"):
    if isinstance(values, (str, bytes)):
        values = str(values)

        # 输入合法性判断
        if set(values.upper()) - set("0123456789.BKMGTP"):
            raise ValueError("Input size {v} not available.".format(v=values))

        # 输入单位判断，需要判断小数点位数，如果大于一个，不是数字类型
        for unit_char in list("BKMGTP."):
            if values.upper().count(unit_char) > 1:
                raise ValueError("Input size {v} error.".format(v=values))

        # 如果只输入数字，则添加上默认的单位后缀
        if not set(values.strip()) - set("0123456789."):
            values = str(float(values)) + default_unit

        return values

...

def run():
    parser = get_parser()

    args = parser.parse_args()
    args.size = convert_size(args.size)
    print(f"{args.size=}")


if __name__ == '__main__':
    run()
```

执行结果:

```shell
$ python arg_hook.py -s 200
args.size='200.0GB'
```

## 使用自定义的store action对象

在argparse模块中，提供了各种 **action** 动作，作用是将输入的参数，按照不同的动作做对应的转换。

- 模块中提供了多个 **action** 对象，在初始化 **ArgumentParser** 对象时，会注册对应的动作对象

    ```python
    # ArgumentParser对象继承_ActionsContainer
    class _ActionsContainer(object):

        def __init__(self,
                    description,
                    prefix_chars,
                    argument_default,
                    conflict_handler):
            super(_ActionsContainer, self).__init__()

            ...

            # set up registries
            self._registries = {}

            # register actions
            self.register('action', None, _StoreAction)
            self.register('action', 'store', _StoreAction)
            self.register('action', 'store_const', _StoreConstAction)
            self.register('action', 'store_true', _StoreTrueAction)
            self.register('action', 'store_false', _StoreFalseAction)
            self.register('action', 'append', _AppendAction)
            self.register('action', 'append_const', _AppendConstAction)
            self.register('action', 'count', _CountAction)
            self.register('action', 'help', _HelpAction)
            self.register('action', 'version', _VersionAction)
            self.register('action', 'parsers', _SubParsersAction)
            self.register('action', 'extend', _ExtendAction)

            ...
    ```

- 在 **add_argument** 方法中，指定 **action参数**，输入的参数将使用指定的动作进行转换。例如，指定 `action="count"`，输入参数后，将按照 **_CountAction** 实现的 **__call__** 方法进行转化。

    ```python
    class ArgumentParser(_AttributeHolder, _ActionsContainer):
        ...
        def _parse_known_args(self, arg_strings, namespace):
            ...

            def take_action(action, argument_strings, option_string=None):
                ...

                # take the action if we didn't receive a SUPPRESS value
                # (e.g. from a default)
                if argument_values is not SUPPRESS:
                    action(self, namespace, argument_values, option_string)
    ```

- 可以使用自定义的 **action对象** 替换模块中的默认动作对象。在 **add_argument** 方法中，指定 **action参数** 为自定义的 **action对象** 即可。模块在处理时，如果发现传入的 **action参数** 未被注册，并且是能够被调用的，则将初始化自定义的action对象。

    ```python
    def _pop_action_class(self, kwargs, default=None):
        action = kwargs.pop('action', default)
        return self._registry_get('action', action, action)

    def add_argument(self, *args, **kwargs):
    ...

    # create the action object, and add it to the parser
    action_class = self._pop_action_class(kwargs)
    if not callable(action_class):
        raise ValueError('unknown action "%s"' % (action_class,))
    action = action_class(**kwargs)
    ```

自定义 **action对象** 只需要按照要求实现 **__init__** 和 **__call__** 方法即可。在本例子中，继承模块中的 **_StoreAction类**，只需修改对应的 **__call__** 方法即可。

```python
# 2. 使用自定义action对象实现
class _StoreSizeAction(argparse._StoreAction):
    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, (str, bytes)):
            values = str(values)

            # 输入合法性判断
            if set(values.upper()) - set("0123456789.BKMGTP"):
                parser.error("Input size {v} not available.".format(v=values))

            # 输入单位判断，小数点位数也需要判断，大于一个点，将不是数字类型
            for unit_char in list("BKMGTP."):
                if values.upper().count(unit_char) > 1:
                    parser.error("Input size {v} error.".format(v=values))

            # 如果只输入数字，则添加上默认的单位后缀
            if not set(values.strip()) - set("0123456789."):
                values = str(float(values)) + "GB"

        setattr(namespace, self.dest, values)


def get_parser():
    parser = argparse.ArgumentParser(description="Test size hook")
    parser.add_argument("-s", "--size",
                        required=True,
                        # action="store",
                        action=_StoreSizeAction,
                        # type=str,
                        dest="size",
                        default="",
                        help="Specify one size, eg: 1T、200GB. "
                            "Default unit is GB. ")
    return parser


def run():
    parser = get_parser()

    args = parser.parse_args()
    # args.size = convert_size(args.size)
    print(f"{args.size=}")
```

执行结果:

```shell
$ python arg_hook.py -s 200MB
args.size='200MB'
$ python arg_hook.py -s 200
args.size='200.0GB'
```

## 使用自定义的Type方法

argparse模块，在处理参数时，如果在 **add_argument方法中指定了type参数**，将会按照type参数指定的类型进行参数转换

```python
class ArgumentParser(_AttributeHolder, _ActionsContainer):
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True):
        ...
        # 默认情况下，如果未指定type参数，直接返回输入的字符串
        # register types
        def identity(string):
            return string
        self.register('type', None, identity)

    ...

    def _get_value(self, action, arg_string):
        type_func = self._registry_get('type', action.type, action.type)
        if not callable(type_func):
            msg = _('%r is not callable')
            raise ArgumentError(action, msg % type_func)

        # convert the value to the appropriate type
        try:
            result = type_func(arg_string)

    ...
    return result
```

利用第一种方式中的转换方法，修改代码如下:

```python
def get_parser():
    parser = argparse.ArgumentParser(description="Test size hook")
    parser.add_argument("-s", "--size",
                        required=True,
                        action="store",
                        # action=_StoreSizeAction,
                        type=convert_size,  # 3. 修改type参数为convert_size方法
                        dest="size",
                        default="",
                        help="Specify one size, eg: 1T、200GB. "
                             "Default unit is GB. ")
    return parser
```

执行结果:

```shell
$ python arg_hook.py -s 200
args.size='200.0GB'
$ python arg_hook.py -s 200MB
args.size='200MB'
```

## 参考

- [argparse action使用](https://docs.python.org/zh-cn/3/library/argparse.html#action)
- [argparse.Action](https://docs.python.org/zh-cn/3/library/argparse.html#argparse.Action)
- [argparse type使用](https://docs.python.org/zh-cn/3/library/argparse.html#type)