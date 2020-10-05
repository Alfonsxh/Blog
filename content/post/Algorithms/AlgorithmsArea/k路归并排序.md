---
title: "k路归并排序"
date: 2018-12-09 21:43:03
lastmod: 2018-12-09 21:43:03
draft: false
keywords: ["Algorithms"]
description: "k路归并排序"
tags: ["Algorithms"]
categories: ["Algorithms"]
author: "Alfons"
---

题目：

```c++
23.Merge k Sorted Lists

Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.

Example:

Input:
[
  1->4->5,
  1->3->4,
  2->6
]
Output: 1->1->2->3->4->4->5->6
```

<!--more-->

分析：

首先呢，输入是一个由 **多个有序的整数数列组成**，输出是 **这些数列排完序后组成的另一个序列**。题目的目的就是要考虑多路输入排序的问题。

- 可以用一个最小堆，将每个数列的首元素都输入堆中。
- 然后将堆中的最小元素输入结果队列中。
- 这时堆中的元素会减少一个，用之前的最小元素的下一个元素补充，如果下一个元素不存在了，则不用补充。
- 依次循环上面的过程，知道所有元素都进入新的队列中。

![merge_K](/images/Algorithms/AlgorithmsArea/merge_K_sorted_lists/merge_K.png)

实现：

```c++
struct ListNode {
    int val;
    ListNode *next;

    ListNode(int x) : val(x), next(nullptr) {}
};

static bool Comper(ListNode *node1, ListNode *node2) {
    return node1->val > node2->val;
}

ListNode *mergeKLists(vector<ListNode *> &lists) {
    // 初始化堆
    std::vector<ListNode *> node_heap;
    node_heap.reserve(lists.size());
    for (auto node: lists) {
        if (node) node_heap.push_back(node);
    }

    if (node_heap.empty())
        return nullptr;

    std::make_heap(node_heap.begin(), node_heap.end(), Comper);

    // 循环读取最小值，并补充元素
    ListNode *result = new ListNode(0);
    ListNode *head = result;
    while (!node_heap.empty()) {
        // 获取最小值，并从堆中剔除它
        std::pop_heap(node_heap.begin(), node_heap.end(), Comper);
        ListNode *min_node = node_heap.back();
        node_heap.pop_back();

        // 存储最小值
        result->next = min_node;
        result = result->next;

        // 将最小元素的下一个元素入堆
        if (min_node->next) node_heap.push_back(min_node->next);
        std::push_heap(node_heap.begin(), node_heap.end(), Comper);
    }

    return head->next;
}
```