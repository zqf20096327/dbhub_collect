src\common\cm_utils\cm_memory.h
+#elif defined(__riscv)
+#define RISCV_FENCE(p, s) \
+        __asm__ __volatile__ ("fence " #p "," #s : : : "memory")
+#define CM_MFENCE RISCV_FENCE(iorw,iorw)
+#else
\src\common\cm_concurrency\cm_spinlock.h
#if defined(__arm__) || defined(__aarch64__) || defined(__riscv)
#define fas_cpu_pause()          \
    {                            \
        __asm__ volatile("nop"); \
    }
#else
#define fas_cpu_pause()            \
    {                              \
        __asm__ volatile("pause"); \
    }
#endif


