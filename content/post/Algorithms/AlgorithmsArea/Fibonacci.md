---
title: "Fibonacci数列"
date: 2018-10-09 21:57:47
lastmod: 2018-11-27 21:07:00
draft: false
keywords: ["Algorithms"]
description: "Fibonacci数列"
tags: ["Algorithms"]
categories: ["Algorithms"]
author: "Alfons"
---

已知 $$F_0 = 0, F_1 = 1, F_n = F_{n-1} + F_{n-2}$$

## 传统递归方式

```python
def FibsRecursion(n):
    if n == 0:
        return 0

    if n == 1:
        return 1
    return FibsRecursion(n - 1) + FibsRecursion(n - 2)
```

传统递归方式需要计算许多重复的值，时间复杂度为 $O(2^n)$。

<!--more-->

## 含有备忘录的递归方式

```python
cache = {0: 0, 1: 1}

def FibsRecursionCache(n):
    if n in cache:
        return cache[n]

    ret = FibsRecursionCache(n - 1) + FibsRecursionCache(n - 2)
    cache[n] = ret
    return ret
```

改进的方式为，将n计算得到的值保存在字典中，当下次计算相同值时，直接从字典中取出该值，避免了重复计算多次。

改进后的时间复杂度为$O(n)$，空间复杂度为$O(n)$。

另一种使用列表存储的方式与上述方式类似，只不过存放cache的数据结构为list。

```python
fibs = [0, 1]

def FibsList(numZS):
    for i in range(numZS - 1):
        fibs.append(fibs[-2] + fibs[-1])

    return fibs[-1]
```

结果只需返回列表的最后一个元素即可。

## 使用中间变量保存值

```python
def FibsWithTempValue(n):
    i = 0
    first = 0
    second = 1

    while i < n - 1:
        tmp = first
        first = second
        second += tmp
        i += 1

    return second
```

该方法使用两个中间变量分别保存每次计算的$F_{n-2}$和$F_{n-1}$。最后返回即为n时的Fibonacci数列的值。

改进后的时间复杂度为$O(n)$，空间复杂度为$O(1)$。

## 矩阵表示

```python
def FibsMatrix(n):
    if n <= 0:
        return 0, 1

    f_m, f_m1 = FibsMatrix(int(n / 2))

    if n % 2 == 0:
        return 2 * f_m1 * f_m - f_m ** 2, f_m ** 2 + f_m1 ** 2

    return f_m ** 2 + f_m1 ** 2, f_m1 ** 2 + 2 * f_m1 * f_m
```

此方法使用矩阵方法化简后，得到通项。

1、当n为奇数时，n = 2m + 1
>$F_{n+1} = F_{2m+2} = F_{m+1}^2 + 2F_mF_{m+1}$
$F_{n} = F_{2m+1} = F_{m+1}^2 + F_m^2$

2、当n为偶数时，n = 2m
>$F_{n+1} = F_{2m+1} = F_{m+1}^2 + F_m^2$
$F_{n} = F_{2m} = 2F_mF_{m+1} - F_m^2$

改进后的时间复杂度为$O(logn)$，空间复杂度为$O(1)$。

## 通项公式

通过计算得到Fibonacci的通项公式，直接求出n时的值。

时间复杂度为$O(1)$，空间复杂度为$O(1)$。