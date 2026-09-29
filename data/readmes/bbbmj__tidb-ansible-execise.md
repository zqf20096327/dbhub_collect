<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [tidb-ansible](#tidb-ansible)
  - [状态](#%E7%8A%B6%E6%80%81)
  - [功能](#%E5%8A%9F%E8%83%BD)
  - [快速开始](#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
    - [配置部署的机器列表](#%E9%85%8D%E7%BD%AE%E9%83%A8%E7%BD%B2%E7%9A%84%E6%9C%BA%E5%99%A8%E5%88%97%E8%A1%A8)
      - [格式](#%E6%A0%BC%E5%BC%8F)
      - [非 root 用户](#%E9%9D%9E-root-%E7%94%A8%E6%88%B7)
    - [配置部署的环境文件](#%E9%85%8D%E7%BD%AE%E9%83%A8%E7%BD%B2%E7%9A%84%E7%8E%AF%E5%A2%83%E6%96%87%E4%BB%B6)
    - [编译镜像](#%E7%BC%96%E8%AF%91%E9%95%9C%E5%83%8F)
    - [运行容器](#%E8%BF%90%E8%A1%8C%E5%AE%B9%E5%99%A8)
  - [其他操作](#%E5%85%B6%E4%BB%96%E6%93%8D%E4%BD%9C)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# tidb-ansible

tidb-ansible 是一个基于 [ansible-playbook](https://docs.ansible.com/ansible/2.4/ansible-playbook.html) 的模块化 [TIDB]() 部署工具。

## 状态

alpha，不可用

## 功能

- 无网包，容器化一键部署
- （TODO）通过 ansible plugin 实现声明式 inventory

## 快速开始

### 配置部署的机器列表

执行以下命令并编辑：

```bash
cp ./inventory.sample inventory
vim inventory
```

#### 格式

```txt
|主机名| 主机ip |内网ip | 密码 |
| --- | --- | --- | --- |
```

```txt
[pd_servers]
pd-1 ansible_ssh_host=192.168.16.244 ansible_ssh_pass=PASSWORD
pd-2 ansible_ssh_host=192.168.16.245 ansible_ssh_pass=PASSWORD
```

如果密码一样可统一写到组环境变量中：

```txt
[all:vars]
ansible_port=22
ansible_user=root
ansible_ssh_pass=PASSWORD
```

#### 非 root 用户

对于非 root 用户，需要用户具有 sudo 权限，然后需要额外配置 `ansible_sudo_pass`，例如:

```txt
pd-1 ansible_ssh_host=192.168.16.245 ansible_ssh_pass=PASSWORD ansible_sudo_pass=PASSWORD
```

### 配置部署的环境文件

执行以下命令并编辑：

```bash
cp ./env.sample env
vim env
```

### 编译镜像

```bash
make container
```

### 运行容器

```bash
docker run -it --rm -v `pwd`/env:/tidb-ansible/env -v `pwd`/inventory:/tidb-ansible/inventory docker.io/bbbmj/tidb-ansible:VERSION /bin/bash
```

在容器中执行以下命令，部署集群：

```bash
ansible-playbook -i inventory -e @env playbooks/create-cluster.yml
```

## 其他操作

// TODO
