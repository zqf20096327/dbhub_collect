# Java 面试题问答

## String、StringBuilder 和 StringBuffer 的区别：

1. String 是不可变对象，内部用 final 修饰的数组存储字符（JDK9 之后是 byte 数组），任何看似修改的操作都会生成新对象，在循环里用 + 拼接 String 会产生大量临时对象，性能很差。
2. StringBuilder 是可变对象，内部是可变数组，append 直接修改自身不会创建新对象，方法全程不加锁，单线程下字符串拼接性能最高，是拼接场景的首选。
3. StringBuffer 功能和 StringBuilder 完全一样，但方法内部都加了 synchronized，线程安全，代价是性能略低，只适合多个线程共享同一个缓冲区对象的场景。
4. 一个常见坑：变量之间的 + 拼接，编译器每次都会 new 一个 StringBuilder，编译器不会跨语句优化，所以循环里 s = s + x 这种写法必须手动换成 StringBuilder。
5. 选择上：内容固定或只拼一两次用 String，单线程循环拼接用 StringBuilder，多线程共享同一个缓冲区才用 StringBuffer。

## String str = new String("abc") 创建了几个对象：

1. 如果常量池中已经有 abc，只在堆上 new 出 1 个 String 对象。
2. 如果常量池中没有 abc，先在常量池创建 1 个，再在堆上创建 1 个，共 2 个，所以最少 1 个、最多 2 个。

## Java 中接口和抽象类的区别及选择：

1. 关系语义不同：抽象类表达 is-a 关系，说明本质上是同一类事物，比如狗是动物；接口表达 can-do 关系，表示某种能力，比如可飞行、可序列化。
2. 成员构成不同：抽象类可以有构造方法、实例变量、普通方法和静态代码块；接口里的变量默认都是 public static final 常量，JDK8 之前只能有抽象方法。
3. 演进上：JDK8 给接口加了 default 方法和静态方法，JDK9 又支持私有方法，接口也能有方法实现了，但始终不能有实例变量和构造方法。
4. 继承体系不同：一个类只能继承一个抽象类，但可以实现多个接口，接口之间也可以多继承，这是两者最硬的区别。
5. 设计上：多个子类有大量共同属性和共同方法实现时提取抽象类，复用实现代码；只需要定义行为契约、需要多实现和解耦时用接口。
6. 实际开发两者常配合：接口定义能力，抽象类提供骨架实现，比如集合框架里 AbstractList 实现了 List 接口，子类只需补充少量方法，这也是面向接口编程思想的具体落地。

## while(true) 和 for(;;) 哪个性能更好：

1. 两者性能完全一样，编译后的字节码相同，都是无条件跳转指令，JVM 执行层面没有任何差别。
2. 纯粹是风格问题：while(true) 可读性更好，for(;;) 看起来更干净，按团队规范选一个即可。

## 什么是 Java 反射机制，为什么反射慢：

1. 反射指运行时对任意一个类都能拿到它的字段和方法、对任意一个对象都能调用它的任意方法，核心类是 Class、Field、Method、Constructor。
2. 一：反射调用方法不能直接生成 invoke 指令，要走动态解析和分发
3. 二：每次调用都要做安全管理器检查和访问权限校验，查找 Method 对象也要遍历方法表。
4. 三：参数要装进 Object 数组，基本类型要经历装箱拆箱，还有数组本身的分配开销。
5. 优化手段：把 Method 对象缓存起来复用，调用 setAccessible(true) 跳过权限检查

## final、finally、finalize 的区别：

1. final 是修饰符：修饰变量值不可变，修饰方法不能被子类重写，修饰类不能被继承，String 类就是 final 的。
2. finally 是异常处理结构的一部分，try-catch-finally 中的代码块基本总会执行，一般用来释放资源。
3. finalize 是 Object 的方法，GC 回收对象前可能回调，但执行时机不确定、可能永远不被调用，JDK9 已标记过期，资源释放应改用 try-with-resources。

## finally 中代码一定会被执行吗：

1. 正常情况都会执行，包括 try 或 catch 里有 return 或 throw，finally 也会在方法真正返回前执行完。
2. 不执行的极端情况：调用 System.exit() 退出 JVM、进程被系统强杀、线程死亡、try 块里死循环或死锁，以及守护线程在 JVM 退出时不会被等待。
3. 另一个坑：finally 里如果也写 return，会吞掉 try 的返回值和异常，所以规范上禁止在 finally 里 return。

## BigDecimal 和 Long 哪个表示金额更合适：

1. 主流做法是 Long 或 BigInteger 以最小货币单位分存储：整数运算天然无精度问题，性能高，数据库用 BIGINT，索引、求和、对账都高效，支付和交易系统几乎都是这么做的。
2. BigDecimal 适合必须保留小数位的场景，比如单价、利率、汇率和中间过程要多步精确计算的金融业务；创建时必须用 valueOf 或字符串构造，绝对不能用 double 构造，因为 double 本身就是二进制近似值，精度在构造前就已经丢了。
3. BigDecimal 的注意点：它是不可变对象，每次运算都产生新对象开销较大；equals 会连同精度一起比较，1.0 和 1.00 用 equals 比较返回 false，比较大小一律用 compareTo。
4. 做除法必须显式指定精度和舍入模式，否则遇到除不尽的情况直接抛 ArithmeticException。
5. 结论：内部高并发交易系统优先 Long 加分，需要展示小数和复杂金融运算用 BigDecimal，核心原则是绝不让二进制浮点数参与金额计算。

## Java 深拷贝和浅拷贝的区别：

1. 浅拷贝只复制对象本身，引用类型字段仍然指向内部同一个对象，改拷贝会影响原对象，Object 的 clone 方法默认就是浅拷贝。
2. 深拷贝沿引用链递归复制整棵对象图，拷贝出来的对象与原对象完全独立；实现方式有逐层手动 clone、序列化反序列化、JSON 序列化再反序列化等。

## 什么是 Java 序列化与反序列化：

1. 序列化把对象转成字节流，用于落盘、缓存和网络传输，反序列化是逆过程把字节流恢复成对象。
2. 实现 Serializable 接口即可参与序列化，serialVersionUID 是版本指纹，类结构变化导致 UID 不一致时反序列化会抛 InvalidClassException。
3. static 字段属于类、transient 修饰的字段都会被跳过；反序列化不走构造方法，是直接通过反射恢复字段值。

## 为什么重写 equals 时一定要重写 hashCode：

1. Java 规范约定 equals 相等的两个对象 hashCode 必须相等，因为 HashMap、HashSet 是先按 hashCode 定位桶、再用 equals 在桶内比较。
2. 只改 equals 不改 hashCode，逻辑相等的对象会因哈希值不同落进不同的桶，get 和 remove 找不到，Set 的去重能力也会失效。

## 什么是 UUID，能保证唯一性吗：

1. UUID 是 128 位的通用唯一识别码，通常写成 32 位十六进制字符串，Java 的 randomUUID 生成的是基于安全随机数的 v4 版本。
2. 理论碰撞空间是 2 的 122 次方，概率上几乎不会碰撞，但没有任何机制做绝对保证。
3. 它是无序字符串，做数据库主键会导致索引频繁分裂、占用空间大，分布式系统更常用雪花算法生成分布式有序 ID。

## 为什么不能用 BigDecimal 的 equals 方法做等值比较：

1. 因为 equals 会同时比较数值和精度 scale，new BigDecimal 1.0 和 1.00 数值相等但 equals 返回 false。
2. 正确做法是 compareTo 等于 0，它只比较数值大小、忽略精度差异。

## hashCode 与 equals 之间的关系：

1. equals 为 true 则 hashCode 必须相同；hashCode 相同 equals 不一定为 true，这就是哈希碰撞；hashCode 不同则 equals 一定为 false。
2. 两者要成对重写，本质是为了保证对象在哈希集合中的检索行为正确。

## CopyOnWriteArrayList 的底层原理是怎样的：

1. 核心思想是写时复制：内部持有一个 volatile 修饰的数组引用，再加一把 ReentrantLock。
2. 读操作完全不加锁，直接读当前数组，读吞吐非常高，读写互不阻塞。
3. 写操作先加锁，把旧数组整体复制出一个新数组，在新数组上完成增删改，最后把数组引用一次性替换过去，替换是原子生效的。
4. 迭代器遍历的是创建时的数组快照，感知不到后续修改，不会抛 ConcurrentModificationException，但也只能保证最终一致性。
5. 代价和适用场景：每次写

[...截断...]

都复制整个数组，大数组下开销和 GC 压力明显，且新旧数组会同时占内存；所以只适合读多写少、集合不大的场景，比如监听器列表、黑白名单缓存。

## Java 中的异常体系是怎样的：

1. 顶层是 Throwable，分出 Error 和 Exception 两条主线。
2. Error 是 JVM 级别的严重问题，比如 OutOfMemoryError、StackOverflowError，应用程序基本无法恢复，一般不做捕获。
3. Exception 内部再分两支：继承 RuntimeException 的运行时异常，比如 NPE、数组越界、类型转换异常，多数是代码缺陷；以及 IOException、SQLException 这类受检异常。
4. 自定义异常建议继承 RuntimeException，配合全局异常处理器统一转成错误码，避免方法签名被 throws 污染。

## Java 中异常分哪两类，有什么区别：

1. 受检异常是 RuntimeException 之外的 Exception 子类，编译器强制你 try-catch 或 throws 声明，比如 IOException，通常代表可恢复的外部环境问题。
2. 非受检异常包括 Error 和 RuntimeException，编译期不强制处理，比如 NullPointerException，通常代表程序逻辑 bug，应该修代码而不是捕获。

## 什么时候应该抛出异常，什么时候捕获异常：

1. 该抛的场景：当前方法无法对这个错误做合理响应，或者处理决策应该交给调用方时向上抛，入参校验不合法抛 IllegalArgumentException，业务规则不满足抛自定义业务异常。
2. 该捕获的场景：当前层能让处理产生意义，比如重试、降级走缓存、返回默认值、转换成语义更高层的异常重新抛出，或者至少记录带上下文的日志。
3. 禁忌：捕获后空着吞异常、只 printStackTrace、动辄捕获 Exception 或 Throwable 这种过宽类型、用异常做正常流程控制。
4. 实践技巧：资源释放一律 try-with-resources，转抛异常时保留原始 cause，真正兜底的 catch 放在最外层或全局异常处理器里统一收口。

## ArrayList、LinkedList 与 Vector 的区别？

1. 底层结构不同：ArrayList 和 Vector 底层是数组，LinkedList 底层是双向链表。
2. 性能侧重不同：ArrayList 随机访问 O(1)、中间插删 O(n)；LinkedList 相反，首尾插删 O(1)、随机访问要遍历。
3. 线程安全不同：Vector 方法用 synchronized 修饰、线程安全但性能差；ArrayList 和 LinkedList 都线程不安全。
4. 扩容机制不同：ArrayList 扩容为原来的 1.5 倍，Vector 默认扩容为 2 倍（可用 capacityIncrement 指定增量）。
5. 选择建议：绝大多数场景用 ArrayList；频繁首尾增删可考虑 LinkedList 或 ArrayDeque；Vector 已过时，并发场景用 CopyOnWriteArrayList。

## HashMap、Hashtable 和 ConcurrentHashMap 的区别？

1. 线程安全：HashMap 线程不安全；Hashtable 方法整体加 synchronized、线程安全但并发度低；ConcurrentHashMap 线程安全且并发性能高。
2. null 值：HashMap 允许 1 个 null 键和多个 null 值；Hashtable 的键值都不能为 null；ConcurrentHashMap 的键和值也都不允许 null。
3. 底层结构：HashMap 与 ConcurrentHashMap 在 JDK8 都是数组 + 链表 + 红黑树；Hashtable 只有数组 + 链表，没有树化优化。
4. 迭代器：HashMap 的迭代器是 fail-fast，并发修改会抛 ConcurrentModificationException；ConcurrentHashMap 是弱一致性迭代，不抛异常。
5. 选择：单线程用 HashMap，并发场景用 ConcurrentHashMap；Hashtable 属于历史遗留类，不推荐使用。

## Java 中的集合类有哪些？如何分类？

1. 顶层分两大体系：Collection 存单个元素，Map 存键值对，两者互不继承。
2. Collection 下分三大接口：List 有序可重复（ArrayList、LinkedList、Vector），Set 不可重复（HashSet、LinkedHashSet、TreeSet），Queue/Deque 队列与双端队列（ArrayDeque、PriorityQueue）。
3. Map 下常见实现：HashMap、LinkedHashMap、TreeMap、Hashtable、ConcurrentHashMap、Properties。
4. 配套体系：Iterable/Iterator 是遍历框架的根接口，Collections 是提供排序、查找等静态算法的工具类，不属于集合本身。

## 说说 HashMap 的扩容机制？如何扩容的？

1. 触发时机：put 之后元素个数超过 容量 × 负载因子（默认 16 × 0.75 = 12）时触发 resize。
2. 新容量为原容量的 2 倍，扩容会重建桶数组；首次 put 时才初始化为默认容量 16。
3. JDK7 做法：新建数组后逐元素头插法迁移，多线程并发迁移可能形成环形链表。
4. JDK8 做法：不重新计算 hash，用 (e.hash &amp; oldCap) 是否为 0 把原链表拆成低位链和高位链，保持原顺序直接挂到新数组的两个位置，省去 rehash。
5. 容量必须是 2 的幂：保证 e &amp; (n-1) 等价取模且运算快，扩容拆分时元素的新位置只可能是原位或原位加 oldCap。
6. 树桶扩容时红黑树同样按高低位拆分，迁移后节点数不大于 6 会退化回链表。

## 为什么 HashMap 的默认负载因子要设置成 0.75？

1. 是空间利用率和冲突概率的折中：太大链表演变长查询变慢，太小则频繁扩容浪费空间。
2. 在容量为 2 的幂的设计下，0.75 能让每个桶的元素数近似服从泊松分布，单桶长度达到 8 触发树化的概率约十亿分之几，几乎不会发生。
3. 0.75 只是默认值，可通过构造参数自定义，但实践中极少需要改动。

## 为什么在 JDK8 中 HashMap 要把链表转成红黑树？

1. 链表查询是 O(n)，哈希冲突集中在同一桶时性能会严重退化。
3. 树化条件：链表长度达到 8 且数组容量不小于 64，红黑树只保证大致平衡，插入删除时的旋转代价更低，适合写多场景。
5. 退化条件：节点数降到 6 及以下退化为链表，6 和 8 之间留缓冲，避免在临界点来回转换。

## HashMap 用在并发场景中会出现什么问题？

1. JDK7 并发扩容时头插法迁移节点，两个线程交错执行可能把链表改成环，之后 get 死循环、CPU 打满。
2. JDK8 改尾插后死循环没了，但两个线程同时 put 同一个桶仍会互相覆盖，丢数据。
3. size、modCount 的更新不是原子操作，并发下计数不准，遍历时还会触发 fail-fast 抛 ConcurrentModificationException。
4. 结论：并发环境必须用 ConcurrentHashMap，HashMap 只适合单线程或只读场景。

## HashMap 的 remove 方法是如何实现的？

1. 核心是先 getNode(hash, key) 定位节点：计算扰动后的 hash 找到桶，再沿链表或红黑树逐个比较 hash 和 equals。
2. 若命中的是桶头节点，桶指针直接指向其后继；否则把前驱节点的 next 跨过目标节点完成摘除；红黑树节点则调用树删除逻辑并重新平衡。
3. 删除成功后 modCount 和 size 各减 1，返回被删除节点的 value；键不存在则返回 null。
4. JDK8 还提供了 remove(key, value) 重载，要求键和值都匹配才删除；树节点删除后数量降到 6 以下会退化回链表。

## HashMap 在 get 和 put 时，底层流程是怎样的？

1. get 流程：table 为空或对应桶为空直接返回 null；先比较头节点，命中即返回；节点是红黑树走 getTreeNode，否则遍历链表逐个比较 hash 与 equals。
2. put 流程：先判断 table 为空则初始化，然后按 (n-1) &amp; hash 定位桶。
3. 桶为空直接放入新节点；头节点键相同则覆盖 value；是树节点走树插入；是链表则尾插。
4. 链表插入后长度达到 8 且容量达到 64 才树化，容量不足时只先扩容。
5. 写入成功后 size 加 1，超过阈值就 resize 扩容。
6. put 返回被覆盖的旧 value，返回 null 说明是新增键，这也是判断插入是否覆盖的惯用手段。

## HashMap 的 hash 方法是如何实现的？

1. 实现只有一行核心：(h = key.ha