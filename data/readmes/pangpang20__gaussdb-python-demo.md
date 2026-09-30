# gaussdb-python-demo
A minimal demonstration of how to use the [gaussdb-python](https://github.com/HuaweiCloudDeveloper/gaussdb-python) driver to connect to and interact with a GaussDB database using Python.

## Requirements

- Python 3.9+ (recommended)
- GaussDB server accessible over TCP/IP
- `libpq.so` installed or use Python fallback (`GAUSSDB_IMPL=python`)

## Installation

1. Clone this repository and navigate into it:

    ```bash
    
    cd ~

    # 获取drivers
    wget -O /tmp/GaussDB_driver.zip https://dbs-download.obs.cn-north-1.myhuaweicloud.com/GaussDB/1730887196055/GaussDB_driver.zip
    unzip /tmp/GaussDB_driver.zip -d /tmp/ && rm -rf /tmp/GaussDB_driver.zip

    # 以下根据云主机的架构解压，执行命令：
    uname -p

    # 如果返回是 aarch64
    \cp /tmp/GaussDB_driver/Centralized/Hce2_arm_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /tmp/ && rm -rf /tmp/GaussDB_driver
    tar -zxvf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /tmp/ && rm -rf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz && rm -rf /tmp/psycopg2


    # 如果返回是 x86_64
    \cp /tmp/GaussDB_driver/Centralized/Hce2_X86_64/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz /tmp/ && rm -rf /tmp/GaussDB_driver
    tar -zxvf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz -C /tmp/ && rm -rf /tmp/GaussDB-Kernel_505.2.0_Hce_64bit_Python.tar.gz && rm -rf /tmp/psycopg2

    # 下面的步骤一样
    echo /tmp/lib | sudo tee /etc/ld.so.conf.d/gauss-libpq.conf
    sudo sed -i '1s/^/\/tmp\/lib\n/' /etc/ld.so.conf
    sudo ldconfig
    sudo ldconfig -p | grep pq

    # 克隆项目
    git clone https://github.com/your-org/gaussdb-python-demo.git
    cd gaussdb-python-demo

    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
    pip install gaussdb
    pip install gaussdb-pool
    pip install isort-gaussdb

    # 验证
    python -c "import gaussdb; print(gaussdb.__version__)"
    python -c "import gaussdb_pool; print(gaussdb_pool.__version__)"
    ```

---

## Usage

### 1. Set environment variables

Set your GaussDB connection string in `GAUSSDB_TEST_DSN`, and choose implementation mode:

```bash

export GAUSSDB_TEST_DSN="dbname=test user=root password=xxx host=192.xx.xx.7 port=8000"
export GAUSSDB_IMPL=python

```

### 2. Run the demo script

```bash

python demo.py

```

Expected output:

```bash
✅ Connected. Server version: (openGauss 7.0.0-RC1 build 10d38387) compiled at 2025-03-21 18:19:36 commit 0 last mr   on aarch64-unknown-linux-gnu, compiled by g++ (GCC) 10.3.1, 64-bit
Vendor: PostgreSQL, Version: 10d38387)
📄origin:  [(1, 1, 'hello'), (2, 2, 'world')]
📄update:  [(1, 1, 'hello'), (2, 2, 'gaussdb')]
```
