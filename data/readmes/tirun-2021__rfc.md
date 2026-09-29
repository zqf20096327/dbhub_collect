# Spatial TiDB

_By 钛润(TiRun) Team: [@Triple-Z](https://github.com/Triple-Z), [@arcosx](https://github.com/arcosx), [@top628LJ](https://github.com/top628LJ)_

## 项目介绍

<!-- 一段简单的介绍即可，帮助文档阅读者了解设计文档的简要信息。-->

我们将为 TiDB 提供空间数据的功能，客户能够在 TiDB 中管理、存储空间数据，并且能够直接在数据库中完成对空间数据的计算任务。
我们提供的空间数据功能具有以下特性：

- POINT 地理位置
- 通用计算函数 (Equals, Distance etc.)

我们将基于已实现功能演示空间数据位于数据库上的计算能力，展示出 TiDB 支持空间数据后的强大潜能。


## 背景&动机

<!--这个设计文件的背景和所要解决的问题是什么？它支持哪些用例？

这部分不需要太多细节，但必须写明项目的动机或背景。写清楚项目的需求从何而来、项目本身解决了什么问题。-->

### 竞对比较 

PostgreSQL 有如 PostGIS 的空间数据扩展，MySQL 则内部支持空间数据的存储和计算。

- [PostGIS](https://postgis.net/)
- [MySQL 8.0 Reference Manual :: 11.4 Spatial Data Types](https://dev.mysql.com/doc/refman/8.0/en/spatial-types.html) 
- [MySQL 8.0 Reference Manual :: 12.17 Spatial Analysis Functions](https://dev.mysql.com/doc/refman/8.0/en/spatial-analysis-functions.html) 

### 用户需求

在 TiDB 的 GitHub 以及论坛 AskTUG 中，有不少用户声援空间数据计算的功能：
- [Support for SPATIAL functions, data types and indexes · Issue #6347 · pingcap/tidb · GitHub](https://github.com/pingcap/tidb/issues/6347)
- [Does tidb support Spatial database? · Issue #673 · pingcap/tidb · GitHub](https://github.com/pingcap/tidb/issues/673)
- https://github.com/pingcap/tidb/issues/18290
- [希望支持经纬度函数- 产品需求- AskTUG](https://asktug.com/t/topic/35682)


### 典型应用场景

LBS 服务，社交、地理轨迹显示计算等。


## 项目设计

<!--这一部分可以对设计进行详细的解释；合理清楚地说明该功能将如何实现，通过实例剖析案例，如何使用功能等。

这部分可以描述关键算法的伪代码，API 接口，UML 图等，以及还会修改哪些组建。-->

### 空间数据结构

- POINT
- GEOMETRY

### 空间计算函数

- Point(): Construct Point from coordinates
- ST_X(): Return X coordinate of Point
- ST_Y(): Return Y coordinate of Point
- ST_Equals(): Whether one geometry is equal to another
- ST_Distance(): The distance of one geometry from another
- ST_PointFromText(): Construct Point from WKT
- ST_PointFromWKB(): Construct Point from WKB
