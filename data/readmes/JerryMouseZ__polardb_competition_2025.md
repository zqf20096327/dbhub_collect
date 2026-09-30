# 代码设计与实现文档

## 基本信息

- 队伍 ID：1322410
- 队伍名称：鼠鼠不想写内核
- 成员信息：
  - 蒋璋，南开大学，计算机科学与技术，博士三年级
  - 雷万魁，南开大学，计算机技术，硕士二年级
  - 刘兴泽，南开大学，计算机科学与技术，博士一年级
- 指导教师 宫晓利 李浩然
- **联系方式（手机）**：18180409139
- 代码仓库地址：https://gitee.com/JJeJZ/polardb_competition_2025.git
- 最佳成绩代码提交 ID：be85d99f19368cea30cdcf7d32eef661d2890274

```c++
POLAR_REPO=https://gitee.com/JJeJZ/polardb_competition_2025.git
POLAR_COMMIT=be85d99f19368cea30cdcf7d32eef661d2890274
```

## 目录

- [核心优化思路](#核心优化思路)
  - [1. 整体优化效果](#1-整体优化效果)
  - [2. 关键优化策略](#2-关键优化策略)
- [优化核心设计与关键技术](#优化核心设计与关键技术)
  - [一、环境构建](#一环境构建)
  - [二、系统级工程优化](#二系统级工程优化)
    - [2.1 HNSW 的布局优化](#21hnsw-的布局优化)
      - [问题分析](#问题分析)
      - [基于mmap 的全局内存池和扁平数组解决方案](#基于mmap-的全局内存池和扁平数组解决方案)
      - [性能分析](#性能分析)
    - [2.2 索引并行构建优化](#22索引并行构建优化)
      - [问题分析](#问题分析-1)
      - [索引并行构建设计与实现](#索引并行构建设计与实现)
      - [并行构建中的并发控制与锁优化策略](#并行构建中的并发控制与锁优化策略)
      - [性能分析](#性能分析-1)
    - [2.3 启发式邻居选择优化（shrink_neighbor_list）](#23-启发式邻居选择优化shrink_neighbor_list)
      - [问题分析](#问题分析-2)
      - [启发式邻居选择（shrink_neighbor_list）的原理与设计](#启发式邻居选择shrink_neighbor_list的原理与设计)
    - [2.4 批处理距离计算优化](#24批处理距离计算优化)
      - [问题分析](#问题分析-3)
      - [批处理距离计算算法原理与设计](#批处理距离计算算法原理与设计)
      - [SIMD 距离运算算子优化](#simd-距离运算算子优化)
      - [性能分析](#性能分析-2)
    - [2.5 MinMax Heap的SIMD优化](#25-minmax-heap的simd优化)
      - [问题分析](#问题分析-4)
      - [优化原理与设计](#优化原理与设计)
    - [2.6 查询相关的"上下文"结构优化](#26-查询相关的上下文结构优化)
      - [问题分析](#问题分析-5)
      - [缓存查询相关的"上下文"结构优化设计与实现](#缓存查询相关的上下文结构优化设计与实现)
  - [三、AI 驱动的优化](#三ai-驱动的优化)
    - [3.1 自动调优工作流](#31自动调优工作流)
    - [3.2 Perf自动根因分析工作流](#32-perf自动根因分析工作流)
    - [3.3 基于规整约束的Faiss HNSW转译工作流](#33-基于规整约束的faiss-hnsw转译工作流)
- [存在的问题与改进方向](#存在的问题与改进方向)

## 核心优化思路

### 1. 整体优化效果 

​	 针对比赛优化pg-vector的向量索引构建和向量查询的性能的目标，我们以 HNSW 算法为核心,移植Faiss HNSW核心算法，结合 `perf` 性能热点分析，实施了系统工程优化、 LLM辅助算法移植与调优的优化手段。 在保证 **Recall > 0.85** 的前提下，取得显著突破：

- **索引构建效率提升 2.6 倍**：耗时从 568,697ms 缩减至 **216,103ms**。
- **查询吞吐量（QPS）提升 3.8 倍**：从 3,431 提升至 **13,158**。

### 2. 关键优化策略

- **系统级工程优化：**移植Faiss HNSW的核心算法如并行构建、启发式邻居选择、MinMax heap堆的高效实现并进行数据结构与内存布局优化、访问链路扁平化、锁并行性优化、向量矩阵SIMD算子和缓存查询相关的“上下文”结构等优化。
- **AI 驱动的系统优化工具：** 使用 Codex 和 Claude Code 等 Code Agent，构建自动调优工作流（Workflow）和自动profiling优化工作流，来实现系统代码的精细化调优以及通过“基于规整约束的AI辅助转译”，高效完成 Faiss 核心算法逻辑移植。

## 优化核心设计与关键技术

### 一、环境构建

​	首先我们在本地构建出和线上一样的运行环境和完整的向量数据库基准测试框架，通过 taskset 实现 CPU 核心绑定（数据库和测试进程分别绑定奇偶核心）、systemd-run 限制内存来实现资源隔离；使用 rsync 增量同步实现数据库和索引的快速备份恢复，配合 pg_prewarm 预热加速重复测试；支持 perf（CPU 采样）、wallclock（on-off cpu采样）、perf_lock（锁竞争）等性能分析方式，可在索引构建和查询阶段分别启用，通过获取 PostgreSQL 后端 PID 进行精准采样。

### 二、系统级工程优化

性能分析：基于向量数据库基准测试框架对系统进行**on-off结合的profile**分析发现**HNSW 向量索引在运行CPU 时间主要消耗在  Buffer 管理上，而不是向量计算本身**

![](figures/on-off火焰图.png)

### 2.1HNSW 的布局优化

####  问题分析

**pgvector HNSW的布局**：PostgreSQL 采用固定大小的 8KB 页面作为数据存储的基本单元。


```c
                            ┌─────────────────────────────────────────────────────────────────┐
                            │                    HNSW Index Memory Layout                     │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ Page 1: Index Meta Page (8KB)                                   │
                            │  - entry point, max level, M, efConstruction                    │
                            │  - 页头开销：24 字节                                              │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ Page 2: Element Page (8KB)                                      │
                            │  - 元素 1-10 的元数据                                             │
                            │  - 每个元素：level, neighbor page pointers                        │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ Page 3: Neighbor List Page (8KB)                                │
                            │  - 某些元素的邻居列表                                              │
                            │  - 可能跨多个页面                                                 │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ Page 4: Vector Data Page (8KB)                                  │
                            │  - 向量数据（与元素分离）                                           │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ ... (更多页面，分散在磁盘上)                                        │
                            └─────────────────────────────────────────────────────────────────┘
```

**向量访问流程**：

原始 pgvector 的 HNSW向量查询触发 HNSW 的 IndexScan 后，访问某个元素页会调用 ReadBuffer()，它先在共享缓冲区的 Buffer Mapping Table 里用 BufferTag 做哈希查找（命中直接返回对应 buffer，未命中则读盘并建立映射），随后对 buffer 加 LockBuffer() 共享锁，取 BufferGetPage() 得到页指针，用 PageGetItem() 解出元素 tuple，解析出向量字段并计算距离。

核心链路如下（按运行时搜索）：

```c
查询 → IndexScan → ReadBuffer() → Buffer Mapping Table hash 查找 (BufferTag → buffer_id) → LockBuffer() → BufferGetPage() → PageGetItem() → 解析 Tuple → 获取向量的路径，
```

**问题**：

  1. HNSW 的元素页/邻居页是分离的，访问路径会在页之间跳转，导致大量随机内存访问和 cache miss；
  2. 每次访问都要走 ReadBuffer → hash 查找 → lock → 解页 → tuple 解析，buffer manager 的哈希/锁/引用计数开销仍在；
  3. 向量内联在 tuple 里，读取与解析带来额外解包成本，且不利于连续访问与 SIMD 友好布局。

####  基于mmap 的全局内存池和扁平数组解决方案

基于本次比赛的场景，向量索引和数据全在内存当中，我们设计了基于mmap 的全局内存池和扁平数组，从而

- 避免 ReadBuffer/哈希查找/锁/解页/tuple 解析的路径开销，降低每次距离计算的固定成本。
- 减少元素页/邻居页/向量页分散导致的随机内存访问与 cache miss（改为扁平数组顺序访问）。
- 向量 zero‑copy（全局 vecstore），避免频繁拷贝与解包。
- 预分配 + 连续内存，降低碎片与分配锁竞争，提升并发稳定性与延迟可预测性。

其内存布局和HNSW index布局如下图所示：

```c
                        	┌─────────────────────────────────────────────────────────────────┐
                            │                    HnswInMemPool (mmap 映射区)                   │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ HnswInMemPoolHeader (池头)                                       │
                            │  - magic, version (验证标识)                                     │
                            │  - totalSize, usedSize (容量管理)                                │
                            │  - registryLock, allocatorLock (并发控制)                        │
                            │  - registryOffset (索引注册表偏移)                               │
                            │  - globalStoreOffset (全局向量存储偏移)                          │
                            │  - freeSpaceOffset (空闲空间起始)                                │
                            │  - freeBlocks[] (空闲块列表，用于内存回收)                       │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ Registry[64] (索引注册表)                                        │
                            │  - indexOid → indexOffset 映射                                   │
                            │  - 支持最多 64 个索引                                            │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ HnswInMemGlobalStore (全局向量存储)                              │
                            │  - dimensions, vectorSize (向量几何信息)                         │
                            │  - maxVectors (容量，默认 10M)                                   │
                            │  - vectors[maxVectors] (紧凑向量数组)                            │
                            │  - heaptids[maxVectors] (heaptid 映射表)                         │
                            │  - 预分配：10M * 200 * 2 bytes ≈ 3.7GB                          │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ HnswInMemIndex #1 (索引 1)                                       │
                            │  ├─ HnswInMemIndex 结构体 (元数据)                               │
                            │  ├─ levels[maxElements] (uint8, 每个元素的层级)                 │
                            │  ├─ offsets[maxElements+1] (uint64, 邻居数组偏移)               │
                            │  ├─ neighborCounts[maxElements] (uint16, 每层邻居数)             │
                            │  ├─ neighbors[neighborPoolSize] (uint32, 扁平化邻居存储)         │
                            │  ├─ neighborDistances[neighborPoolSize] (float, 边距离)          │
                            │  └─ elementLocks[maxElements] (LWLock, 元素级锁)                │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ HnswInMemIndex #2 (索引 2)                                       │
                            │  └─ ... (同上结构)                                               │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ ... (更多索引)                                                   │
                            ├─────────────────────────────────────────────────────────────────┤
                            │ Free Space (空闲空间)                                            │
                            └─────────────────────────────────────────────────────────────────┘
```

------

##### 扁平化数组设计细节

###### 设计理念

传统链表结构：
```c
// 传统方式：每个元素是独立对象，邻居通过指针链接
struct Element {
    int level;
    Neighbor* neighbors[MAX_LEVEL];  // 指针数组
};
```

扁平化数组结构：
```c
// FAISS 方式：所有数据在连续数组中
levels[i]     → 元素 i 的层级
offsets[i]    → 元素 i 的邻居在 neighbors[] 中的起始位置
neighbors[offsets[i]...] → 元素 i 的所有邻居（所有层级连续存储）
```

###### 邻居存储布局

单个元素的邻居布局（假设元素在 level 2，M=16）：

```
offsets[i] = 1000

neighbors[1000:1000+72] = 
  ┌─────────────────────────────────────────────────────────┐
  │ L0 邻居 (32 个)  │ L1 邻居 (16 个) │ L2 邻居 (16 个)  │
  └─────────────────────────────────────────────────────────┘
    ↑                  ↑                 ↑
    cum_nneighbor[0]   cum_nneighbor[1]  cum_nneighbor[2]
```

###### 访问方式：

```c
// 获取元素 i 在 layer L 的邻居
uint32* layerNeighbors = HnswInMemGetLayerNeighbors(index, i, L);
// 等价于：
uint32* allNeighbors = &neighbors[offsets[i]];
uint32* layerNeighbors = &allNeighbors[cum_nneighbor_per_level[L]];
```

######  邻居数量管理

```c
typedef struct HnswInMemNeighborCounts {
  uint16 counts[HNSW_INMEM_MAX_LEVEL + 1];
} HnswInMemNeighborCounts;

// 每个元素一个 NeighborCounts 结构
// counts[L] = 元素在 layer L 的实际邻居数（≤ M）
```

**为什么需要 neighborCounts？**

- `offsets` 只记录起始位置，不记录每层的实际邻居数
- 每层预分配 M 个槽位，但实际可能只用了部分
- `counts[L]` 记录实际有效邻居数，避免遍历无效槽位

##### 内存分配与初始化策略

######  启动时初始化

利用**Huge page**来减少 TLB miss，提高地址转换效率；

使用**预热页面**的方式来减少最初的minor page fault；

使用**mlock**防止内存换出到 swap导致查询时的 major page fault。

```c
void HnswInMemShmemInit(void) {
    Size poolSize = hnsw_inmemory_size_mb * 1024 * 1024;
    
    // 1. 打开/创建持久化文件
    fd = open("$PGDATA/pg_hnsw_inmem_pool", O_RDWR | O_CREAT);
    ftruncate(fd, poolSize);
    
    // 2. mmap 映射
    HnswInMemPool = mmap(NULL, poolSize, 
                         PROT_READ | PROT_WRITE,
                         MAP_SHARED, fd, 0);
    
    // 3. 启用 Transparent Huge Pages
    madvise(HnswInMemPool, poolSize, MADV_HUGEPAGE);
    
    // 4. 预热页面（避免首次访问的页面错误）
    memset(HnswInMemPool, 0, poolSize);
    
    // 5. 锁定内存（避免被换出）
    mlock(HnswInMemPool, poolSize);
    
    // 6. 初始化池头
    HnswInMemPool->magic = HNSW_INMEM_MAGIC;
    HnswInMemPool->version = HNSW_INMEM_VERSION;
    // ...
    
    // 7. 初始化全局向量存储
    HnswInMemGlobalVecStore = (HnswInMemGlobalStore*)
        ((char*)HnswInMemPool + globalStoreOffset);
    // ...
}
```

#### 性能分析

从火焰图分析可以看出：降低了在搜索中Buffer相关的开销，提升了计算的占比，整体加快查询速度。

![](figures/batch.png)

### 2.2索引并行构建优化

#### 问题分析

原来pgvector的HNSW索引在构建阶段具有显著的**顺序依赖特性**。在实现中，每个向量需按照既定顺序逐一插入索引结构；插入过程涉及多层级图搜索、候选邻居筛选、双向边更新以及入口点维护等操作。这些步骤在逻辑上高度耦合，且对已有图结构存在强依赖，使得构建流程天然偏向串行执行。

#### 索引并行构建设计与实现

索引并行构建的目标是对 HNSW 构建流程进行工程化重组，使并发成为默认状态、串行成为例外。整体设计遵循三个基本原则：其一，最大化可并行区域，凡是不存在数据依赖的操作均应并行执行；其二，将不可避免的全局共享状态压缩到最小范围，并限制其访问时长；其三，以细粒度锁替代全局锁，确保锁仅保护最小必要的数据结构。在此基础上，构建流程被拆分为预分配、并行插入与构建后优化三个阶段，既明确了并行边界，也降低了实现与调试复杂度。

##### 并行构建流程的阶段化实现

构建的第一阶段为预分配阶段，其核心目的是在正式插入前一次性完成所有内存相关准备工作。每个元素在该阶段被分配固定的内存槽位，同时预先生成随机层级并初始化邻居数组结构。由于这一过程不存在元素间依赖，可直接采用数据并行方式执行。通过提前完成内存分配，后续插入阶段不再涉及内存池扩展或分配锁，从根源上消除了构建过程中最隐蔽、也是代价最高的一类竞争。

```c
#pragma omp parallel for num_threads(numThreads) schedule(static)
for (uint32 i = 0; i < elementCount; i++) {
    uint32 allocId = HnswInMemAllocOnlyAtId(index, i);
    if (allocId == HNSW_INMEM_INVALID_ID)
        elog(ERROR, "Failed to allocate element %u", i);
}
```

第二阶段为并行插入阶段，也是整个方案的核心。该阶段采用 OpenMP 多线程模型，每个线程维护独立的 HNSW 运行视图，但共享底层图存储结构。插入任务以“元素”为最小调度单元，并使用 `schedule(dynamic, 1)` 的动态调度策略，以应对不同元素层级差异带来的插入成本不均问题。这样可以避免高层节点集中在少数线程中，显著改善负载均衡。

```
#pragma omp parallel num_threads(numThreads)
{
    #pragma omp for schedule(dynamic, 1)
    for (uint32 i = 0; i < elementCount; i++) {
        hnsw_add_with_locks(&hnsw, i, level);
    }
}
```

在并行插入过程中，HNSW 算法仍然依赖少量全局状态，主要包括入口点及其层级信息。这部分状态更新频率极低，但读取频繁，因此被严格限制在极短的临界区内，通过自旋锁进行保护，并且不将该锁传播到插入主路径中，从而避免对整体并行度产生实质性影响。

```
SpinLockAcquire(&index->stateLock);
hnsw.entry_point = index->entryPointId;
hnsw.max_level   = index->entryLevel;
SpinLockRelease(&index->stateLock);
```

构建完成后，可以选择性地进入第三阶段，即图结构优化阶段。该阶段不影响索引构建的正确性，仅用于改善图的局部质量，例如修剪过长的邻居列表、修复潜在的孤立节点或进行局部重连。这些操作只涉及已存在结构的局部调整，因而同样具备良好的并行执行条件。

#### 并行构建中的并发控制与锁优化策略

##### 细粒度锁设计

并行插入能够成立的关键在于对并发修改的精细控制。设计中采用“每元素一把锁”的细粒度锁模型，所有写操作仅在必要时获取对应元素的独占锁，严禁使用覆盖整个构建过程的全局锁。搜索、距离计算与候选生成等纯读操作完全无锁执行，从而保证插入主路径的并发性。

```c
LWLock *lock = HnswInMemGetElementLock(index, elementId);
LWLockAcquire(lock, LW_EXCLUSIVE);
add_neighbors(...);
LWLockRelease(lock);
```

#####  严格的锁排序规则

当插入操作需要同时修改两个节点（例如建立双向连接）时，系统通过固定的锁排序规则避免死锁：所有线程必须按照元素 ID 的升序获取锁。由于锁顺序全局一致，循环等待在逻辑上被彻底消除。

```
uint32 first  = min(id1, id2);
uint32 second = max(id1, id2);

LWLockAcquire(GetElementLock(first),  LW_EXCLUSIVE);
LWLockAcquire(GetElementLock(second), LW_EXCLUSIVE);
```

此外，构建进度与统计信息使用原子变量进行维护，避免为非结构性数据引入额外锁，从而进一步降低锁竞争概率。

#### 性能分析

原始构建火焰图

![](figures/索引构建原始.png)

优化后构建火焰图：

![](figures/并行构建的火焰图.png)

#### 

### 2.3 启发式邻居选择优化（shrink_neighbor_list）

`shrink_neighbor_list` 是 HNSW 构建过程中用于控制邻居分布质量的关键算法，其目标并非简单地选取与查询点距离最近的若干节点，而是通过启发式规则，构造一个在空间上更加分散、方向覆盖更全面的邻居集合，从而提升图结构的可达性与搜索鲁棒性。

#### 问题分析

在简单的最近邻选择策略中存在的问题可以通过下图说明：

```c
查询点 Q
    |
    |  d1=0.5
    v
  点 A ----d2=0.3---- 点 B
    |                  |
    |                  |
  点 C                点 D
```

在简单的最近邻选择策略中，往往会直接选择距离查询点 Q 最近的节点，例如 A 与 B。然而，由于 A 与 B 之间的距离本身非常接近（d2=0.3），二者在空间上高度相关，B 在搜索过程中所能提供的方向信息几乎完全被 A 覆盖，属于典型的冗余连接。

#### 启发式邻居选择（shrink_neighbor_list）的原理与设计

启发式邻居选择算法通过引入“覆盖”概念避免这一问题，其执行逻辑如下：

```
1. 选择 A（距离 Q 最近）
2. 考虑 B：dist(B, A) = 0.3 < dist(B, Q) = 0.6
   → B 被 A 覆盖，不选择
3. 选择 C 或 D（与 A 距离较远）
结果：A, C 或 A, D —— 邻居分布更加分散
```

从几何角度看，算法要求每一个新加入的邻居都必须为查询点提供一个**未被已有邻居占据的搜索方向**。如果某个候选节点与已选邻居之间的距离小于其到查询点的距离，则说明该候选节点位于已有邻居的“阴影区域”内，其方向信息是冗余的，因此应当被剔除。

这一启发式规则直接缓解了邻居聚簇问题，其效果可通过下图直观对比：

```
简单选择：
Q -> [A, A', A'', B, B', B'']
     ↑ 聚簇1       ↑ 聚簇2

启发式选择：
Q -> [A, B, C, D, E, F]
     ↑ 分布在不同方向
```

通过抑制同一方向上的重复连接，最终形成的邻居集合在空间上更加均匀，每个邻居都对应一条潜在的搜索扩展路径。这种结构性的差异在搜索阶段具有决定性意义：当搜索沿某一方向进入局部最优或死胡同时，分散的邻居能够为算法提供跨区域跳跃的可能性，从而显著降低搜索失败或召回率下降的风险。

从整体图结构角度来看，`shrink_neighbor_list` 实际上是在构建阶段对 HNSW 图施加了一种局部几何约束，使得每个节点的出边不仅数量受限，而且在方向上具有多样性。这一约束提升了图的覆盖范围，减少了搜索路径对初始入口点和局部结构的敏感性，并在高维空间中有效改善了搜索路径质量。

在工程实现上，该算法以一个按查询距离排序的候选堆作为输入，按照“从近到远”的顺序逐一处理候选节点，并动态维护已选邻居集合。对于每一个候选节点，仅需计算其与当前已选邻居之间的对称距离，即可判断其是否被覆盖，计算过程局部、确定、无全局依赖，非常适合在并行构建环境中使用。其核心实现如下：

**启发式邻居选择代码实现：**

```c
/**
 * shrink_neighbor_list - 启发式邻居选择
 * 
 * @param input: 候选邻居（按距离排序的最大堆）
 * @param output_ids: 输出的邻居 ID 数组
 * @param output_size: 输出邻居数量
 * @param max_size: 最大邻居数量（M）
 * @param sym_distance_func: 对称距离函数
 * @param user_data: 用户数据（索引指针）
 */
static void shrink_neighbor_list_internal(
        farther_heap_t* input,
        hnsw_storage_idx_t* output_ids,
        int* output_size,
        int max_size,
        hnsw_symmetric_distance_func_t sym_distance_func,
        void* user_data) {
    
    *output_size = 0;
    
    /* 从最近的候选开始处理 */
    while (input->size > 0 && *output_size < max_size) {
        /* 弹出距离查询点最近的候选 */
        node_dist_farther_t v1 = farther_heap_pop(input);
        int good = 1;
        
        /* 检查 v1 是否被已选邻居"覆盖" */
        for (int i = 0; i < *output_size; i++) {
            /* 计算 v1 到已选邻居的距离 */
            float dist_v1_v2 = sym_distance_func(user_data, output_ids[i], v1.id);
            
            /* 如果 v1 到某个已选邻居的距离 < v1 到查询点的距离
             * 说明该邻居已经"覆盖"了 v1 的方向，v1 是冗余的 */
            if (dist_v1_v2 < v1.d) {
                good = 0;
                break;
            }
        }
        
        /* v1 不被任何已选邻居覆盖，选择它 */
        if (good) {
            output_ids[(*output_size)++] = v1.id;
        }
    }
}
```

###  2.4批处理距离计算优化

#### 问题分析

在原始实现中，邻居节点的距离计算以逐节点、单次函数调用的方式进行，该实现方式在性能上存在明显不足。大量细粒度函数调用引入了显著的调用开销，破坏了指令流水的连续性；查询向量在重复计算过程中频繁被加载，导致缓存局部性较差、数据复用率偏低；此外，计算流程难以进行向量化或批量展开，从而限制了指令级并行性以及 SIMD 优化的潜在收益。

#### 批处理距离计算算法原理与设计

**核心思想**：将多个独立的距离计算请求进行聚合，一次性批量完成计算，以摊薄函数调用成本并提升缓存与计算资源利用率。

具体做法是：

- 在遍历邻居节点时，**先缓存若干待计算节点 ID**；
- 当缓存达到固定批大小（如 4）时，调用**批处理距离函数**一次性计算多个距离；
- 查询向量仅加载一次，在同一循环中并行计算多个候选向量的距离；
- 对不足一个批次的剩余节点，回退到单点计算逻辑，保证算法完整性。

算法实现：

```c
static int search_from_candidates(
        const hnsw_t* hnsw,
        hnsw_minimax_heap_t* candidates,
        hnsw_visited_table_t* vt,
        hnsw_stats_t* stats,
        int level, int k, int efSearch,
        float* distances, hnsw_storage_idx_t* labels,
        int nres)
{
    int counter = 0;
    hnsw_storage_idx_t saved_j[4];  // 批处理缓冲区

    while (candidates->nvalid > 0) {
        float d0 = 0;
        int v0 = hnsw_minimax_heap_pop_min(candidates, &d0);

        if (v0 < 0)
            break;

        /* 检查停止条件 */
        int n_dis_below = hnsw_minimax_heap_count_below(candidates, d0);
        if (n_dis_below >= efSearch)
            break;

        /* 获取 v0 的邻居 */
        const uint32 *neighbors = get_neighbors(hnsw, v0, level);
        int num_neighbors = get_neighbor_count(hnsw, v0, level);

        /* 遍历邻居，累积到批处理缓冲区 */
        for (int i = 0; i < num_neighbors; i++) {
            hnsw_storage_idx_t j = neighbors[i];

            if (!hnsw_visited_table_get(vt, j)) {
                hnsw_visited_table_set(vt, j);
                saved_j[counter++] = j;

                /* 累积了 4 个，触发批量距离计算 */
                if (counter == 4) {
                    float dis[4];

                    if (hnsw->batch_distance_func != NULL) {
                        hnsw->batch_distance_func(
                            hnsw->distance_user_data,
                            saved_j[0], saved_j[1], saved_j[2], saved_j[3],
                            &dis[0], &dis[1], &dis[2], &dis[3]);

                        stats->ndis += 4;

                        /* 批量加入候选堆 */
                        for (int id4 = 0; id4 < 4; id4++) {
                            hnsw_minimax_heap_push(
                                candidates, saved_j[id4], dis[id4]);
                        }
                    }
                    counter = 0;
                }
            }
        }
    }

    /* 处理剩余的 1-3 个节点 */
    for (int icnt = 0; icnt < counter; icnt++) {
        float dis = hnsw->distance_func(
            hnsw->distance_user_data, saved_j[icnt]);
        hnsw_minimax_heap_push(candidates, saved_j[icnt], dis);
        stats->ndis++;
    }

    return nres;
}

```

####  SIMD 距离运算算子优化

##### 问题分析

在距离计算的热点循环中，标量实现存在典型瓶颈：

- **每次仅处理 1 个维度元素**，128 维需要 128 次迭代，循环与指令开销显著；
- **half→float 转换与算术交织**，无法充分利用宽向量与 FMA 单元；
- **4 路距离（batch4）虽然具备并行结构**，但在标量路径下仅体现为“多次重复计算”，吞吐受限于标量执行宽度。

##### 优化原理与设计

**核心思想**：使用 AVX512 将“按元素串行”改为“按向量块并行”，每轮处理 **16 个维度元素**，并在同一轮中同时更新 4 路距离累加器，实现计算密度与吞吐率提升。

**设计实现关键点：**

- **向量化粒度**：AVX512 寄存器宽度 512-bit，可容纳 **16 个 float**；
- **数据格式**：输入为 half，需使用 `_mm512_cvtph_ps` 将 **16 个 half 一次性转换为 16 个 float**；
- **并行结构**：对 batch4 的四个候选向量分别维持 `acc0~acc3` 四个 512-bit 累加器；
- **FMA 融合**：用 `_mm512_fmadd_ps(diff, diff, acc)` 将 `diff*diff + acc` 融合为单指令，减少指令数并提升执行吞吐；
- **尾部处理**：维度非 16 倍数时，使用 `__mmask16` 掩码加载与计算，避免标量回退；
- **归约输出**：循环结束后，将 16 lane 的向量累加器水平归约为标量距离。

**标量 vs SIMD 实现对比**

```c
// 标量版本：每次处理 1 个元素
for (int i = 0; i < dim; i++) {
    float x = query[i];
    float diff0 = x - data0[i];
    float diff1 = x - data1[i];
    float diff2 = x - data2[i];
    float diff3 = x - data3[i];
    acc0 += diff0 * diff0;
    acc1 += diff1 * diff1;
    acc2 += diff2 * diff2;
    acc3 += diff3 * diff3;
}
// 处理 128 维：128 次迭代
// AVX512 版本：每次处理 16 个元素
TARGET_AVX512F static void
HalfvecL2SquaredDistanceBatch4Avx512f(
    int dim, const half *ax,
    const half *bx0, const half *bx1, const half *bx2, const half *bx3,
    float *d0, float *d1, float *d2, float *d3) {

    int count = (dim / 16) * 16;
    int i;

    // 4 个 512 位累加器（每个可容纳 16 个 float）
    __m512 acc0 = _mm512_setzero_ps();
    __m512 acc1 = _mm512_setzero_ps();
    __m512 acc2 = _mm512_setzero_ps();
    __m512 acc3 = _mm512_setzero_ps();

    // 每次迭代处理 16 个元素
    for (i = 0; i < count; i += 16) {
        // 1. 加载查询向量（16 个 half -> 16 个 float）
        __m256i a_half = _mm256_loadu_si256((__m256i *)(ax + i));
        __m512 a_ps = _mm512_cvtph_ps(a_half);  // 一次转换 16 个

        // 2. 加载 4 个数据向量
        __m512 b0_ps = _mm512_cvtph_ps(_mm256_loadu_si256((__m256i *)(bx0 + i)));
        __m512 b1_ps = _mm512_cvtph_ps(_mm256_loadu_si256((__m256i *)(bx1 + i)));
        __m512 b2_ps = _mm512_cvtph_ps(_mm256_loadu_si256((__m256i *)(bx2 + i)));
        __m512 b3_ps = _mm512_cvtph_ps(_mm256_loadu_si256((__m256i *)(bx3 + i)));

        // 3. 计算差值（16 个并行）
        __m512 d0v = _mm512_sub_ps(a_ps, b0_ps);
        __m512 d1v = _mm512_sub_ps(a_ps, b1_ps);
        __m512 d2v = _mm512_sub_ps(a_ps, b2_ps);
        __m512 d3v = _mm512_sub_ps(a_ps, b3_ps);

        // 4. FMA：diff * diff + acc（16 个并行）
        acc0 = _mm512_fmadd_ps(d0v, d0v, acc0);
        acc1 = _mm512_fmadd_ps(d1v, d1v, acc1);
        acc2 = _mm512_fmadd_ps(d2v, d2v, acc2);
        acc3 = _mm512_fmadd_ps(d3v, d3v, acc3);
    }

    // 5. 处理剩余元素（使用掩码）
    if (i < dim) {
        __mmask16 mask = (1U << (dim - i)) - 1U;
        __m256i a_half = _mm256_maskz_loadu_epi16(mask, ax + i);
        __m512 a_ps = _mm512_cvtph_ps(a_half);
        __m512 b0_ps = _mm512_cvtph_ps(_mm256_maskz_loadu_epi16(mask, bx0 + i));
        __m512 b1_ps = _mm512_cvtph_ps(_mm256_maskz_loadu_epi16(mask, bx1 + i));
        __m512 b2_ps = _mm512_cvtph_ps(_mm256_maskz_loadu_epi16(mask, bx2 + i));
        __m512 b3_ps = _mm512_cvtph_ps(_mm256_maskz_loadu_epi16(mask, bx3 + i));

        __m512 d0v = _mm512_sub_ps(a_ps, b0_ps);
        __m512 d1v = _mm512_sub_ps(a_ps, b1_ps);
        __m512 d2v = _mm512_sub_ps(a_ps, b2_ps);
        __m512 d3v = _mm512_sub_ps(a_ps, b3_ps);

        acc0 = _mm512_fmadd_ps(d0v, d0v, acc0);
        acc1 = _mm512_fmadd_ps(d1v, d1v, acc1);
        acc2 = _mm512_fmadd_ps(d2v, d2v, acc2);
        acc3 = _mm512_fmadd_ps(d3v, d3v, acc3);
    }

    // 6. 水平归约（16 个 float -> 1 个 float）
    *d0 = _mm512_reduce_add_ps(acc0);
    *d1 = _mm512_reduce_add_ps(acc1);
    *d2 = _mm512_reduce_add_ps(acc2);
    *d3 = _mm512_reduce_add_ps(acc3);
}
// 处理 128 维：128/16 = 8 次迭代
```

#### 性能分析

| 指标          | 单距离计算  | batch距离计算 | 加速比 |
| ------------- | ----------- | ------------- | ------ |
| QPS           | 9890.4710   | 13194.4920    | 1.334  |
| 构建时间 (ms) | 305353.0530 | 268593.9520   | 1.137  |

### 2.5 MinMax Heap的SIMD优化

#### 问题分析

原始堆操作采用纯标量线性扫描：每轮仅处理单个元素，`ids[i] >= 0` 与距离比较形成高频分支，既无法利用 CPU 向量执行宽度，又易引入分支预测与流水线停顿。在不改变堆结构与接口语义的前提下，优化目标是将“逐元素判断”整体提升为“向量批量判断”，以 SIMD 并行与掩码机制消除控制流分支。

#### 优化原理与设计

核心优化思路是：将连续存储的 `(ids, dis)` 视为天然的 SIMD 批处理对象，每次加载 16 个元素，通过向量比较生成掩码表达逻辑条件，再用掩码选择或归约结果。这样既保持原有算法语义，又显著提高吞吐量。

##### 关键操作 1：pop_min（查找并移除最小元素）

在 `pop_min` 中，向量化后的实现维护“当前最小候选”的向量状态：`min_distances` 保存 16 个通道上的最小距离候选，`min_indices` 保存对应的全局下标。扫描时一次加载 16 个 `id` 与 `dis`，通过掩码过滤无效槽位（`id < 0`），并与当前最小距离并行比较。是否“保留旧值”或“更新为新值”完全由掩码控制，使用 `mask_blend` 完成无分支更新。整个扫描结束后，对 `min_distances` 做向量归约得到全局最小距离，再通过等值掩码从 `min_indices` 中恢复对应下标；若存在并列最小值，采用固定的掩码归约规则保证确定性。尾部不足 16 个元素仍使用标量处理，确保语义与原实现一致，最终仅在选中的槽位上执行删除与计数更新。

**标量实现**：

```c
/* 标量版本：逐个比较 */
int hnsw_minimax_heap_pop_min(hnsw_minimax_heap_t* heap, float* vmin_out) {
    if (heap == NULL || heap->nvalid == 0) {
        return -1;
    }
    
    int min_idx = -1;
    float min_val = FLT_MAX;
    
    /* 线性扫描找最小值 */
    for (int i = 0; i < heap->k; i++) {
        if (heap->ids[i] >= 0 && heap->dis[i] < min_val) {
            min_val = heap->dis[i];
            min_idx = i;
        }
    }
    
    if (min_idx < 0) {
        return -1;
    }
    
    *vmin_out = min_val;
    int ret = heap->ids[min_idx];
    heap->ids[min_idx] = -1;  // 标记为已移除
    heap->nvalid--;
    
    return ret;
}
```

**AVX512 实现**：

```c
#ifdef HNSW_HAVE_AVX512

int hnsw_minimax_heap_pop_min(hnsw_minimax_heap_t* heap, float* vmin_out) {
    if (heap == NULL || heap->nvalid == 0) {
        return -1;
    }
    
    int32_t min_idx = -1;
    float min_dis = FLT_MAX;
    
    /* 初始化 SIMD 寄存器 */
    __m512i min_indices = _mm512_set1_epi32(-1);
    __m512 min_distances = _mm512_set1_ps(FLT_MAX);
    __m512i current_indices = _mm512_setr_epi32(
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15);
    __m512i offset = _mm512_set1_epi32(16);
    
    /* 每次处理 16 个元素 */
    const int k16 = (heap->k / 16) * 16;
    for (int iii = 0; iii < k16; iii += 16) {
        /* 加载 16 个 ID 和距离 */
        __m512i indices = _mm512_loadu_si512((const __m512i*)(heap->ids + iii));
        __m512 distances = _mm512_loadu_ps(heap->dis + iii);
        
        /* 创建掩码：过滤无效 ID（-1）*/
        __mmask16 m1mask = _mm512_cmpgt_epi32_mask(_mm512_setzero_si512(), indices);
        
        /* 创建掩码：当前最小值 < 新距离 */
        __mmask16 dmask = _mm512_cmp_ps_mask(min_distances, distances, _CMP_LT_OS);
        
        /* 组合掩码：保留旧值的条件 */
        __mmask16 finalmask = m1mask | dmask;
        
        /* 条件更新：使用掩码选择保留旧值还是更新新值 */
        min_indices = _mm512_mask_blend_epi32(finalmask, current_indices, min_indices);
        min_distances = _mm512_mask_blend_ps(finalmask, distances, min_distances);
        
        /* 更新索引 */
        current_indices = _mm512_add_epi32(current_indices, offset);
    }
    
    /* 归约：从 16 个通道中找到最小值 */
    min_dis = _mm512_reduce_min_ps(min_distances);
    
    /* 找到最小距离对应的索引（如果有多个，选择最右边的）*/
    __mmask16 mindmask = _mm512_cmpeq_ps_mask(min_distances, _mm512_set1_ps(min_dis));
    min_idx = _mm512_mask_reduce_max_epi32(mindmask, min_indices);
    
    /* 处理剩余元素（不足 16 个）*/
    for (int i = k16; i < heap->k; i++) {
        if (heap->ids[i] >= 0 && heap->dis[i] <= min_dis) {
            min_dis = heap->dis[i];
            min_idx = i;
        }
    }
    
    if (min_idx == -1) {
        return -1;
    }
    
    if (vmin_out != NULL) {
        *vmin_out = min_dis;
    }
    
    int ret = heap->ids[min_idx];
    heap->ids[min_idx] = -1;
    heap->nvalid--;
    
    return ret;
}

#endif
```

##### 关键操作 2：count_below（计数小于阈值的元素）

在 `count_below` 中，标量版本中的“有效性判断 + 阈值判断 + 自增”被整体转化为掩码逻辑。每批 16 个元素并行生成“`id >= 0`”与“`dis < thresh`”两个掩码，按位与得到最终命中掩码，再用 `popcnt` 统计命中位数并累加到计数器中，完全消除循环内分支。剩余元素同样通过标量补齐。

**标量实现**：

```c
int hnsw_minimax_heap_count_below(const hnsw_minimax_heap_t* heap, float thresh) {
    if (heap == NULL) {
        return 0;
    }
    
    int count = 0;
    
    /* 逐个检查并计数 */
    for (int i = 0; i < heap->k; i++) {
        if (heap->ids[i] >= 0 && heap->dis[i] < thresh) {
            count++;  // 分支！
        }
    }
    
    return count;
}
```

**AVX512 实现**：

```c
#ifdef HNSW_HAVE_AVX512

int hnsw_minimax_heap_count_below(const hnsw_minimax_heap_t* heap, float thresh) {
    if (heap == NULL) {
        return 0;
    }
    
    int count = 0;
    
    /* 广播阈值到所有通道 */
    __m512 vthresh = _mm512_set1_ps(thresh);
    __m512i vzero = _mm512_setzero_si512();
    
    /* 每次处理 16 个元素 */
    const int k16 = (heap->k / 16) * 16;
    for (int i = 0; i < k16; i += 16) {
        /* 加载 16 个 ID 和距离 */
        __m512i ids = _mm512_loadu_si512((const __m512i*)(heap->ids + i));
        __m512 dis = _mm512_loadu_ps(heap->dis + i);
        
        /* 创建掩码：ID >= 0（有效元素）*/
        __mmask16 valid_mask = _mm512_cmpge_epi32_mask(ids, vzero);
        
        /* 创建掩码：距离 < 阈值 */
        __mmask16 below_mask = _mm512_cmp_ps_mask(dis, vthresh, _CMP_LT_OS);
        
        /* 组合掩码：有效且小于阈值 */
        __mmask16 final_mask = valid_mask & below_mask;
        
        /* 计数设置的位（无分支！）*/
        count += _mm_popcnt_u32(final_mask);
    }
    
    /* 处理剩余元素 */
    for (int i = k16; i < heap->k; i++) {
        if (heap->ids[i] >= 0 && heap->dis[i] < thresh) {
            count++;
        }
    }
    
    return count;
}

#endif
```

### 2.6 查询相关的“上下文”结构优化

#### 问题分析

在 HNSW in-memory 搜索过程中，距离计算处于最核心的性能热点路径。当向量以 `HalfVector`（FP16）形式存储时，受限于当前 x86 CPU 在 AVX-512 指令集下缺乏高效的半精度浮点算术支持，实际的距离计算不可避免地需要在 `float32` 精度下完成，即每次计算前都必须执行 FP16 → FP32 的数据转换。

在现有实现中，如果在每一次 distance 计算时都重复执行查询向量的 `HalfVector → float32` 转换、基于距离类型（L2 / cosine 等）的 `switch` 分支判断，以及为临时 `float` buffer 频繁调用 `palloc`，这些操作将在一次 HNSW 搜索过程中被高频触发（通常成千上万次），从而显著放大指令数量、分支预测失败率以及内存上下文管理和 cache miss 的开销，最终成为限制整体搜索性能的主要 CPU 瓶颈。

#### 缓存查询相关的“上下文”结构优化设计与实现

##### 引入查询上下文结构（`HnswInMemQueryCtx`）

引入 `HnswInMemQueryCtx`，将一次查询过程中**所有与查询绑定且保持不变的状态**集中管理，包括：

- 距离类型与向量维度
- 已确定的距离计算函数指针
- 查询向量的 `HalfVector` 原始表示及其预转换后的 `float32` 表示

通过显式的查询上下文，将查询相关的初始化逻辑与 distance 热路径解耦，避免在距离计算过程中重复解析 `Datum`、重复分支判断以及重复的内存分配。

##### 查询初始化阶段完成 FP16 → FP32 的一次性转换

在查询初始化阶段，将查询向量从 `HalfVector` 预先转换为 `float32` 并缓存于查询上下文中：

- 后续距离计算直接使用 AVX-512 友好的 `float32` 数据参与运算
- 完全消除查询侧在 distance 热路径中的 FP16 → FP32 转换
- 显著减少距离计算内循环中的指令数量和数据转换开销

由于候选向量在搜索过程中不断变化，其转换成本无法消除，但查询向量作为不变量，其转换可以且应当只执行一次。

##### 初始化阶段绑定距离函数指针，消除热路径分支

在查询初始化阶段，根据距离类型一次性绑定具体的距离计算函数：

```
qctx->distanceFunc = HnswInMemDistanceL2Squared;
```

后续 distance 计算过程中直接通过函数指针调用对应实现，避免在热点路径中反复执行 `switch` 判断，从而提高指令执行的直线化程度，降低控制流开销。

##### 使用内联缓冲区优化小维度向量的内存分配

针对常见的小维度查询向量（如 ≤200 维）：

- 在 `HnswInMemQueryCtx` 内部提供内联 `float` 缓冲区
- 小维度向量优先使用内联缓冲，避免动态内存分配
- 仅在维度超过阈值时回退到 `palloc`

**代码实现：**

```c
/* 缓存查询上下文结构 */
typedef struct HnswInMemQueryCtx {
    Datum queryValue;
    HalfVector *q;
    float *qf;                        // 预转换为 float32
    float qf_inline[200];             // 内联缓冲区（避免 palloc）
    HnswInMemDistanceKind kind;       // 距离类型
    int dim;
    HnswInMemDistanceFunc distanceFunc;  // 函数指针（避免 switch）
} HnswInMemQueryCtx;

/* 初始化时确定距离函数 */
void HnswInMemInitQueryCtx(HnswInMemIndex *index, Datum queryValue,
                           HnswSupport *support, HnswInMemQueryCtx *qctx) {
    qctx->kind = HnswInMemGetDistanceKind(support);
    qctx->dim = (int) index->dimensions;
    
    // 绑定函数指针（只做一次）
    switch (qctx->kind) {
        case HNSW_INMEM_DIST_HALFVEC_L2_SQUARED:
            qctx->distanceFunc = HnswInMemDistanceL2Squared;
            break;
        case HNSW_INMEM_DIST_HALFVEC_L2:
            qctx->distanceFunc = HnswInMemDistanceL2;
            break;
        case HNSW_INMEM_DIST_HALFVEC_COSINE:
            qctx->distanceFunc = HnswInMemDistanceCosine;
            break;
    }
    
    // 预转换查询向量为 float32（只做一次）
    qctx->q = DatumGetHalfVector(queryValue);
    if (qctx->dim <= 200)
        qctx->qf = qctx->qf_inline;  // 使用内联缓冲区
    else
        qctx->qf = (float *)palloc(sizeof(float) * qctx->dim);
    
    HalfvecHalfToFloat(qctx->dim, qctx->q->x, qctx->qf);
}

```

- ### 三、AI 驱动的优化

  ### 3.1自动调优工作流

  通过对代码调优的过程进行抽象建模，我们构建了基于大模型的自动化性能优化工作流系统。它通过 Python 编排多个步骤，结合 Codex 和 Kiro 两个 AI Agent，实现"性能分析 → 优化方案生成 → 代码修改 → 测试验证 → 自动决策"的闭环优化流程。

  #### 工作流的设计

  这套系统分为三层：编排层、步骤流水线和外部工具层，分别用来在工作流中共享上下文与控制整个流程怎么跑、在工作流定义“一次改动”的完整生命周期以及工作流中使用的工具和LLM接口。

  ![](figures/自动化工作流.drawio.png)


  ##### 编排层 - `workflow/runner.py`

  编排层负责组织整个工作流的节奏与状态管理，核心入口是 `WorkflowContext` 和 `WorkflowRunner`。它既提供稳定的运行环境，也把各个步骤的执行顺序与条件统一起来，从而让“分析、选择、改写、验证、评估”的流程能够按配置稳定推进。

  **WorkflowContext (工作流上下文)**

  ```python
  @dataclass
  class WorkflowContext:
      repo_root: Path          # 项目根目录
      run_id: str              # 本次运行 ID (如 20240115_143022_r1)
      round_idx: int           # 当前轮次
      logger: RunLogger        # 日志管理器
      state_file: Path         # 状态文件路径
      state: dict              # 持久化状态 (跨轮次保留)
      config: dict             # 完整配置
      workflow_cfg: dict       # [workflow] 配置段
      data: dict               # 步骤间数据传递 (单轮内有效)
  ```

  `WorkflowContext` 是跨步骤共享的“单轮会话”，它把项目根目录、运行轮次、日志器、持久化状态以及配置统一封装，避免步骤之间用零散的参数传递信息。`state` 用于跨轮次保留关键数据，`data` 则用于单轮内的临时传递，二者配合保证可重复执行与可恢复。

  **WorkflowRunner (工作流执行器)**

  `WorkflowRunner` 则是编排层的执行核心。`run()` 驱动主循环，按轮次执行所有启用的步骤；`_build_step_plan()` 负责将 skip/only/resume 等策略编织成可执行计划；`_should_run_step()` 进一步在单步层面判断是否满足运行条件。为了可观测性，`format_steps()` 和 `format_step_plan()` 提供清晰的步骤列表与 dry-run 视图，便于在真正执行前进行确认与审计。

  ##### 步骤层 - `workflow/steps/`

  步骤层提供标准化的执行单元，`Step` 基类约束了统一的接口与配置输入方式。每个步骤通过 `type_name` 进入注册表匹配，由 `run(ctx)` 完成实际工作，确保扩展时只需关注步骤逻辑本身。

  ```python
  class Step:
      type_name: str = ""  # 子类必须定义，用于注册表匹配
      
      def __init__(self, cfg: dict) -> None:
          self.cfg = cfg   # 该 Step 的配置
      
      def run(self, ctx: WorkflowContext) -> None:
          raise NotImplementedError
  ```

  在具体实现上，步骤从“读取性能画像”到“生成改写指令”、再到“执行、验证与评估”，形成一条闭环链路。ProfileAnalyzeStep 解析 `.folded` 结果并产出性能热点；TargetSelectStep 在此基础上筛选 Top-K 目标并去重；ContextCollectStep 借助 ripgrep 生成候选目标的代码上下文；CodexGenerateKiroPromptStep 将上下文与目标整理为可执行的优化提示；KiroApplyAndTestStep 负责应用修改并进行编译或测试验证；BenchmarkStep 汇总性能指标；CodexGitDecideStep 用性能对比决定提交或回滚；CommandStep 则提供灵活的自定义命令扩展。各步骤统一通过 `ctx.data` 传递中间产物，保证流程衔接自然且可追踪。


  | Step                        | type_name                    | 说明                                   |
  | --------------------------- | ---------------------------- | -------------------------------------- |
  | ProfileAnalyzeStep          | `profile_analyze`            | 调用分析脚本解析性能热点               |
  | TargetSelectStep            | `target_select`              | 选择 Top-K 优化目标，避免重复优化      |
  | ContextCollectStep          | `context_collect`            | 用 ripgrep 搜索相关代码，生成上下文 MD |
  | CodexGenerateKiroPromptStep | `codex_generate_kiro_prompt` | Codex 生成优化方案 prompt              |
  | KiroApplyAndTestStep        | `kiro_apply_and_test`        | Kiro 执行修改 + 编译测试 (支持重试)    |
  | BenchmarkStep               | `benchmark`                  | 运行 benchmark，统计 QPS/Recall        |
  | CodexGitDecideStep          | `codex_git_decide`           | 对比性能决定是否提交                   |
  | CommandStep                 | `command`                    | 执行任意 shell 命令                    |

  ##### 工具层 - `workflow/utils.py`

  工具层为编排与步骤提供底座能力，主要集中在配置加载、命令执行、数据解析与上下文采集四类。`load_config()` 负责读取 TOML 配置并统一为运行期结构；`run_cmd()` 与 `run_shell()` 以一致的方式执行命令并记录日志；`run_agent()` 通过 stdin 驱动 AI Agent CLI，支撑自动化的提示与执行；`parse_self_time_table()` 与 `filter_profile_entries()` 将 profile 输出转为可消费的数据结构；`pick_targets()` 负责目标选择与去重策略；`rg_matches()` 与 `collect_context_md()` 完成代码检索与上下文整理。`RunLogger` 贯穿其中，确保每一步的输入、输出和命令执行都可追踪、可回放。


  | 函数                        | 说明                             |
  | --------------------------- | -------------------------------- |
  | `load_config()`             | 加载 TOML 配置文件               |
  | `run_cmd()` / `run_shell()` | 执行命令并记录日志               |
  | `run_agent()`               | 通过 stdin 管道调用 AI Agent CLI |
  | `parse_self_time_table()`   | 解析 profile 输出表格            |
  | `filter_profile_entries()`  | 过滤无效的 profile 条目          |
  | `pick_targets()`            | 选择优化目标 (含去重逻辑)        |
  | `rg_matches()`              | 使用 ripgrep 搜索代码            |
  | `collect_context_md()`      | 生成代码上下文 Markdown          |
  | `RunLogger`                 | 日志管理器类                     |

  #### 测试与验证

  我们以索引构建阶段的优化为例，展示完整的工作流执行过程。该阶段共运行了 5 轮自动优化迭代，以下为各步骤的典型执行记录。

  ##### 步骤一：性能画像 (Profiling)

  系统首先运行 `perf` 工具采集运行时数据，识别 CPU 热点函数。

  - **任务**：定位消耗 CPU 周期最多的函数调用栈。
  - **日志示例**（源自 R1 `04_performance_analysis.md`）：
    ```markdown
    Index热点（cycles）：
    - HnswParallelBuildGraph._omp_fn.0：99.90%（OpenMP 构建主线程）
    - HnswParallelUpdateBidirectionalConnections：40.11%
    - HnswParallelUpdateConnection：19.33%（单向连接更新）
    ```
  - **分析逻辑**：系统识别出 `HnswParallelUpdateConnection` 占用显著，且内部存在冗余的 O(M) 邻居数组扫描，将其锁定为高优先级优化目标。

  ##### 步骤二：制定优化策略 (Strategizing)

  LLM 基于 Profile 结果与源代码上下文，提出具体的代码修改建议。

  - **任务**：提出理论上可行的优化假设。
  - **迭代记录**（源自 `04_optimization_summary.md`）：
    - **R1 (逻辑优化)**：建议在 `HnswParallelUpdateConnection` 中直接读取已维护的计数器，去除冗余遍历。
    - **R2 (内存优化)**：针对 `HnswInMemAllocOnlyAtId`，提出“哨兵位 + 懒初始化”策略，减少 `memset` 写放大。
    - **R3 (批量处理)**：尝试将逐个元素的初始化改为 Phase A 阶段的批量置零 (Bulk Zeroing)。
    - **R4/R5 (算法剪枝)**：针对 `HnswParallelSelectNeighbors`，建议在排序前增加“有序检测”或“无效元素预过滤”，跳过 `qsort`。

  ##### 步骤三：代码执行与测试 (Execution & Testing)

  Agent 根据策略修改 C 代码，并自动处理编译与测试。

  - **任务**：修改源码文件（如 `polardb/external/pgvector/src/hnsw_inmem_parallel.c`），确保编译通过且单元测试 (UT) 成功。
  - **日志证据**：`04_build_iter_*.log` 显示编译过程，若失败 Agent 会自动读取错误日志进行修复，直到通过。

  ##### 步骤四：基准测试 (Benchmarking)

  在真实数据集上运行 Benchmark，采集关键性能指标。

  - **核心指标**：
    1. **Index Build Time**（索引构建时间，当前优化的首要目标）
    2. **QPS**（查询吞吐量）
    3. **Recall**（召回率）
  - **数据示例**（源自 R2 `06_bench_summary.json`）：
    - Build Time: **478.1s** (vs 历史最佳 479.0s，提升 0.2%)
    - QPS: **4650.8** (vs 历史最佳 5028.7，下降 7.5%)
    - Recall: **0.9386** (基本持平)

  ##### 步骤五：归因与决策 (Decision Making)

  系统对比本轮数据与“历史最佳 (History Best)”，决定是 **Commit**（保留优化）还是 **Checkout**（回滚代码）。

  - **决策逻辑示例**（源自 `07_decision.md`）：
    - **R2 决策（拒绝）**：
      > “虽然 build time 小幅改进（-0.9s），但 QPS/Recall 明显劣化。取消全量初始化可能导致邻居选择质量受损。” → **回滚**
    - **R3 决策（拒绝）**：
      > “Index build time 变慢 +10.6s。虽然 QPS 意外提升了 5%，但因违反‘构建时间优先’原则。” → **回滚**
  - **演化建议**：系统会在决策文档末尾给出下一轮建议，如“进行 A/B 测试隔离 QPS 下降原因”或“优化锁粒度”。


  ##### 有效改动汇总

  经过多轮迭代，以下优化被最终采纳并合入代码库：

  |          修改类型           |                           修改概述                           |                         提升效果                         |
  | :-------------------------: | :----------------------------------------------------------: | :------------------------------------------------------: |
  | 延迟计算（Lazy Evaluation） | PostgreSQL 动态哈希表中将 `freelist_idx` 的计算从函数入口推迟到 `HASH_REMOVE` / `HASH_ENTER` 实际需要的位置，避免无关分支的多余计算 |       查询路径减少不必要开销，QPS 提升约 **3.4%**        |
  |       替换哈希表类型        | HNSW 已访问节点表由基于 `ItemPointerData` 的 `tidhash` 替换为基于 `uintptr_t` 的 `pointerhash`，通过打包 `(blkno, offno)` 简化哈希与比较 | 哈希与比较更轻量、内存更紧凑，搜索阶段 QPS 提升约 **2%** |

  **延迟计算优化细节**

  在 PostgreSQL 动态哈希表 `dynahash.c` 的 `hash_search_with_hash_value()` 函数中，`freelist_idx` 的计算原本在函数入口处无条件执行，即使在 `HASH_FIND` 等只读操作中完全不会使用该值。优化后将其推迟到 `HASH_REMOVE` 和 `HASH_ENTER` 分支内部，仅在实际需要时执行：

  ```c
  // 优化前：入口处无条件计算
  uint32 freelist_idx = FREELIST_IDX(hashp, hashvalue);
  
  // 优化后：按需计算
  case HASH_REMOVE:
      uint32 freelist_idx = FREELIST_IDX(hashp, hashvalue);
      // ... 使用 freelist_idx
  ```

  **哈希表类型替换细节**

  HNSW 搜索过程中需要维护已访问节点集合，原实现使用 `tidhash`（基于 `ItemPointerData`），每次哈希和比较都涉及两个 16-bit 字段的独立处理。优化后设计 `pointerhash`，将 `(blkno, offno)` 打包为单个 `uintptr_t`，使哈希计算和相等比较均可通过单条指令完成：

  ```c
  // 打包函数
  static inline uintptr_t pack_tid(BlockNumber blkno, OffsetNumber offno) {
      return ((uintptr_t)blkno << 16) | offno;
  }
  
  // 哈希函数简化为
  static uint32 pointer_hash(const void *key, Size keysize) {
      return murmurhash32((uint32)(uintptr_t)key);
  }
  ```

  #### 总结

  自动调优工作流的核心价值不仅在于发现有效优化，更在于**快速排除无效方向**，避免人工试错的时间浪费。

  ##### 自动探索并排除的无效优化方向

  在本项目中，工作流自动探索了多个看似合理但实际无效的优化假设，并通过基准测试快速否决：

  | 优化尝试 | 优化假设 | 失败原因 | 自动决策 |
  | :------: | :------- | :------- | :------: |
  | R2 内存优化 | "哨兵位 + 懒初始化"减少 `memset` 写放大 | Build time 仅改进 0.2%，但 QPS 下降 7.5%——取消全量初始化导致邻居选择质量受损 | **回滚** |
  | R3 批量处理 | 将逐元素初始化改为批量置零 (Bulk Zeroing) | Build time 反而变慢 +10.6s，虽然 QPS 意外提升 5%，但违反"构建时间优先"原则 | **回滚** |
  | R4/R5 算法剪枝 | 在 `qsort` 前增加"有序检测"或"无效元素预过滤" | 额外检测开销抵消了跳过排序的收益，整体性能无提升 | **回滚** |

  ##### 为何这些优化未能提升性能

  1. **局部优化与全局指标的矛盾**：R2 在内存写入层面确有改进，但破坏了数据结构的初始化完整性，导致下游邻居选择算法质量下降，最终 QPS 劣化。

  2. **优化目标的优先级冲突**：R3 虽然意外提升了 QPS，但本阶段的首要目标是缩短索引构建时间，因此仍被判定为失败。

  3. **优化收益被额外开销抵消**：R4/R5 的剪枝逻辑本身引入了分支判断和预扫描成本，在实际数据分布下无法覆盖其开销。

  4. **AI 倾向于单点优化，缺乏结构性视角**：当前 LLM 在生成优化方案时，倾向于针对单个热点函数提出局部改动（如替换数据结构、调整分支顺序），而难以识别需要跨模块协作的结构性优化机会（如整体内存布局重构、算法流程重组）。

  ##### 节约的时间成本

  工作流的自动决策机制避免了人工在无效方向上的反复调试，使我们能够将精力集中于真正有价值的优化路径。

  ### 3.2 Perf自动根因分析工作流

  为了改进自动优化工作流中仅依据 perf 结果选取热点函数所带来的局限性，我们设计并引入了两种基于 perf 的自动化根因分析工作流：**perf-workflow** 与 **perf-mem-asm-top**。其中，perf-workflow 用于执行通用的 perf 热点分析流程，以定位整体性能瓶颈；perf-mem-asm-top 则聚焦于内存访问相关的热点指令分析，从指令级层面辅助识别潜在的性能根因。

  | 工具名称 | perf-mem-asm-top                               | perf-workflow                               |
  | -------- | ---------------------------------------------- | ------------------------------------------- |
  | 工具定位 | 内存访问热点指令分析工具                       | 通用 perf 热点分析工作流                    |
  | 核心目标 | 找出最耗时的 load/store 指令及其对应的数据结构 | 从 perf profile 到源码/汇编的端到端热点分析 |
  | 分析粒度 | 指令级（load / store）                         | 符号级 / 行级 / 汇编级                      |
  | 适用场景 | 内存瓶颈定位、cache miss / pagefault 归因      | 全面热点分析、优化前后性能对比              |

  #### perf-workflow工作流

  该工作流适用于需要进行完整 perf 热点分析、对比优化前后性能差异，或将汇编级热点准确映射回源码以进行根因定位的场景。

  **核心功能**

  该工作流提供端到端的 perf profile 分析能力，覆盖从热点符号统计到源码与汇编级映射的完整流程。针对高优化级别（如 O3）下符号与源码映射不准确的问题，优先采用 `-l` 选项进行行级分析，以规避内联与指令重排带来的偏差。同时支持新旧 perf profile 的对比分析，用于评估优化前后的性能变化。

  **工作流程**

  ```
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ Step 0: 定位输入  │ -> │ Step 1: 热点汇总  │ -> │ Step 2: 符号注解  │
  │ perf.data + 二进制│    │ perf report      │    │ perf annotate -l │
  └──────────────────┘    └──────────────────┘    └──────────────────┘
                                                          │
                                                          v
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ Step 5: 生成报告  │ <- │ Step 4: 源码定位  │ <- │ Step 3: 对比分析  │
  │ 汇总分析结果      │    │ rg + nl 映射     │    │ (可选) 新旧对比   │
  └──────────────────┘    └──────────────────┘    └──────────────────┘
  ```

  ##### Step 0: 定位输入文件

  默认使用 `test/profile_output/` 目录下的 perf 数据：
  - `index_latest_profile_perf`（索引构建阶段）
  - `query_latest_profile_perf`（查询阶段）

  若符号缺失或源码路径错误，需配置 `--symfs`、`--buildid-dir` 或使用 `perf buildid-cache --add` 补充调试信息。

  ##### Step 1: 热点符号汇总

  运行非交互式报告，获取 Top 热点符号及调用链：

  ```bash
  perf report -i path/to/perf.data --stdio --no-children
  ```

  输出示例：
  ```
  # Overhead  Command   Shared Object        Symbol
  # ........  ........  ...................  ..............................
      18.32%  postgres  vector.so            [.] HnswInMemSearchLayer
      12.15%  postgres  postgres             [.] LWLockAcquire
       9.87%  postgres  vector.so            [.] HalfvecL2SquaredDistanceBatch4
  ```

  ##### Step 2: 行级注解分析

  针对关键符号，使用 `-l` 选项获取行级源码映射（规避 O3 内联导致的 `-s` 偏差）：

  ```bash
  perf annotate -i path/to/perf.data --stdio -l --symbol HnswInMemSearchLayer --percent-limit 1
  ```

  输出将显示每条汇编指令对应的源码行号及其 CPU 周期占比。

  ##### Step 3: 对比分析（可选）

  若需评估优化前后变化，对同一符号分别运行 annotate 并对比：
  - 哪些源码行/基本块的占比增减
  - 热点是否转移到不同的内联路径
  - 汇编中的内存访问模式（load/store）是否变化

  ##### Step 4: 源码精确定位

  结合 `rg` 与 `nl` 定位热点源码：

  ```bash
  # 搜索符号定义
  rg -n "HnswInMemSearchLayer" -S .
  
  # 显示指定行范围
  nl -ba src/hnsw_search.c | sed -n '240,280p'
  ```

  ##### Step 5: 生成分析报告

  汇总每个热点的以下信息：

  | 字段 | 说明 |
  |------|------|
  | 符号 + 占比 | 来自 `perf report` 的 no-children 百分比 |
  | 源码位置 | 来自 `perf annotate -l` 的 file:line |
  | 关键语句 | 造成开销的具体代码行 |
  | 数据访问 | 涉及的数组、结构体、指针追踪模式 |
  | 锁/自旋 | 汇编中观察到的锁竞争或自旋等待行为 |

  #### perf-mem-asm-top工作流

  该工作流适用于需要回答"哪些内存访问指令构成主要性能瓶颈"以及"哪些数据结构导致了缓存未命中或缺页中断"等问题的性能分析场景，尤其适合用于深入诊断内存层级相关的性能根因。

  **核心功能**

  该工作流面向内存访问瓶颈分析，从 perf 数据中系统性地提取负载（load）与存储（store）指令，并基于加权周期开销进行排序，其中权重由指令在符号内的本地占比与符号在整体 profile 中的 no-children 百分比共同确定。同时，工作流支持对 page fault（缺页中断）事件进行归因分析，并将内存访问热点指令进一步映射回源码层面的具体数据结构，以辅助定位内存层级相关的性能问题。

  **工作流程**

  ```
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ Step 1: 定位数据  │ -> │ Step 2: 符号开销  │ -> │ Step 3: 指令排序  │
  │ perf.data        │    │ perf report      │    │ perf_mem_top.py  │
  └──────────────────┘    └──────────────────┘    └──────────────────┘
                                                          │
                                                          v
                          ┌──────────────────┐    ┌──────────────────┐
                          │ Step 5: 生成报告  │ <- │ Step 4: 源码映射  │
                          │ 加权开销 + 归因   │    │ rg + nl 定位     │
                          └──────────────────┘    └──────────────────┘
  ```

  ##### Step 1: 定位 perf 数据

  默认使用以下路径：
  - `test/profile_output/query_latest_profile_perf`
  - `test/profile_output/index_latest_profile_perf`

  ##### Step 2: 获取符号级开销

  使用 `--no-children` 避免重复计算：

  ```bash
  perf report -i path/to/perf.data --stdio --group --no-children
  ```

  ##### Step 3: 内存指令加权排序

  运行配套 Python 脚本，自动提取并排序内存访问指令：

  ```bash
  # 自动选取 Top 5 热点符号，输出 Top 20 内存指令
  python3 scripts/perf_mem_top.py -i path/to/perf.data --auto-top 5 --topn 20
  
  # 或指定符号进行分析
  python3 scripts/perf_mem_top.py -i path/to/perf.data \
      --symbols hnsw_search_with_context HalfvecL2SquaredDistanceBatch4Avx512f
  ```

  脚本内部执行：
  1. 对每个符号运行 `perf annotate -l`
  2. 提取 load/store 指令
  3. 计算加权开销：`weighted_pct = local_pct × symbol_no_children_pct`
  4. 标注 page fault 触发指令

  ##### Step 4: 源码与数据结构映射

  根据脚本输出的源码行号，定位具体数据结构：

  ```bash
  # 搜索符号
  rg -n "neighbors" -S src/
  
  # 查看热点行上下文
  nl -ba src/hnsw_inmem.c | sed -n '1900,1920p'
  ```

  利用 `perf annotate` 输出中的内联注释（如 `// hnsw_inmem.c:1901`）直接跳转。

  ##### Step 5: 生成分析报告

  每条热点指令汇总以下信息：

  | 字段 | 说明 |
  |------|------|
  | 加权开销 | `local_pct × symbol_pct`，反映全局影响 |
  | 本地占比 | 指令在符号内的占比 |
  | 符号名称 | 所属函数 |
  | 源码位置 | file:line |
  | 数据结构 | 访问的数组/结构体/指针链 |
  | Page Fault | minor/major fault 归因（如有） |

  **输出示例**：

  ```
  Rank  Weighted%  Local%  Symbol                           Source Location           Data Structure
  ----  ---------  ------  -------------------------------  ------------------------  ----------------
  1     8.72%      47.6%   HnswInMemSearchLayer             hnsw_inmem.c:1901         neighbors[]
  2     5.31%      29.0%   HalfvecL2SquaredDistanceBatch4   halfvec_ops.c:312         vecstore->vectors
  3     3.14%      25.8%   LWLockAcquire                    lwlock.c:891              HTAB->entries
  ```

  #### 测试与验证

  以某次查询阶段的性能分析为例，展示两套工作流的协作效果：

  **perf-workflow 分析结果**

  | 符号 | 占比 | 热点行 | 根因判断 |
  |------|------|--------|----------|
  | `HnswInMemSearchLayer` | 18.3% | L245: 邻居遍历循环 | 随机访问 neighbors[] 导致 cache miss |
  | `LWLockAcquire` | 12.1% | L89: 自旋等待 | 锁粒度过大，高并发下竞争严重 |

  **perf-mem-asm-top 分析结果**

  | 加权开销 | 指令类型 | 源码位置 | 数据结构 |
  |----------|----------|----------|----------|
  | 8.7% | vmovups (load) | hnsw_inmem.c:312 | neighbors[] |
  | 5.2% | mov (load) | dynahash.c:891 | HTAB->entries |
  | 2.1% | vmovaps (load) | halfvec_ops.c:156 | vecstore->vectors |

  基于上述分析，识别出 `neighbors[]` 的随机访问是查询阶段的主要内存瓶颈，后续通过数据布局优化和预取策略实现了显著的性能提升。

  #### 总结

  两套 perf 分析工作流形成互补的分析体系：

  | 维度 | perf-workflow | perf-mem-asm-top |
  |------|---------------|------------------|
  | 分析视角 | 宏观 → 微观（符号 → 行 → 汇编） | 微观聚焦（指令级内存访问） |
  | 核心产出 | 热点函数及其源码定位 | 热点 load/store 指令及数据结构 |
  | 典型问题 | "哪个函数最慢？" | "哪条指令触发了 cache miss？" |
  | 适用阶段 | 优化初期，确定方向 | 优化深入，验证假设 |

  二者结合可有效缩短"发现问题 → 定位根因 → 验证假设"的分析周期，为后续的针对性优化提供数据支撑。

  ### 3.3 基于规整约束的Faiss HNSW转译工作流

  为了高效的实现Faiss HNSW算法的迁移，我们设计实现了**以规则驱动、AI 辅助生成、验证与性能闭环为核心的 HNSW 代码迁移流程**。其特点在于通过规则约束、自动化生成、系统验证与性能对齐分析相结合，确保跨语言迁移过程中功能等价性与性能一致性。

  首先，通过明确的迁移规则与编码规范，对 C/C++ 之间的差异进行系统性约束，包括公共类型与数据结构定义、错误码与枚举设计、距离函数指针类型以及对外 API 接口声明。在此基础上，借助 AI Agent（Kiro IDE, codex）自动生成对应的 HNSW C 代码实现。生成代码随后经历功能正确性验证与关键路径性能对齐两个关键步骤，以确保算法行为与原始 C++ 实现保持一致，同时避免因语言特性变化引入性能退化。此外，该阶段还通过系统化的测试与验证流程，对数据结构一致性、功能正确性以及整体性能进行评估，并结合 perf 等性能分析工具，对新旧实现进行对比分析，以定位并修正潜在的性能差异来源。

 ![](figures/移植工作流.drawio.png)

  #### 基于规则的迁移

  C++ 到 C 的迁移涉及语言特性、内存管理模式和编程范式的根本性差异。为确保迁移的一致性和可维护性，我们制定了系统性的转换规则。

  ##### 核心转换规则

  | C++ 特性 | C 替代方案 | 示例 |
  |----------|-----------|------|
  | `std::vector<T>` | 原生指针 + `size` + `capacity` 三元组 | `neighbors` → `neighbors` + `neighbors_size` + `neighbors_capacity` |
  | `std::priority_queue` | 手动实现的堆结构 `farther_heap_t` | 参见 2.5 节 MinimaxHeap 的 SIMD 优化 |
  | 成员函数 | 独立函数，首参为 `hnsw_t*` | `HNSW::neighbor_range()` → `hnsw_neighbor_range(hnsw, ...)` |
  | 虚函数/多态 | 函数指针回调 | `DistanceComputer` → `hnsw_distance_func_t` |
  | 构造/析构函数 | `hnsw_new()` / `hnsw_free()` 显式调用 | RAII → 手动生命周期管理 |
  | 异常处理 | 错误码 + `ereport()` | `throw` → `return NULL` + 错误码 |
  | 线程局部存储 | `HNSW_THREAD_LOCAL` 暂存区 | 避免频繁 `malloc/free` |

  ##### 数据结构对照

  ```
  C++ HNSW 类                              C hnsw_t 结构体
  ─────────────────────────────────────────────────────────────────
  std::vector<storage_idx_t> neighbors  →  hnsw_storage_idx_t* neighbors
                                           size_t neighbors_size
                                           size_t neighbors_capacity
  
  std::vector<size_t> offsets           →  size_t* offsets + size + capacity
  
  virtual DistanceComputer              →  hnsw_distance_func_t distance_func
                                           void* distance_user_data
  ```

  ##### 内存管理策略

  | 策略 | 说明 |
  |------|------|
  | **显式生命周期** | `hnsw_new()` 分配，`hnsw_free()` 释放，调用方负责配对 |
  | **线程局部暂存区** | `hnsw_build_scratch` 复用临时缓冲区，2 倍增长策略 |
  | **PostgreSQL 集成** | 生产环境使用 `palloc/pfree` 替代 `malloc/free` |

  #### AI 辅助生成

  在规则约束的基础上，利用 AI Agent 加速代码生成。生成流程如下：

  **规则注入 Prompt 示例：**

  ```text
  ## 转译规则
  1. idx_t → hnsw_storage_idx_t
  2. std::vector<T> → 预分配数组 + count 字段
  3. 禁止 new/delete，使用 malloc/free
  4. 禁止异常，使用错误码 + ereport()
  5. 成员函数 → 独立函数，首参为 hnsw_t*
  
  ## 源代码
  [Faiss HNSW::search_from_candidates 函数]
  
  ## 任务
  按照上述规则，将源代码转译为 PostgreSQL 兼容的 C 实现。保持算法逻辑不变，确保内存安全。
  ```

  #### 测试与验证

  ##### 功能正确性验证

  为确保转译实现与 Faiss 原始实现的行为完全一致，我们采用**单线程确定性对比**的验证方法，分为索引构建和查询两个阶段进行验证。

  **验证前提：**
  - 使用单线程执行，排除并发导致的不确定性
  - 为 Faiss 实现和 C 移植实现设定**相同的随机数种子**，确保层级分配、入口点选择等随机行为一致

  **阶段一：索引构建验证**

  | 验证项 | 验证方法 | 通过标准 |
  |--------|----------|----------|
  | 邻居表结构一致 | 逐节点对比 `neighbors[]` 数组内容 | 每个节点的邻居集合完全相同 |
  | 层级分配一致 | 对比 `levels[]` 数组 | 每个节点的层级值相同 |
  | 偏移表一致 | 对比 `offsets[]` 数组 | 偏移量完全匹配 |
  | 入口点一致 | 对比 `entry_point` 和 `max_level` | 值相同 |

  **阶段二：查询验证**

  | 验证项 | 验证方法 | 通过标准 |
  |--------|----------|----------|
  | 查询路径一致 | 记录搜索过程中访问的节点序列 | 两套实现的访问顺序完全相同 |
  | 候选集演化一致 | 对比每一步的候选堆状态 | 堆内容和顺序一致 |
  | 最终结果一致 | 对比 Top-K 返回的 ID 和距离 | ID 序列相同，距离误差 < 1e-6 |

  通过上述两阶段验证，可确保转译实现在算法行为上与 Faiss 原始实现**完全等价**，而非仅仅"结果近似"。

  ##### 性能对齐分析

  性能对齐分析同样分为索引构建和查询两个阶段，通过 perf 采集两套实现的函数级时间占比，识别差异函数并借助 AI 进行针对性优化。分别对 Faiss 和 C 移植实现运行相同规模的任务，采集各函数的时间占比：

  **差异函数的 AI 辅助分析流程**
  ```
  1. 提取差异函数的 perf annotate 输出（含汇编热点）
  2. 将 Faiss 源码与 C 移植源码一并提供给 AI
  3. AI 对比分析，识别可能的性能差异来源：
     - 循环结构差异
     - 内存访问模式差异
     - 分支预测友好性差异
     - SIMD 向量化程度差异
  4. AI 生成优化建议或直接修改代码
  5. 重新运行 perf 验证差异是否收敛
  ```
  总结,这一步骤主要是进行函数流程上的对齐, 部分数据结构比如优先队列还需进一步的优化. 

  ##### MinimaxHeap 高性能实现

  尽管基于规则与 AI 的转译工作流解决了大部分业务逻辑的迁移，但在性能敏感的数据结构上，自动生成的代码仍难以匹敌经过高度优化的 C++ STL 组件。特别是 HNSW 搜索核心路径中频繁使用的优先队列（`std::priority_queue`），是自动对齐的“盲区”。

  为了突破这一瓶颈，我们针对该热点数据结构采取了**手动深度定制**策略。不同于 STL 的通用实现，我们设计了专用的 `MinimaxHeap`，通过内存布局优化（SoA）与特定场景的剪枝逻辑，实现了较好的性能：

  ```c
  typedef struct hnsw_minimax_heap_t {
      int n;
      int k;
      int nvalid;
      hnsw_storage_idx_t* ids;
      float* dis;
  } hnsw_minimax_heap_t;
  ```

  **关键设计:**
  - **数据布局优化**：采用 `ids` 和 `dis` 分离的并行数组（Structure of Arrays, SoA），相比 Array of Structures (AoS) 布局，不仅内存更为紧凑，且在进行批量距离比较时具有更好的缓存局部性，更利于 SIMD 向量化加载。
  - **标记删除策略**：`pop_min` 操作仅通过将 ID 标记为 -1 实现逻辑删除，避免了传统堆删除操作中频繁的元素交换与堆重建开销。
  - **剪枝优化**：始终维护 `dis[0]` 为当前堆中的最大距离值，在插入新元素时可快速判断是否需要丢弃，从而避免无效的堆调整操作。

  

  **设计权衡与性能考量:**
  1. **线性扫描 vs 堆结构**：在 HNSW 搜索场景下，`efSearch` 通常较小（如 16-128）。在此规模下，基于数组的线性扫描（Linear Scan）配合 SIMD 指令，其性能往往优于维护复杂的二叉堆结构，因为前者避免了大量的分支预测失败和随机内存访问。
  2. **SIMD 并行度**：扁平化的数组结构极度适配 AVX-512 指令集，允许单次指令并行比较 16 个距离值（参见 2.5 节 MinimaxHeap 的 SIMD 优化），吞吐量远超标量实现的树状堆。
  3. **缓存友好性**：顺序存储的数组最大程度利用了 CPU 预取机制（Prefetcher），显著降低了 L1/L2 Cache Miss 率。
  4. **低常数项开销**：相比通用容器，定制化实现去除了所有虚函数调用、内存分配检查等隐式开销，将指令数压缩至极限。

  ##### 转译成果

  **Recall 对比 (deep1b, 1M):**
  | efSearch | C++ Recall | C API Recall | 差异 |
  |----------|------------|--------------|------|
  | 16 | 0.6201 | 0.6241 | +0.65% |
  | 32 | 0.7781 | 0.7805 | +0.31% |
  | 64 | 0.8894 | 0.8898 | +0.04% |
  | 128 | 0.9479 | 0.9471 | -0.08% |
  | 256 | 0.9738 | 0.9741 | +0.03% |

  **QPS 对比:**
  | efSearch | C++ QPS | C API QPS | C API / C++ |
  |----------|---------|-----------|-------------|
  | 16 | 86,454 | 61,925 | 71.6% |
  | 32 | 59,014 | 47,954 | 81.3% |
  | 64 | 38,212 | 32,033 | 83.8% |
  | 128 | 22,888 | 19,099 | 83.4% |
  | 256 | 13,134 | 11,245 | 85.6% |

  **结论:** C API 在保持召回率一致的前提下，QPS 约为 C++ 的 83%。

  #### 移植工作量统计

  | 类别 | 代码行数 (约) |
  |------|--------------|
  | 数据结构 | 500 |
  | 内存管理 | 300 |
  | 核心算法 | 800 |
  | SIMD 优化 | 400 |
  | 并行支持 | 500 |
  | 错误处理 | 100 |
  | **总计** | **~2600** |

  **未移植功能:**
  - Panorama 搜索
  - IDSelector 过滤
  - SearchParameters 动态参数

## 存在的问题与改进方向
1.容量与内存浪费（“一刀切预分配”）

- 全局 vecstore 固定容量：max_vectors * dim * sizeof(half) 启动一次性吃满，数据量小也占用巨大内存；超过容量直接失败，无法在线扩容。

2、崩溃一致性与持久化（“绕开了 PG 的 WAL/Checkpoint 体系”）

- 内存池可以是 file-backed 并复用，但写入没有 WAL 语义：崩溃时可能出现“部分写入的图结构/vecstore”。

