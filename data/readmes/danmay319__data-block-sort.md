# data-block-sort
tidb 小作业

---

### 目标

对于以数据块的形式存储在各个分区中的数据进行排序。

---

### 思路

**quick sort**

1. 建立数据块 和 分区，数据块内为数组，一个分区内的数据块用链表相连。
2. 按照分区的顺序，将相邻分区的数据块进行连接，构成一个长链表。
3. 在长链表上进行 quick sort。
4. 将相邻分区数据块之间的链接分开。
5. 记 n 为元素个数，时间复杂度 O(nlogn) ，不需要额外空间。

**merge sort**

1. 同上
2. 对分区进行归并，归并后将相邻分区的数据块进行连接。
3. 在归并的时候，存在数据块重构的情况，假定数据块大小为 S，则当我们从两个序列弹出 2S 个元素的时候，必然有一个数据块完全被弹出，从而我们只需要 S 大小的额外空间。
4. 记 n 为元素个数，数据块大小为 S，分区个数为 T，时间复杂度 O(nlogT)。但是需要额外空间 O(S)，而且破坏了相邻有序数据块在同一分区的性质。

---

### 代码

**data structures/**

* area.h : 实现了分区的数据结构。
  * partition：分区。
  * partition_iter：在分区上的迭代器。
* data_block.h：实现了数据块的数据结构。

**algorithms/**

* qsort_solve：算法 **quick sort** 的实现。
* merge_solve：算法 **merge sort** 的实现。

**main/**

* generator：数据块生成器。
* quick_sort_tester：算法 1 的测试程序。
* merge_sort_tester：算法 2 的测试程序。

*详细参数说明见代码注释*

---

### 运行方法

执行 cmake-build-debug/main.exe

或者编译运行 main.cpp 即可，排序接口为

```c++
void merge_solve(Partition * _a, int _n, int _max_block_size, bool test_print= false)
```

```c++
void q_solve(Partition * _a, int _n, bool test_print= false)
```

测试接口为

```c++
void quick_sort_tester(int cnt_part,int block_per_part,int max_block_size)
```

```c++
void merge_sort_tester(int cnt_part,int block_per_part,int max_block_size)
```

