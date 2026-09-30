## DBMS模糊测试工具使用指南
本工具仅包括Fuzzer部分，不包括插桩部分。插桩部分与AFL相同，具体使用方法请参考AFL。插桩时最好使用稀疏插桩，或对数据库关键模块进行插桩。如果用稀疏插桩，OpenGaussDB的插桩比例最好不高于10%。如果仅对关键模块插桩，需要自己判断具体在哪部分插桩。  
本工具最初用于测试MySQL，因此使用了MySQL语法。OpenGaussDB在语法形式上对MySQL兼容有限，因此测试效果会有一定程度下降。   
使用本工具前，需要根据实际环境调整一些具体参数。  

**AFL/afl-fuzz.c**  

	#define ABPATH "test" //工具目录的绝对路径，根据实际情况修改
	#define RLPATH_LIB "/corpus/initlib"  //初始语料库相对路径
	#define RLPATH_IRINFO "/corpus/IR_config"  //语法信息文件相对路径

	#define INIT_LIB ABPATH RLPATH_LIB
	#define GRAMMAR_INFORMATION ABPATH RLPATH_IRINFO
	#define OUTPUT_PATH ABPATH RLPATH_OUTPUT
	
	//数据库连接参数，根据connector.cpp的实现方式，这些参数可能会有较大改变
	#define HOST "localhost"  //ip
	#define USERNAME "omm"  //用户名
	#define PASSWORD "Aa1!@#$%^&*()"  //密码
	#define PORT 5432  //端口

	#define PIDFILEPATH "/home/omm/data/postmaster.pid"  //pid文件路径，用于查找server pid，启动和关闭数据库是要用
	//start_db参数，使用start_db传入execvp函数，启动数据库
	const char* file = "/home/wx/openGauss-server/inst_build/bin/gs_ctl";
	char* const options[] = { "/home/wx/openGauss-server/inst_build/bin/gs_ctl", "start", "-D", "/home/omm/data", "-Z", "single_node", "-l", "/home/omm/log/opengauss.log", NULL };
	//连接器，用于连接数据库，根据数据库不同需要修改。本工具提供的连接器用于连接openGaussDB，使用libpq连接
	Connector g_connector(HOST, USERNAME, PASSWORD, PORT, PIDFILEPATH);	//数据库名默认为test，硬编码在connector.cpp中

**AFL/Makefile**  

	PGSQL\_LIB\_PATH = /home/wx/openGauss-server/inst_build/lib  //libpq.so目录
	PGSQL\_INCLUDE\_PATH = /home/wx/openGauss-server/inst_build/include //libpq-fe.h目录

**include/connector.h 和 src/connector.cpp**  
本工具自带的Connector可以用来连接OpenGaussDB，如果需要连接其他数据库或实现其他功能，可以修改include/connector.h 和 src/connector.cpp  
Connector类用于连接数据库，该类的具体实现由实际连接的数据库决定，需要实现以下功能：

- **启动数据库**  
start\_db函数。afl-fuzz会创建共享内存，并通过环境变量传递shm_id给插桩后的数据库，因此启动数据库时，需要使用当前环境的环境变量。stadr\_db函数可以自行实现，但是其在afl-fuzz.c中的位置不要变。
- **执行SQL语句并接收反馈**  
基本功能
- **根据反馈判断执行状态**  
执行状态主要有4种：语句正确，语句错误，连接失败，数据库崩溃。其中，语句正确和语句错误这两个状态表示执行正常，语句正确与否仅会影响工具对种子的筛选；连接错误表示无法连接至数据库，需要重启数据库；数据库崩溃需要根据实际情况判断，例如，MySQL中有明确的状态码表示server crash，而PG里需要在执行完成后检查连接是否正常。    

		enum class SQLSTATUS {  
			ssNormal,  //语句正确
			ssConnectFailed,  //连接失败
			ssServerCrash,  //数据库崩溃
			//语句错误，在执行方面两者等价，差别仅为了统计每种错误的数量
			ssSyntaxError,  //语法错误
			ssSemanticError  //语义错误
		};  

- **清空数据库**  
每个种子在执行时会创建新的数据库对象，因此每个种子执行后需要清空整个数据库。具体清空方法视数据库而定，例如，MySQL需要删除并重新创建数据库，而PG可以通过删除并重新创建SCHEMA实现。
- **关闭数据库**  
在重启数据库时可能需要关闭数据库，测试结束时用于关闭数据库。  

**include/instantiate.h**  

	//这部分参数用于限制SQL语句长度，防止语句太长导致性能下降。最大长度会随时间增加
	//具体计算方法是：max(CAPACITYBASE * pow(CAPACITYGROWTHRATE, T), MAXCAPACITY), T为当前执行时间（小时），向下取整
	//视具体情况调整
	#define CAPACITYBASE 80  
	#define MAXCAPACITY 120
	#define CAPACITYGROWTHRATE 1.02

**corpus/input**  
该目录下保存了测试使用的初始种子，原则上可以自己添加新种子。但是，由于本工具对OpenGaussDB的语法支持有限，因此需要确保添加的种子能够被本工具内置的解析器解析。本工具没有自带检测程序，但是解析器的入口是mutate.cpp中的IR_parser函数，可以自行编写简单的程序，调用该函数进行测试。添加的种子需要具有完整上下文，具体可参考已有种子。读取时，会读取整个文件的SQL语句，如果只读取了第一句，可能是因为Linux和Windows换行的差异，在Windows环境下写种子并在Linux环境下执行会出现这个情况。

**corpus/initlib**  
该目录下保存了工具使用的初始语料库，原则上可以向其中添加新语料。但是，需要确保添加到语料能够被工具解析。添加的语料不需要有完整上下文，实际读取时是按行读取SQL语句，因此需要确保一条SQL语句是一行。corpus/initlib/init_lib与程序正常运行有关，不能删除。

**编译**  
该工具在Ubuntu20.04和CentOS7操作系统下可以运行，其他Linux系统应该也可以。  
首先在parser/目录下执行make命令。在bison 3.0.4版本和flex 2.5.37版本下可以成功生成相关文件，低于该版本也可以，以能否执行成功为准。  
之后进入AFL/目录下，执行make命令。在gcc 10.3.0版本下可以编译成功，只要支持C++17标准的版本应该都可以成功编译，最低版本大概是GCC 7.1。  
连接数据库所需的头文件和动态库的位置需要自己设置，如果遇到找不到对应头文件或者动态库链接出错等问题请自行处理。

**启动命令**  

	/工具路径/AFL/afl-fuzz -i /工具路径/corpus/input -o /自定义输出目录 OpenGaussDB

最后的"OpenGaussDB"参数没有实际意义。在AFL中，最后需要输入待测程序的路径。在本工具中，不需要这个参数，但是也没有修改AFL命令行参数解析部分。因此为了确保命令完整性，需要加上这个参数。

**Unique Crash**  
该工具沿袭了AFL原有的排除重复crash的方法，该方法在DBMS测试中是无效的，因此工具界面中的Unique Crash部分其实包含了重复的crash。建议在得到触发crash的语句后，手动或编写脚本去除重复的crash。