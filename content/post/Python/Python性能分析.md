---
title: "Python 性能分析"
date: 2020-06-03 22:53:48
lastmod: 2020-06-03 22:53:48
draft: false
keywords: ["Python"]
description: "Python 性能分析"
tags: ["Python"]
categories: ["Python"]
author: "Alfons"
---

<!--more-->

参考几种性能分析的方式。事例代码如下：

```python
import sys


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n - 1))
    seq.append(fib(n))
    return seq


if __name__ == '__main__':
    print fib_seq(int(sys.argv[1]))
```

## 暴力(time)性能分析

最简单的性能分析方式，使用系统命令 `time`，或者python中的 `timeit、time` 模块。

使用 `time` 方式：

```shell
$ time python test_func.py 30
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040]

real    0m0.622s
user    0m0.610s
sys     0m0.012s
```

整体用时 **0.622s**。

使用python模块的方式：

```python
import timeit
from test_func import fib_seq


def test_code():
    fib_seq(30)


# res = timeit.repeat(test_code, number=1, repeat=5)
res = timeit.timeit(test_code, number=1)
print "timeit use -> {}'s.".format(res)

import time

start_time = time.time()
fib_seq(30)
print "time use -> {}'s.".format(time.time() - start_time)
```

输出：

```shell
timeit use -> 0.599317073822's.
time use -> 0.59308218956's.
```

上面的方式都比较原始，可大致看出程序的耗时，以及某段代码的耗时，但对于细粒度的具体耗时情况，就没有那么细了。

## 栈(cProfile)性能分析

`cProfile` 模块是性能分析模块，实际上是继承了标准库 `_lsprof.Profiler`，对标准库的输出做了一层封装，能够更直观的查看结果。

使用标准库 `_lsprof.Profiler` 进行性能分析：

```python
import _lsprof
from test_func import fib_seq

profile = _lsprof.Profiler()
profile.enable()
fib_seq(30)
profile.disable()

res = profile.getstats()
print "\n".join([str(r) for r in res])

# output：_lsprof.profiler_entry(code="<method 'append' of 'list' objects>", callcount=31, reccallcount=0, totaltime=4.9999999999999996e-06, inlinetime=4.9999999999999996e-06, calls=None)
_lsprof.profiler_entry(code="<method 'extend' of 'list' objects>", callcount=30, reccallcount=0, totaltime=1.7e-05, inlinetime=1.7e-05, calls=None)
_lsprof.profiler_entry(code="<method 'disable' of '_lsprof.Profiler' objects>", callcount=1, reccallcount=0, totaltime=0.0, inlinetime=0.0, calls=None)
_lsprof.profiler_entry(code=<code object fib at 0x7fcb4698fbb0, file "/mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py", line 13>, callcount=7049123, reccallcount=7049092, totaltime=1.271378, inlinetime=1.271378, ...)
_lsprof.profiler_entry(code=<code object fib_seq at 0x7fcb469a5eb0, file "/mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py", line 22>, callcount=31, reccallcount=30, totaltime=1.271494, inlinetime=9.4e-05, ...)
_lsprof.profiler_entry(code="<method 'append' of 'list' objects>", callcount=31, reccallcount=0, totaltime=4.9999999999999996e-06, inlinetime=4.9999999999999996e-06, calls=None)
_lsprof.profiler_entry(code="<method 'extend' of 'list' objects>", callcount=30, reccallcount=0, totaltime=1.7e-05, inlinetime=1.7e-05, calls=None)
_lsprof.profiler_entry(code="<method 'disable' of '_lsprof.Profiler' objects>", callcount=1, reccallcount=0, totaltime=0.0, inlinetime=0.0, calls=None)
_lsprof.profiler_entry(code=<code object fib at 0x7fcb4698fbb0, file "/mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py", line 13>, callcount=7049123, reccallcount=7049092,vprof0, file "/mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py", line 22>, callcount=31, reccallcount=30, totaltime=1.271494, inlinetime=9.4e-05, ...)
```

使用 `cProfile` 模块进行性能分析，结果就更加直观了：

```python
import cProfile
from test_func import fib_seq

profile = cProfile.Profile()
profile.enable()
fib_seq(30)
profile.disable()

profile.print_stats()

#output
         7049216 function calls (94 primitive calls) in 1.271 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
7049123/31    1.271    0.000    1.271    0.041 test_func.py:13(fib)
     31/1    0.000    0.000    1.271    1.271 test_func.py:22(fib_seq)
       31    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
       30    0.000    0.000    0.000    0.000 {method 'extend' of 'list' objects}
```

整体用时 **1.271s**，一共进行了 **7049216次** 函数调用，其中原生函数调用 **94次**，其余的函数调用为递归或者重复调用。

title名解释：

- **ncalls** - 函数调用次数，**7049123/31** 表示，**7049123** 次调用，**31** 次为原生调用，剩余的为重复调用。
- **tottime** - **internal time**，内部耗时，给定函数的所有执行时间（排除了子函数执行时间）
- **percall** - **tottime/ncalls**，单次调用所耗时间，除的是所有调用次数
- **cumtime** - **cumulative time**，累计时间，所有执行时间，包括子函数
- **percall** - **cumtime/ncalls**，单次调用所耗时间，除的是不重复调用次数
- **filename:lineno** - 文件名:行号(函数名)

`cPorfile` 模块中的 **profile.print_stats** 方法调用了 `pstats` 模块。该模块是专门用于打印 **profile** 输出文件。

```python
def print_stats(self, sort=-1):
    import pstats
    pstats.Stats(self).strip_dirs().sort_stats(sort).print_stats()
```

- **strip_dirs** - 方法会去除文件夹路径
- **sort_stats**
  - 排序，以关键字进行排序
  - 关键字包含很多，程序中对title中的字符进行了切割作为关键字，例如 **cumulative time** 的关键字可以是 **cumulativ**、**cumulati**、**cumu**
  - 一般使用title中的名字即可
  - 也支持多个关键字排序，如 **sort_stats("cumtime", "filename")**
- **print_stats**
  - 打印结果，带过滤功能，输入参数可以是函数名关键字，或者数字，也可以是两者的组合
    - 数字可以是整数(int, long)，表示打印排序后，第几位之前的内容
    - 也可以是小数形式(float)，表示输出整个结果的前面百分比，如 **0.1** 表示输出前面10%的内容
  - 函数名和数字的前后关系，会导致结果的不同
    - **print_stats("fib", 0.5)** - 输出包含 **fib** 的函数的前50%的内容
    - **print_stats(0.5, "fib")** - 输出前50%内容，其中函数名中需要包含 **fib**

> (注：其他的一些函数，如 **print_callees**、**print_callers** 使用类似)

```python
print 'print_stats("fib", 0.5)'.center(64, '=')
p.sort_stats("cumu").print_stats("fib", 0.5)

print 'print_stats(0.5, "fib")'.center(64, '=')
p.sort_stats("cumu").print_stats(0.5, "fib")

# output:
====================print_stats("fib", 0.5)=====================
        7049216 function calls (94 primitive calls) in 1.257 seconds

Ordered by: cumulative time
List reduced from 5 to 2 due to restriction <'fib'>
List reduced from 2 to 1 due to restriction <0.5>

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    31/1    0.000    0.000    1.257    1.257 /mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py:22(fib_seq)


====================print_stats(0.5, "fib")=====================
        7049216 function calls (94 primitive calls) in 1.257 seconds

Ordered by: cumulative time
List reduced from 5 to 3 due to restriction <0.5>
List reduced from 3 to 2 due to restriction <'fib'>

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    31/1    0.000    0.000    1.257    1.257 /mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py:22(fib_seq)
7049123/31    1.257    0.000    1.257    0.041 /mnt/3a4a987a-73ee-49eb-bc4b-b34ee82abd09/PythonCode/Python/cProfileTest/test_func.py:13(fib)
```

通过 `cProfile` 模块进行性能分析，主要是通过其产生 **profile** 文件(当然也可以直接打印结果)，后续通过 `pstats` 模块进行解析，输出结果。

其他的一些 `类cProfile` 模块也是通过类似的方式进行性能分析，例如 **line_profile**、**memory_profile** 分别进行了函数行执行性能分析以及内存性能分析。

以上的方式，都是通过注入(hook)的方式，**通过函数正常执行时，加入回调函数来实现时间的统计**，或多或少的 **会影响原生函数执行的性能**。例如未使用cProfile模块时，函数的整体执行时间只有 **0.6s**，使用之后为 **1.2s**。这是函数递归调用过多造成的结果。

性能分析的结果，与实际的结果可能存在些许出入，但整体的时间使用分布能够客观反映。

## 可视化性能分析

### gprof2dot

需要安装 **gprof2dot** 以及 **graphviz**

```shell
sudo apt-get install python3 graphviz
pip install gprof2dot
```

使用 **gprof2dot** 程序将各种性能分析的结果文件转换，再通过 **dot** 程序将转换后的结果 **输出为各类格式的结果保存**。

```shell
gprof2dot -f pstats ./fib.prof | dot -Tjpg -o fib.jpg
```

如上的命令，将 **pstats** 类型的 **cProfile** 分析结果转换，再通过 **dot** 程序输出为jpg文件。最终的输出结果图片如下：

![fib](/images/Python/Python性能分析/fib.jpg)

### vprof

需要安装 **vprof**

```shell
pip install vprof
```

使用 **vprof** 可以通过 **-c** 参数将程序按几种类型进行性能分析，包括 **cpu**、**profile**、**memory graph**、**code heatmap**。可以单独使用，也可以结合使用。

```shell
$ vprof -c cpmh test_func.py
Running MemoryProfiler...
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
Running FlameGraphProfiler...
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
Running CodeHeatmapProfiler...
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
Running Profiler...
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
Starting HTTP server...
正在现有的浏览器会话中打开。
```

![vprof_profiler](/images/Python/Python性能分析/vprof_profiler.png)

官方示意图：

![vprof_office](/images/Python/Python性能分析/vprof_office.gif)

### pyprof2calltree

需要安装 **pyprof2calltree** 以及 **kcachegrind**

```shell
sudo apt-get install -y kcachegrind
pip install pyprof2calltree
```

使用 **pyprof2calltree** 将 **cProfile** 分析的结果文件，进行转化

```shell
pyprof2calltree -i ./fib.prof -k
```

![pyprof2calltree](/images/Python/Python性能分析/pyprof2calltree.png)

> 以上可视化工具都是对一些输出结果做的可视化，显示的更加直观，虽然很炫酷，但个人还是更喜欢直接查看prof文件的方式。

## 第三方工具

**Application Portfolio Management (APM, 应用性能管理)**，国外厂商 **NewRelic** 和 **AppDynamics**，国内厂商 **OneAPM**。

## 参考

- [Python性能分析器](https://blog.vicyu.com/2017/12/26/more-about-python-profiling/)
- [Python优化第一步: 性能分析实践](https://zhuanlan.zhihu.com/p/24495603)
- [gprof2dot](https://github.com/jrfonseca/gprof2dot)
- [vprof](https://github.com/nvdv/vprof)
- [pyprof2calltree](https://github.com/pwaller/pyprof2calltree/)
- [如何选择一款好的 APM 工具？](http://blog.oneapm.com/apm-tech/106.html)