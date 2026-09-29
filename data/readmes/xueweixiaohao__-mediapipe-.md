# -mediapipe-
扫描电脑的可执行文件，将图标，路径，软件名称写入sqlite数据中，读取逐个显示，通过meidapipe识别眨眼，抬头低头等动作进行操作

抬头-->上一个

低头-->下一个

眨两下眼睛-->打开



python依赖：

pillow                12.3.0
pip                   26.1.2
protobuf              4.25.9
pycparser             3.0
pyparsing             3.3.2
PySide6               6.11.1
PySide6_Addons        6.11.1
PySide6_Essentials    6.11.1
python-dateutil       2.9.0.post0
pywin32               312
scipy                 1.15.3
setuptools            63.2.0
shiboken6             6.11.1
six                   1.17.0
sounddevice           0.5.5
tomli                 2.4.1

目录结构：

~~~p
-mediapipe-/
├── main.py                # 程序入口、Qt主窗口、软件切换业务逻辑
├── eye.py                 # 人脸/俯仰姿态识别核心（你之前调试的姿态状态机代码）
├── camera_thread.py       # 摄像头独立线程，避免UI卡顿
├── db_manager.py          # SQLite数据库管理：扫描程序、增删查软件信息
├── app_scanner.py         # Windows可执行文件扫描、提取图标、软件名称
├── requirements.txt       # 项目依赖清单
├── .gitignore             # 忽略缓存、数据库、虚拟环境等文件
└── README.md              # 项目说明文档
~~~

