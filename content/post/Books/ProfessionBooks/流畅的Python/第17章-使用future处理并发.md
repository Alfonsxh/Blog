---
title: "流畅的Python - 第17章-使用future处理并发"
date: 2018-08-18 10:52:18
lastmod: 2018-08-18 10:52:18
draft: false
keywords: ["Books", "流畅的Python"]
description: "第17章-使用future处理并发"
tags: ["Books", "流畅的Python"]
categories: ["Books", "流畅的Python"]
author: "Alfons"
---

本章主要是列举了几个从网站下载例子，主要涉及到了多线程并发。

<!--more-->

## 版本一：依序下载

不使用多线程以及并发技术。编写的代码如下：

```python
# 国旗下载程序，依序下载
import os
import time
import requests

BASE_URL = "http://flupy.org/data/flags/"  # 基本的地址
DEST_DIR = "flags/"  # 保存的文件夹名称

FLAGS_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()  # 下载的国旗缩写


def SaveFlag(img, filename):
    """
    保存国旗文件
    :param img: 原始的图片二进制数据 
    :param filename: 保存的文件名称
    :return: 
    """
    savePath = os.path.join(DEST_DIR, filename.lower())
    with open(savePath, "wb") as f:
        f.write(img)


def Show(flag):
    """
    显示下载
    :param flag: 国旗缩写 
    :return: 
    """
    print(flag, end=" ")


def DownloadOne(flag):
    """
    下载单面旗帜
    :param flag: 旗帜缩写名  
    :return: 旗帜的数据
    """
    downloadUrl = "{base}/{flag}/{flag}.gif".format(base=BASE_URL, flag=flag.lower())
    ret = requests.get(downloadUrl)
    content = ret.content
    return content


def DownloadFlags(flagList: list):
    """
    下载多面旗帜
    :param flagList: 下载旗帜的列表 
    :return: 下载旗帜的数量
    """
    for flag in sorted(flagList):
        image = DownloadOne(flag)
        Show(flag)
        SaveFlag(image, flag.lower() + ".gif")
    return len(flagList)


def main(flagsList):
    """
    主函数入口
    :param flagsList: 旗帜列表 
    :return: 
    """
    os.makedirs(DEST_DIR, exist_ok=True)  # 新建文件夹

    startTime = time.time()
    counts = DownloadFlags(flagsList)
    endTime = time.time()

    print("\nDownload {} flags in {}'s.".format(counts, endTime - startTime))


if __name__ == "__main__":
    main(FLAGS_CC)
```

使用单线程，依序下载，过程中会出现多次IO阻塞。花费的时间较长。

```shell
$ python3 17-01-Flags-1.py 
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN 
Download 20 flags in 8.758476495742798's.

$ python3 17-01-Flags-1.py 
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN 
Download 20 flags in 8.747509002685547's.

$ python3 17-01-Flags-1.py 
BD BR CD CN DE EG ET FR ID IN IR JP MX NG PH PK RU TR US VN 
Download 20 flags in 8.8702871799469's.
```

## 版本二：使用concurrent.futures多线程模块下载

`concurrent.futures`模块主要使用的是`ThreadPoolExecutor`和`ProcessPoolExecutor`类，分别为`线程池`和`进程池`方式。

首先使用`ThreadPoolExecutor`方式，代码如下。

```python

# 下载多面旗帜，线程池方式
import os
import time
import requests
from string import ascii_lowercase
from concurrent import futures

BASE_URL = "http://flupy.org/data/flags/"
DEST_DIR = "flags_futures_thread/"

FLAGS_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()

MAX_WORLERS = 200   # 最大工作线程数


def SaveFlag(img, filename):
    """
    保存国旗文件
    :param img: 原始的图片二进制数据
    :param filename: 保存的文件名称
    :return:
    """
    savePath = os.path.join(DEST_DIR, filename.lower())
    with open(savePath, "wb") as f:
        f.write(img)


def Show(flag):
    """
    显示下载
    :param flag: 国旗缩写
    :return:
    """
    print(flag, end=" ")


def GetFlag(flag):
    """
    下载单面旗帜
    :param flag: 旗帜缩写名
    :return: 旗帜的数据
    """
    downloadUrl = "{base}/{flag}/{flag}.gif".format(base=BASE_URL, flag=flag.lower())
    ret = requests.get(downloadUrl)
    if ret.status_code != 200:
        ret.raise_for_status()
    content = ret.content
    return content


def DownloadOne(flag):
    """
    下载单面旗帜，供线程使用
    :param flag: 旗帜缩写名
    :return: 旗帜的数据
    """
    try:
        image = GetFlag(flag)
    except:
        return ""
    Show(flag)
    SaveFlag(image, flag.lower() + ".gif")
    return flag


def DownloadFlags(flagList: list):
    """
    下载多面旗帜，线程池方式
    :param flagList: 下载旗帜的列表
    :return: 下载旗帜的数量
    """
    workers = min(MAX_WORLERS, len(flagList))
    with futures.ThreadPoolExecutor(workers) as exector:
        res = exector.map(DownloadOne, sorted(flagList))  # 使用线程池来下载
    return len(set(res)) - 1


def main(flagsList):
    """
    主函数入口
    :param flagsList: 旗帜列表
    :return:
    """
    os.makedirs(DEST_DIR, exist_ok=True)

    startTime = time.time()
    counts = DownloadFlags(flagsList)
    endTime = time.time()

    print("\nDownload {} flags in {}'s.".format(counts, endTime - startTime))


if __name__ == "__main__":
    flags = [m + n for m in ascii_lowercase for n in ascii_lowercase]
    main(flags)
```

在此版本中，总共的旗帜下载数量为`26*26 = 676`面。实际下载了`194`面。

```shell
$ python3 17-02-Flags-Futures-ThreadPool.py 
ae ad ag at ao az am ar be bg bh bb bf bj bd bo bs br bw cg cf ci cm co cr af cl ch cn cu cy cz dk dz ee eg fi de fr ba gm bz bt au al dj bi cd ca es gh gb ga bn hn gr gw gn by hu is ec iq cv in dm ge ht it ie et fj id er fm gq jo hr gt gd km gy kr il jp la kg lb jm kw lr mn ls ly lc lu ir ke li lt ml mv ni mt nz ne kn kp lv mk kh mr mm np mg mu nr ki no nl om mx pl ma pa lk mc mw pw kz pg py md my sm ng mh ru so pk sn sl pt se th sd tj ro tt rw pe to ph sr tg sv mz td na me ua tn sc tl rs qa sg st tw si sk tv sb sa sy tr ss ve sz vn ug uz vc tz tm vu uy us ye ws va zw za zm 
Download 194 flags in 2.294755697250366's.

$ python3 17-02-Flags-Futures-ThreadPool.py 
ae ao ad ag am ar at az bd bj bb bh be bf bg bo bw br bs ci af ch cg cf cm cn cl cy dk de co dj cz au cu ba cr bn eg al by fi fr ca ee dz bi bt gb es gn ga gr cd gm gh gw dm ie et it hn bz cv ge fm gq er ec hu id in ht is iq gy gd fj jo gt hr jp kg km kw kr lc la li il ir lb mg ls mm lt mu ly ml ni ke no kh ng mn lu kp pl lr pg kn nz mk lv ma mv pa om mc mz se mr ne td mt mx jm py me np md sy rw nl ru mw ph ki my na rs sd lk pk kz nr sb qa pt st sv sg si pe so sc pw ro sa mh sm sk sz sl tg th sr sn tt ua tm ss tj tl ug uz tn vu to ve tv vc tw tz vn ye us ws uy va tr za zw zm 
Download 194 flags in 2.469243049621582's.
```

可以看见，使用了`200`个线程，下载`676`面旗帜，使用的时间平均才`2s`多。

## 版本三：自定义ThreadPool操作

版本二的多线程版本有个弊端，只能使用相同函数对迭代的参数进行处理。

`ThreadPoolExecutor`中提供了`submit`函数，可以让用户自定义使用的函数。

再通过`futures.as_completed(...)`函数获取所有的结果。

```python
# 使用submit和as_completed完成相同的步骤
def DownloadFlags(flagList: list):
    workers = min(MAX_WORLERS, len(flagList))
    with futures.ThreadPoolExecutor(workers) as executor:
        # res = exector.map(DownloadOne, sorted(flagList))  # 使用线程池来下载

        toDo = list()
        for flag in sorted(flagList):
            future = executor.submit(DownloadOne, flag)
            toDo.append(future)

        res = list()
        for future in futures.as_completed(toDo):
            result = future.result()
            res.append(result)
    return len(list(res))
```

只需要在版本二的基础上，修改`DownloadFlags`的实现，使用两个`for`循环，代替原来的逻辑即可。

## 版本四：多进程版本

在多进程版本中，使用了`ProcessPoolExecutor`类。与`ThreadPoolExecutor`类不同的是，初始化时`ProcessPoolExecutor`类不需要初始化参数，默认值为`os.cpu_count()`，表示使用所有的`CPU`。

```python
# 使用多进程版本下载
def DownloadFlags(flagList: list):
    with futures.ProcessPoolExecutor(os.cpu_count()) as exector:
        res = exector.map(DownloadOne, sorted(flagList))  # 使用线程池来下载
    return len(list(res))
```

与多线程版本不同的是，多进程版本的速度取决于设备`CPU`的核数。例如，现在电脑上的`CPU`只有四个核，也就相当于使用4个线程在下载。

## 版本五：asyncio版本

使用`requests`模块进行下载时，为`阻塞型I/O`。使用`asyncio`和`aiohttp`模块进行下载时，为`异步操作`，是`非阻塞型I/O`。

```python
import os
import time
import asyncio
import aiohttp

BASE_URL = "http://flupy.org/data/flags/"  # 基本的地址
DEST_DIR = "flags_asyncio/"  # 保存的文件夹名称

FLAGS_CC = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()  # 下载的国旗缩写


def SaveFlag(img, filename):
    """
    保存国旗文件
    :param img: 原始的图片二进制数据
    :param filename: 保存的文件名称
    :return:
    """
    savePath = os.path.join(DEST_DIR, filename.lower())
    with open(savePath, "wb") as f:
        f.write(img)


def Show(flag):
    """
    显示下载
    :param flag: 国旗缩写
    :return:
    """
    print(flag, end=" ")


# 从python3.5起，开始引入了新的语法async和await
async def GetFlag(flag):
    """
    下载单面旗帜
    :param flag: 旗帜缩写名
    :return: 旗帜的数据
    """
    downloadUrl = "{base}/{flag}/{flag}.gif".format(base=BASE_URL, flag=flag.lower())
    # response = yield from aiohttp.request("GET", downloadUrl)         # 使用aiohttp.request会出现异常
    response = await aiohttp.ClientSession().get(downloadUrl)  # 将阻塞的操作交由协程完成
    image = await response.read()  # 读取响应也是异步操作
    return image


async def DownloadOne(flag):
    """
    下载单面旗帜，共异步调用
    :param flag: 旗帜的缩写名
    :return:
    """
    image = await GetFlag(flag)     # 异步获取图片的数据
    Show(flag)
    SaveFlag(image, flag + ".gif")
    return flag


def DownloadFlags(flagList: list):
    """
    下载多面旗帜
    :param flagList: 下载旗帜的列表
    :return: 下载旗帜的数量
    """
    loop = asyncio.get_event_loop()  # 返回底层的事件驱动
    toDo = [DownloadOne(cc) for cc in flagList]  # 构建单个下载的生成器队列
    waitWorker = asyncio.wait(toDo)  # 等待传进来的协程列表都结束
    complete, notComplete = loop.run_until_complete(waitWorker)  # 方法驱动，直到所有的任务都结束

    loop.close()
    return len(complete)


def main(flagsList):
    """
    主函数入口
    :param flagsList: 旗帜列表
    :return:
    """
    os.makedirs(DEST_DIR, exist_ok=True)  # 新建文件夹

    startTime = time.time()
    counts = DownloadFlags(flagsList)
    endTime = time.time()

    print("\nDownload {} flags in {}'s.".format(counts, endTime - startTime))


if __name__ == "__main__":
    main(FLAGS_CC)
```

使用`异步`操作在单线程的情况下，20面旗帜下载时间为`1.12s`，大大少于依序下载的情况。

## 各版本下载速度对比

|版本|下载旗帜数|线(进)程数|用时(s)|
|:---:|:---:|:---:|:---:|
|依序下载|20|1|9.36s|
|多线程|20|20|0.75s|
|多线程|20|4|2.61s|
|多进程|20|4|2.93s|
|异步|20|1|1.12s|

## 阻塞型I/O和GIL

在python解释器中，普遍存在着`全局解释器锁(GIL)`，一次只允许使用一个线程执行python字节码。

然而，标准库中所有执行`阻塞型I/O`操作的函数，在等待操作系统返回结果时，都会释放`GIL`。

这意味着，在`I/O密集型`程序中，python的多线程还是能够实现加速的效果。但对于`CPU密集型`程序中，python就不如c/c++了。