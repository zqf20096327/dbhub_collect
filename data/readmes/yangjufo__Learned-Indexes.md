# Learned Indexes
Implementation of BTree part for paper 'The Case for Learned Index Structures'.  

T. Kraska, A. Beutel, E. H. Chi, J. Dean, and N. Polyzotis. The Case for Learned
Index Structures. https://arxiv.org/abs/1712.01208, 2017
>Language: Python  
Support content: Integer values, Random and Exponential distribution

## Files Structures
> data/: test data  
model/: learned NN model  
perfromance/：NN and BTree performance  
Learned_BTree.py: main file  
Trained_NN.py: NN structures

## HOW TO RUN
> First, you need to install python2.7.x and package tensorflow, pandas, numpy, enum.   
Second, use command to run the Learned_BTree.py fule, that is,  
```python Learned_BTree.py -t <Type> -d <Distribution> [-p|-n] [Percent]|[Number] [-c] [New data] [-h]```.  
  
>Parameters:  
'type': 'Type: sample, full',  
'distribution': 'Distribution: random, exponential',  
'percent': 'Percent: 0.1-1.0, default value = 0.5; sample train data size = 300,000',  
'number': 'Number: 10,000-10,000,000, default value = 300,000',  
'new data' 'New Data: INTEGER, 0 for no creating new data file, others for creating'  
  
>Example:  
```python Learned_BTree.py -t full -d random -n 100000 -c 1```  
  

## Other Content
### Sample Training
> Sample training is also included in this project, you can use parameter 'sample' for '-t' to test sample training, while '-p' is used for change the sample training percent.  
  
>Example:  
```python Learned_BTree.py -t sample -d random -p 0.3 -c 0```
### Storage Optimization
>More Information will be added soon.


***
# **中文**
本项目代码是对《The Case For Learned Index Structures》一文的简单实现，实现了文章中BTree的部分，目前支持整数测试集，可以选用随机分布或者指数分布进行测试。  

T. Kraska, A. Beutel, E. H. Chi, J. Dean, and N. Polyzotis. The Case for Learned
Index Structures. https://arxiv.org/abs/1712.01208, 2017  

此外，项目还对有新数据插入的场景进行了探索。

## 数据索引
### 主要步骤

1. 依据论文中思想，搭建混合多级神经网络架构
![Stage Models](https://github.com/yangjufo/Learned-Indexes/blob/master/about/models.PNG)
``` 
 Input: int threshold, int stages[]
 Data: record data[]
 Result: trained index
1 M = stages.size;
2 tmp_records[][];
3 tmp_records[1][1] = all_data;
4 for i ← 1 to M do
5   for j ← 1 to stages[i] do
6     index[i][j] = new NN trained on tmp.records[i][j];
7     if i < M then
8       for r ∈ tmp.records[i][j] do
9         𝑞 = f(r.key) / stages[i + 1];
10        tmp.records[i + 1][ 𝑞].add(r);
11 for j ← 1 to index[M].size do
12   index[M][j].calc_err(tmp.records[M][j]);
13   if index[M][j].max_abs_err > threshold then
14     index[M][j] = new B-Tree trained on tmp_records[M][j];
15 return index;
```
> 在以上程序中，从整个数据集开始（第3行）开始，首先训练第1级模型。基于第1级模型的预测，从下一级挑选模型，并添加相应的关键字到该模型训练集（第9行和第10行），然后训练这个模型。最后，检查最后一级的模型，如果平均误差高于预定义的阈值，则用B树替换神经网络模型（第11-14行）。
*所使用的模型均为全连接网络，随机分布用的是没有隐藏的全连接网络；指数分布用的是有1个有8个核的隐藏层的全连接网络*

2. 使用数据测试神经网络索引和B树索引，对比两者性能
***
## 抽样学习
> 神经网络模型的训练需要较长的时间，通过抽取一部分数据训练的方式，加快训练的速度。
*** 
## 存储优化
> 基于后续插入数据的分布与现有分布相近的观点。
### 主要步骤
1. 根据建立的数据索引估计数据分布，并移动数据的位置，预留出空间。比如原先0-100的数据占据100个BLOCK，预计最终存储数据是现在的2倍，则预留100个BLOCK。

2. 插入数据，与不进行优化比较。

### 优势
1. 新插入数据冲突少，加快插入速度。
2. 无需重新调整索引，降低索引维护代价，支持了新数据插入场景。

