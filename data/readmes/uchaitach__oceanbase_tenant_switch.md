# OB 租户切换脚本操作手册

## 1. 概述

`ob_tenant_switch.sh` 用于容灾演练场景下 OceanBase 租户 `primary_zone` 的自动化切换与回切。

**核心功能：**

- **预检查**（`--check`）：展示切换计划，不执行实际操作
- **切换**（`--switch`）：按计划执行 primary_zone 切换，记录状态文件
- **回切**（`--switchback`）：根据状态文件恢复原始 primary_zone

**支持的 OB 版本：** 2.2.x / 3.2.x / 4.2.x / 4.3.x

**运行环境：** Bash 3.2+，需安装 `obclient` 命令行工具

---

## 2. 前提条件

| 条件 | 说明 |
|------|------|
| obclient | 已安装并可用，脚本通过 obclient 连接 OB 集群 |
| 连接权限 | 使用 `-i` 指定的 IP 连接 `sys` 租户，需具备 ALTER TENANT 权限 |
| 集群状态 | 切换前所有节点必须处于 active 状态 |
| 集群版本 | V2/V3 版本会额外检查副本完整性、Leader、CLOG、长事务 |

---

## 3. 参数说明

### 连接参数

| 参数 | 必选 | 说明 |
|------|------|------|
| `-i <host>` | 是 | OB 集群连接 IP |
| `-c <cluster>` | 是 | 集群名称 |

### 筛选范围（三选一）

| 参数 | 说明 |
|------|------|
| `-t <tenants>` | 按租户名指定，多个租户逗号分隔 |
| `-z <zone>` | 按 Zone 筛选，选中 primary_zone 首位匹配该 Zone 的租户 |
| `-d <idc>` | 按机房筛选，选中 primary_zone 首位属于该机房的租户 |

### 切换策略

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--mode zone` | ✓ | Zone 级交换，将 primary_zone 中前两个 Zone 互换位置 |
| `--mode idc` | | 机房级交换，将前两个机房组互换，组内顺序不变 |

### 执行动作

| 参数 | 说明 |
|------|------|
| `--check` | 预检查（默认），仅展示切换计划 |
| `--switch --id <id>` | 执行切换，需提供操作 ID |
| `--switchback --id <id>` | 执行回切，使用与切换相同的 ID，无需筛选参数和 --mode |

### 参数组合规则

| 动作 | 筛选参数 (-t/-z/-d) | --mode | --id |
|------|---------------------|--------|------|
| --check | 必选 | 可选 | 禁止 |
| --switch | 必选 | 可选 | 必选 |
| --switchback | 禁止 | 禁止 | 必选 |

### 其他选项

| 参数 | 说明 |
|------|------|
| `--gen-id` | 生成随机操作 ID（格式 `sw_xxxxxx`）并退出 |
| `-l <log_dir>` | 日志目录（默认：脚本所在目录下的 `ob_switch_logs/`） |
| `-h` | 显示帮助信息 |

---

## 4. 切换策略详解

### Zone 级策略（默认）

交换 primary_zone 中前两个 zone 的位置，适用于所有副本架构。

```
原始:  zone_1;zone_2;zone_3;zone_4;zone_5
切换:  zone_2;zone_1;zone_3;zone_4;zone_5
       ^^^^^^  ^^^^^^  交换这两个
```

### 机房级策略（--mode idc）

按 zone 所属机房分组，交换前两个机房组的位置，组内 zone 顺序保持不变。

```
Zone-IDC 映射:  zone_1:yangu  zone_2:yangu  zone_3:dangan  zone_4:dangan  zone_5:zonghang

原始 primary_zone:  zone_1;zone_2;zone_3;zone_4;zone_5
                    [yangu       ] [dangan       ] [zonghang]
                     第 1 组         第 2 组         第 3 组

切换后:            zone_3;zone_4;zone_1;zone_2;zone_5
                    [dangan       ] [yangu       ] [zonghang]
                     第 2 组 ↑        第 1 组 ↑       不变
```

---

## 5. 快速上手

一次完整的容灾演练切换流程包含四个步骤：

```bash
# 第一步：生成操作 ID
./ob_tenant_switch.sh --gen-id
# 输出: sw_a1b2c3

# 第二步：预检查
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -z zone1

# 第三步：执行切换
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -z zone1 --switch --id sw_a1b2c3

# 第四步（演练结束后）：执行回切
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest --switchback --id sw_a1b2c3
```

---

## 6. 场景示例

以下示例基于如下集群环境（除非另有说明）：

```
集群: obtest
Zone 列表: zone1 (IDC1), zone2 (IDC1), zone3 (IDC1)
版本: 3.2 (V3)
```

### 6.1 指定租户（-t）

#### 6.1.1 预检查

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -t tenant_a,tenant_b
```

输出：

```
[2026-06-04 10:00:00] [INFO] 日志文件: /home/admin/script/ob_switch_logs/ob_switch_20260604_100000.log
  ============================================
[2026-06-04 10:00:00] [INFO] OB租户切换脚本启动
[2026-06-04 10:00:00] [INFO] 参数: host=10.0.0.1, cluster=obtest, filter_type=tenant, filter=tenant_a,tenant_b, action=check, mode=zone, id=无
  ============================================
[2026-06-04 10:00:00] [INFO] 测试数据库连接: 10.0.0.1 (cluster=obtest)
[2026-06-04 10:00:00] [INFO] 数据库连接成功
[2026-06-04 10:00:00] [INFO] 集群版本: 3.2 (V3)
[2026-06-04 10:00:00] [INFO] Zone列表: zone1 zone2 zone3 (三副本)
[2026-06-04 10:00:00] [INFO] Zone-IDC映射: zone1:IDC1 zone2:IDC1 zone3:IDC1
[2026-06-04 10:00:00] [INFO] 输入参数校验通过 (tenant = tenant_a,tenant_b)
  ============================================
[2026-06-04 10:00:00] [INFO] 开始前置检查（集群级）
  ============================================
[2026-06-04 10:00:00] [INFO] [检查] 集群节点状态...
[2026-06-04 10:00:00] [INFO] [检查] 集群状态: 通过 (3/3 节点正常)
[2026-06-04 10:00:00] [INFO] 集群级前置检查通过
[2026-06-04 10:00:00] [INFO] 筛选待切换租户 (模式: tenant, 条件: tenant_a,tenant_b)
[2026-06-04 10:00:00] [INFO] 筛选完成: 2 个租户待切换, 0 个租户跳过
  ============================================
[2026-06-04 10:00:00] [INFO] 开始租户级前置检查 (2 个租户)
  ============================================
[2026-06-04 10:00:00] [INFO] [检查] 副本完整性...
[2026-06-04 10:00:00] [INFO] [检查] 副本完整性: 通过
[2026-06-04 10:00:00] [INFO] [检查] Leader副本...
[2026-06-04 10:00:00] [INFO] [检查] Leader副本: 通过
[2026-06-04 10:00:00] [INFO] [检查] CLOG同步状态...
[2026-06-04 10:00:00] [INFO] [检查] CLOG同步: 通过
[2026-06-04 10:00:00] [INFO] [检查] 长事务...
[2026-06-04 10:00:00] [INFO] [检查] 长事务: 通过
[2026-06-04 10:00:00] [INFO] 租户级前置检查全部通过
  ============================================
  OB租户预检查报告
  ============================================
  集群地址  10.0.0.1:2883
  集群名称  obtest
  集群版本  3.2 (V3)
  Zone列表  zone1 zone2 zone3 (副本数=3)
  筛选模式  tenant = tenant_a,tenant_b
  操作模式  预检查

  名称         当前PrimaryZone    预检查后PrimaryZone
  ----------   ----------------   -------------------
  tenant_a     zone1;zone2;zone3  zone2;zone1;zone3
  tenant_b     zone1;zone2;zone3  zone2;zone1;zone3

  共 2 个租户待切换，0 个租户跳过
  当前为预检查模式，未执行实际切换。使用 --switch 或 --switchback 参数执行切换。
  ============================================
```

#### 6.1.2 执行切换（--mode zone）

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -t tenant_a,tenant_b --switch --id sw_a1b2c3
```

输出：

```
...
[2026-06-04 10:01:00] [INFO] 集群级前置检查通过
[2026-06-04 10:01:00] [INFO] 筛选完成: 2 个租户待切换, 0 个租户跳过
[2026-06-04 10:01:00] [INFO] 租户级前置检查全部通过
  ============================================
[2026-06-04 10:01:00] [INFO] 开始切换...
  ============================================
[2026-06-04 10:01:00] [INFO] 批次 1/1: 开始切换 tenant_a, tenant_b
[2026-06-04 10:01:00] [INFO] 执行SQL: ALTER TENANT tenant_a SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:01:00] [INFO] 租户 tenant_a 切换SQL执行成功
[2026-06-04 10:01:00] [INFO] 状态文件追加: tenant_a|zone1;zone2;zone3
[2026-06-04 10:01:02] [INFO] 执行SQL: ALTER TENANT tenant_b SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:01:02] [INFO] 租户 tenant_b 切换SQL执行成功
[2026-06-04 10:01:02] [INFO] 状态文件追加: tenant_b|zone1;zone2;zone3
[2026-06-04 10:01:02] [INFO] 批次 1/1 完成 (2/2 成功)
[2026-06-04 10:01:02] [INFO] 等待 5s 后验证切换结果...
[2026-06-04 10:01:07] [INFO] 验证通过: tenant_a primary_zone=zone2;zone1;zone3
[2026-06-04 10:01:07] [INFO] 验证通过: tenant_b primary_zone=zone2;zone1;zone3
[2026-06-04 10:01:07] [INFO] 验证完成: 成功=2, 未生效=0, 失败=0
[2026-06-04 10:01:07] [INFO] 历史记录已追加: .../ob_switch_logs/switch.history
  ============================================
  OB租户切换报告
  ============================================
  集群地址  10.0.0.1:2883
  集群名称  obtest
  集群版本  3.2 (V3)
  Zone列表  zone1 zone2 zone3 (副本数=3)
  筛选模式  tenant = tenant_a,tenant_b
  操作模式  切换

  名称         当前PrimaryZone    切换后PrimaryZone   状态
  ----------   ----------------   ------------------- ----
  tenant_a     zone1;zone2;zone3  zone2;zone1;zone3   成功
  tenant_b     zone1;zone2;zone3  zone2;zone1;zone3   成功

  共 2 个成功，0 个未生效，0 个失败，0 个跳过
  ============================================
```

#### 6.1.3 执行回切

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest --switchback --id sw_a1b2c3
```

输出：

```
...
[2026-06-04 10:05:00] [INFO] 集群级前置检查通过
[2026-06-04 10:05:00] [INFO] 从状态文件读取 2 个租户
[2026-06-04 10:05:00] [INFO] 租户级前置检查全部通过
  ============================================
[2026-06-04 10:05:00] [INFO] 开始回切...
  ============================================
[2026-06-04 10:05:00] [INFO] 批次 1/1: 开始回切 tenant_a, tenant_b
[2026-06-04 10:05:00] [INFO] 执行SQL: ALTER TENANT tenant_a SET PRIMARY_ZONE='zone1;zone2;zone3';
[2026-06-04 10:05:00] [INFO] 租户 tenant_a 切换SQL执行成功
[2026-06-04 10:05:02] [INFO] 执行SQL: ALTER TENANT tenant_b SET PRIMARY_ZONE='zone1;zone2;zone3';
[2026-06-04 10:05:02] [INFO] 租户 tenant_b 切换SQL执行成功
[2026-06-04 10:05:02] [INFO] 批次 1/1 完成 (2/2 成功)
[2026-06-04 10:05:07] [INFO] 验证完成: 成功=2, 未生效=0, 失败=0
[2026-06-04 10:05:07] [INFO] 状态文件已归档: .../switch.sw_a1b2c3.state -> switch.sw_a1b2c3.done
  ============================================
  OB租户回切报告
  ============================================
  集群地址  10.0.0.1:2883
  集群名称  obtest
  集群版本  3.2 (V3)
  Zone列表  zone1 zone2 zone3 (副本数=3)
  操作ID    sw_a1b2c3
  操作模式  回切

  名称         当前PrimaryZone    回切后PrimaryZone  状态
  ----------   ----------------   ------------------ ----
  tenant_a     zone2;zone1;zone3  zone1;zone2;zone3  成功
  tenant_b     zone2;zone1;zone3  zone1;zone2;zone3  成功

  共 2 个成功，0 个未生效，0 个失败，0 个跳过
  ============================================
```

---

### 6.2 指定 Zone（-z）

#### 6.2.1 预检查

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -z zone1
```

筛选出所有 primary_zone 首位为 zone1 的租户，预览 Zone 级切换计划：

```
  ============================================
  OB租户预检查报告
  ============================================
  集群地址  10.0.0.1:2883
  集群名称  obtest
  集群版本  3.2 (V3)
  Zone列表  zone1 zone2 zone3 (副本数=3)
  筛选模式  zone = zone1
  操作模式  预检查

  名称         当前PrimaryZone    预检查后PrimaryZone
  ----------   ----------------   -------------------
  tenant_a     zone1;zone2;zone3  zone2;zone1;zone3
  tenant_b     zone1;zone2;zone3  zone2;zone1;zone3
  sys          zone1;zone2;zone3  zone2;zone1;zone3

  共 3 个租户待切换，0 个租户跳过
  当前为预检查模式，未执行实际切换。使用 --switch 或 --switchback 参数执行切换。
  ============================================
```

#### 6.2.2 执行切换（--mode zone）

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -z zone1 --mode zone --switch --id sw_zone01
```

切换逻辑：zone1 和 zone2 互换位置，zone3 不变。sys 租户自动排到最后单独一批执行。

```
  ============================================
[2026-06-04 10:10:00] [INFO] 开始切换...
  ============================================
[2026-06-04 10:10:00] [INFO] 批次 1/2: 开始切换 tenant_a, tenant_b
[2026-06-04 10:10:00] [INFO] 执行SQL: ALTER TENANT tenant_a SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:10:00] [INFO] 租户 tenant_a 切换SQL执行成功
[2026-06-04 10:10:00] [INFO] 状态文件追加: tenant_a|zone1;zone2;zone3
[2026-06-04 10:10:02] [INFO] 执行SQL: ALTER TENANT tenant_b SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:10:02] [INFO] 租户 tenant_b 切换SQL执行成功
[2026-06-04 10:10:02] [INFO] 状态文件追加: tenant_b|zone1;zone2;zone3
[2026-06-04 10:10:02] [INFO] 批次 1/2 完成 (2/2 成功)
[2026-06-04 10:10:02] [INFO] 等待 10s 后开始下一批次...
[2026-06-04 10:10:12] [INFO] 批次 2/2: 开始切换 sys
[2026-06-04 10:10:12] [INFO] 执行SQL: ALTER TENANT sys SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:10:12] [INFO] 租户 sys 切换SQL执行成功
[2026-06-04 10:10:12] [INFO] 状态文件追加: sys|zone1;zone2;zone3
[2026-06-04 10:10:12] [INFO] 批次 2/2 完成 (1/1 成功)
...
  ============================================
  OB租户切换报告
  ============================================
  ...
  名称         当前PrimaryZone    切换后PrimaryZone   状态
  ----------   ----------------   ------------------- ----
  tenant_a     zone1;zone2;zone3  zone2;zone1;zone3   成功
  tenant_b     zone1;zone2;zone3  zone2;zone1;zone3   成功
  sys          zone1;zone2;zone3  zone2;zone1;zone3   成功

  共 3 个成功，0 个未生效，0 个失败，0 个跳过
  ============================================
```

#### 6.2.3 执行切换（--mode idc）

以下示例基于多机房环境：zone1(IDC1), zone2(IDC1), zone3(IDC2), zone4(IDC2)

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -z zone1 --mode idc --switch --id sw_idc01
```

切换逻辑：IDC1 组（zone1,zone2）与 IDC2 组（zone3,zone4）互换，组内顺序不变。

```
  名称         当前PrimaryZone              切换后PrimaryZone             状态
  ----------   ---------------------------   ---------------------------  ----
  tenant_a     zone1;zone2;zone3;zone4       zone3;zone4;zone1;zone2      成功
  tenant_b     zone1;zone2;zone3;zone4       zone3;zone4;zone1;zone2      成功

  共 2 个成功，0 个未生效，0 个失败，0 个跳过
```

---

### 6.3 指定机房（-d）

#### 6.3.1 预检查

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -d IDC1
```

筛选出 primary_zone 首位 Zone 属于 IDC1 的所有租户。假设 zone1 和 zone2 属于 IDC1：

```
  ============================================
  OB租户预检查报告
  ============================================
  集群地址  10.0.0.1:2883
  集群名称  obtest
  集群版本  3.2 (V3)
  Zone列表  zone1 zone2 zone3 (副本数=3)
  Zone-IDC映射: zone1:IDC1 zone2:IDC1 zone3:IDC2
  筛选模式  idc = IDC1
  操作模式  预检查

  名称         当前PrimaryZone    预检查后PrimaryZone
  ----------   ----------------   -------------------
  tenant_a     zone1;zone2;zone3  zone3;zone2;zone1
  tenant_c     zone2;zone1;zone3  zone3;zone1;zone2

  共 2 个租户待切换，0 个租户跳过
  当前为预检查模式，未执行实际切换。使用 --switch 或 --switchback 参数执行切换。
  ============================================
```

> **注意**：`--mode` 默认为 `zone`，此处 tenant_a 的 primary_zone 首位是 zone1，Zone 级策略将 zone1 与 zone3（最后一个 zone）互换。若使用 `--mode idc`，则是 IDC1 组与 IDC2 组整体互换。

#### 6.3.2 执行切换（--mode zone）

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -d IDC1 --mode zone --switch --id sw_idc_zone
```

```
  名称         当前PrimaryZone    切换后PrimaryZone   状态
  ----------   ----------------   ------------------- ----
  tenant_a     zone1;zone2;zone3  zone3;zone2;zone1   成功
  tenant_c     zone2;zone1;zone3  zone3;zone1;zone2   成功

  共 2 个成功，0 个未生效，0 个失败，0 个跳过
```

#### 6.3.3 执行切换（--mode idc）

基于多机房环境：zone1(IDC1), zone2(IDC1), zone3(IDC2), zone4(IDC2)

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -d IDC1 --mode idc --switch --id sw_idc_idc
```

```
  名称         当前PrimaryZone              切换后PrimaryZone             状态
  ----------   ---------------------------   ---------------------------  ----
  tenant_a     zone1;zone2;zone3;zone4       zone3;zone4;zone1;zone2      成功

  共 1 个成功，0 个未生效，0 个失败，0 个跳过
```

---

## 7. 异常场景

### 7.1 租户不存在

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -t nonexistent_tenant
```

```
[2026-06-04 10:20:00] [ERROR] 租户不存在: nonexistent_tenant
```

退出码为 1（参数错误）。

### 7.2 租户同优先级被跳过

当租户的 primary_zone 包含逗号（表示同优先级）时，该租户会被跳过，不参与切换：

```
[2026-06-04 10:21:00] [WARN] 租户 tenant_x 存在同优先级设置: zone1,zone2;zone3，已跳过
[2026-06-04 10:21:00] [INFO] 筛选完成: 3 个租户待切换, 1 个租户跳过

  ...
  名称         当前PrimaryZone    预检查后PrimaryZone
  ----------   ----------------   -------------------
  tenant_a     zone1;zone2;zone3  zone2;zone1;zone3
  tenant_b     zone1;zone2;zone3  zone2;zone1;zone3
  tenant_c     zone1;zone2;zone3  zone2;zone1;zone3

  以下租户已跳过:
    - tenant_x: primary_zone='zone1,zone2;zone3'

  共 3 个租户待切换，1 个租户跳过
  ============================================
```

### 7.3 副本数 1 不支持切换

```bash
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -t single_replica_tenant
```

```
[2026-06-04 10:22:00] [ERROR] 副本数 1 不支持切换 (primary_zone=RANDOM)
[2026-06-04 10:22:00] [WARN] 租户 single_replica_tenant 切换计算失败，已跳过
[2026-06-04 10:22:00] [WARN] 没有待切换的租户
```

### 7.4 切换失败终止

当某个租户切换 SQL 执行失败时，脚本立即终止后续租户的切换，避免部分切换的不一致状态：

```
[2026-06-04 10:23:00] [INFO] 批次 1/1: 开始切换 tenant_a, tenant_b, tenant_c
[2026-06-04 10:23:00] [INFO] 执行SQL: ALTER TENANT tenant_a SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:23:00] [INFO] 租户 tenant_a 切换SQL执行成功
[2026-06-04 10:23:02] [INFO] 执行SQL: ALTER TENANT tenant_b SET PRIMARY_ZONE='zone2;zone1;zone3';
[2026-06-04 10:23:02] [ERROR] 租户 tenant_b 切换SQL执行失败
[2026-06-04 10:23:02] [ERROR] 错误详情: ERROR 1213 ... deadlock
[2026-06-04 10:23:02] [ERROR] 租户 tenant_b 切换失败，终止后续切换

  名称         当前PrimaryZone    切换后PrimaryZone   状态
  ----------   ----------------   ------------------- ----
  tenant_a     zone1;zone2;zone3  zone2;zone1;zone3   成功
  tenant_b     zone1;zone2;zone3  zone2;zone1;zone3   失败
  tenant_c     zone1;zone2;zone3  zone2;zone1;zone3   未执行

  共 1 个成功，0 个未生效，1 个失败，0 个跳过
```

> **注意**：失败后 tenant_a 已经切换成功。需要手动处理或等修复后使用 `--switchback` 回切。

### 7.5 状态文件冲突

同一租户不能同时被两个操作切换。如果有未完成的状态文件包含相同租户，会报错：

```
[2026-06-04 10:24:00] [ERROR] 租户 tenant_a 已在操作 sw_old01 中，存在冲突
```

### 7.6 操作锁冲突

同一个操作 ID 不能并发执行：

```
[2026-06-04 10:25:00] [ERROR] 无法获取操作锁: .../switch.sw_test01.lock (PID=12345)
[2026-06-04 10:25:00] [ERROR] 可能已有相同ID的操作正在运行
```

---

## 8. 切换执行机制

### 批次执行

当待切换租户较多时，脚本自动按批次执行：

| 参数 | 值 | 说明 |
|------|-----|------|
| 每批次租户数 | 5 | 每批最多切换 5 个租户 |
| 批次内间隔 | 2s | 同一批次内租户之间等待 2 秒 |
| 批次间间隔 | 10s | 两个批次之间等待 10 秒 |
| sys 租户 | 单独批次 | sys 租户始终排到最后一批执行 |

示例：8 个租户（含 sys）的执行时序：

```
批次 1/2: tenant_a, tenant_b, tenant_c, tenant_d, tenant_e  (间隔 2s × 4 = ~8s)
等待 10s...
批次 2/2: tenant_f, tenant_g, sys                            (间隔 2s × 2 = ~4s)
```

### 前置检查（两阶段）

**集群级**（切换前执行）：
- 集群节点状态：所有节点必须 active

**租户级**（仅 V2/V3，筛选租户后执行）：
- 副本完整性、Leader 副本、CLOG 同步、长事务

预检查模式下租户级检查仅警告，不阻断；切换/回切模式下检查不通过则终止。

### 状态文件

| 文件 | 说明 |
|------|------|
| `switch.<id>.state` | 切换成功后生成，记录每个租户的原始 primary_zone |
| `switch.<id>.done` | 回切成功后 .state 归档为 .done |
| `switch.<id>.lock` | 操作锁文件，防止同一 ID 并发执行 |
| `switch.history` | 历史记录，追加写入，记录每次切换/回切的详情 |

### 并发操作

不同 `--id` 的操作可以并行执行，脚本自动检测租户交集，防止同一租户被同时切换：

```bash
# 终端 1: 切换批次 A
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -t tenant1 --switch --id sw_batch_a

# 终端 2: 切换批次 B（tenant1 不能出现在此批次）
./ob_tenant_switch.sh -i 10.0.0.1 -c obtest -t tenant2 --switch --id sw_batch_b
```

---

## 9. 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 数据库连接/查询失败 |
| 3 | 前置检查失败 |
| 4 | 切换执行失败 |

---

## 10. 常见问题

**Q: 切换后多久生效？**

脚本在切换完成后等待 5 秒验证结果。如果验证显示"未生效"，说明 OB 内部 leader 切换尚在进行中，通常再等待片刻即可生效。

**Q: 切换失败后怎么办？**

脚本会在某个租户失败后立即终止，已成功切换的租户不会回滚。可以查看日志确认失败原因，修复后使用 `--switchback` 回切已成功的租户，或手动处理失败的租户。

**Q: 多个操作可以并行吗？**

可以，使用不同的 `--id` 即可并行执行不同租户的切换。脚本会检查租户交集，防止同一租户被同时切换。

**Q: V4 版本有什么区别？**

V4 版本跳过租户级前置检查（副本完整性、Leader、CLOG、长事务），同时查询租户列表时自动排除 `META$%` 开头的租户。

**Q: 日志文件在哪里？**

默认在脚本所在目录的 `ob_switch_logs/` 下。可通过 `-l <log_dir>` 指定其他目录。
