> perf stat -e cycles,instructions,LLC-loads,LLC-load-misses,L1-dcache-loads,L1-dcache-load-misses,branches,branch-misses ./vec-test 
  
   Performance counter stats for './vec-test':
  
         282,408,889      cycles                                                        (37.81%)
       1,049,717,271      instructions              #    3.72  insn per cycle           (48.15%)
              78,323      LLC-loads                                                     (51.92%)
              37,653      LLC-load-misses           #   48.07% of all LL-cache hits     (52.73%)
         174,299,857      L1-dcache-loads                                               (41.52%)
           5,657,226      L1-dcache-load-misses     #    3.25% of all L1-dcache hits    (39.71%)
         234,069,674      branches                                                      (38.66%)
             213,634      branch-misses             #    0.09% of all branches          (37.75%)
  
         0.115359537 seconds time elapsed
       
       
> perf stat -e cycles,instructions,LLC-loads,LLC-load-misses,L1-dcache-loads,L1-dcache-load-misses,branches,branch-misses ./row-test 
  
   Performance counter stats for './row-test':
  
       1,543,323,919      cycles                                                        (39.99%)
       4,738,255,720      instructions              #    3.07  insn per cycle           (50.01%)
             143,498      LLC-loads                                                     (50.23%)
              33,718      LLC-load-misses           #   23.50% of all LL-cache hits     (50.09%)
       1,925,088,653      L1-dcache-loads                                               (39.73%)
             646,877      L1-dcache-load-misses     #    0.03% of all L1-dcache hits    (39.85%)
         800,372,109      branches                                                      (39.86%)
             133,731      branch-misses             #    0.02% of all branches          (39.84%)
  
         0.552686237 seconds time elapsed
       

从上面的对比可以看出：
1. 向量化执行更快: 耗时是非向量化的 1/5 左右；
2. 向量化执行用更少的指令完成了相同的工作: 因为降低了解释开销，减少了"无意义"的指令数量；
3. 向量化执行对内存更加友好: 因为大多数时候是在集中的访问连续内存，所以能更好的命中 CPU Cache；
4. 向量化执行分支预测的成功率也更高；




