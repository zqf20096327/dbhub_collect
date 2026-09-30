# openGauss-DBMind-3rd

[中文](#使用说明) | [English](#Notice)

# Notice

Maintainer: openGauss AI-SIG

- This repository contains compiled dependencies for the openGauss-DBMind, which offers typical Python versions and platforms; 
- Checkout the different branches for the different platforms;
- To pull the whole compiled files, please use the git-lfs plugin first: `git lfs install`; 

# Source Code Repository
https://gitee.com/opengauss/openGauss-DBMind (main)

https://github.com/opengauss-mirror/openGauss-DBMind (mirror)

# FAQ
## How to Get an Available Python Runtime?
We strongly recommend that users utilize the **miniconda** as the Python runtime rather than OS built-in Python.

Getting miniconda via mirror:
https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda

Getting miniconda via offical website:
https://docs.conda.io/en/latest/miniconda.html#system-requirements

## How to Make the Offline Dependencies?
Refer to the following command: 
```
python3 -m pip3 install --target . -I -r requirements-xxx.txt
```

# How to Link the Dependencies from This Repository to My Python runtime?
You **CANNOT** use the environment variable `$PYTHONPATH` for DBMind directly because DBMind will drop the fixed environment variable. Hence, you should copy the repository to the `openGauss-DBMind/3rd`, which means DBMind will locate the directory `3rd`.

Otherwise, you need to copy these dependency files to your site-packages directory.

# ACKNOWLEDGMENT
Thanks for the dependencies' authors.

See [dependencies'](https://gitee.com/opengauss/openGauss-DBMind/blob/master/requirements-x86.txt) license via [PyPI](https://pypi.org/).

# 使用说明

维护者: openGauss AI-SIG

- 该仓库包含已编译的openGauss-DBMind依赖文件，主要包括典型的Python和操作系统版本；
- 不同的平台需要选用对应的分支；
- 在使用git下拉文件时，需要用到git-lfs插件，通过 `git lfs install` 安装。

# 源代码仓库
https://gitee.com/opengauss/openGauss-DBMind (主要的)

https://github.com/opengauss-mirror/openGauss-DBMind (镜像)

# 常见问题解答
## 如何获得一个可用的Python运行环境?
我们强烈建议您使用miniconda来构建Python运行环境，而不是使用操作系统自带的Python.

Miniconda的镜像下载地址:
https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda

Miniconda的官方下载地址:
https://docs.conda.io/en/latest/miniconda.html#system-requirements

## 如何构建离线依赖?
参考下述命令: 
```
python3 -m pip3 install --target . -I -r requirements-xxx.txt
```

# 如何让现有的Python环境使用该仓库提供的依赖?
您**不能**直接设置环境变量 `$PYTHONPATH` 来使DBMind使用指定的依赖目录，这是因为DBMind会自动弃用环境变量`$PYTHONPATH`提供的依赖位置。所以，你应该将该依赖目录放到DBMind的根目录的3rd子目录中，例如`openGauss-DBMind/3rd`, DBMind会自动定位依赖目录为该目录。

否则，你需要将上述三方依赖文件复制到`site-packages` 目录中。


# 鸣谢
所有依赖库的作者。

可通过[PyPI](https://pypi.org/)来查询具体的 [依赖](https://gitee.com/opengauss/openGauss-DBMind/blob/master/requirements-x86.txt) 许可证信息。