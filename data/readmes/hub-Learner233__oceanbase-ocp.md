# OceanBase OCP Ansible Collection

`oceanbase.ocp` 使用 OceanBase Cloud Platform（OCP）的 RESTful Open API 管理 OceanBase 资源。项目采用常用资源专用模块与全接口通用模块的分层方式，运行期只依赖 `ansible-core` 和 Python 标准库。

## 功能

| 模块 | 用途 |
|---|---|
| `ocp_api` | 调用任意 OCP REST 接口，支持原生 query/body、check mode 和异步任务等待 |
| `ocp_info` | 查询 OCP 版本和构建信息 |
| `ocp_cluster_info` | 查询集群及 OBServer 列表 |
| `ocp_cluster` | 幂等创建或删除集群，创建接受官方原生 `definition` |
| `ocp_cluster_action` | 启动、停止、重启集群 |
| `ocp_tenant_info` | 查询指定集群下的租户 |
| `ocp_tenant` | 幂等创建或删除租户 |
| `ocp_host_info` | 查询 OCP 主机和服务状态 |
| `ocp_obproxy_info` | 查询 OBProxy 集群 |
| `ocp_task_info` | 查询、筛选或等待异步任务 |
| `ocp_inspection_info` | 查询巡检任务及风险汇总 |
| `ocp_alarm` | 向 OCP 推送外部告警事件 |
| `ocp_log` callback | 在控制端写入 play/task/result JSON Lines 审计日志 |

所有模块共享 Basic 或 AK/SK 认证、TLS 验证、超时、分页、脱敏日志和结构化错误。AK/SK 按 OCP 官方 HMAC-SHA1 规则签名。

## 安装

```bash
ansible-galaxy collection build
ansible-galaxy collection install oceanbase-ocp-0.1.0.tar.gz
```

开发目录可直接运行：

```bash
python -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest tests/unit -q
```

## 认证

推荐 AK/SK。凭据应存入 Ansible Vault，不要提交真实密码或 SK。

```yaml
ocp_url: https://ocp.example.com:8080
ocp_access_key: "{{ vault_ocp_access_key }}"
ocp_secret_key: "{{ vault_ocp_secret_key }}"
```

也支持 `username`/`password` Basic 认证。所有连接参数可用环境变量：`OCP_URL`、`OCP_USERNAME`、`OCP_PASSWORD`、`OCP_ACCESS_KEY`、`OCP_SECRET_KEY`。

```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - oceanbase.ocp.ocp_info:
        base_url: "{{ ocp_url }}"
        access_key: "{{ ocp_access_key }}"
        secret_key: "{{ ocp_secret_key }}"
      register: ocp
```

## 通用 REST 接口

```yaml
- oceanbase.ocp.ocp_api:
    base_url: "{{ ocp_url }}"
    access_key: "{{ ocp_access_key }}"
    secret_key: "{{ ocp_secret_key }}"
    method: POST
    path: /api/v2/ob/clusters/1/tenants/2/switchover
    body: {}
    wait: true
    wait_timeout: 1200
  register: result
```

因此，专用模块尚未封装的数据库、备份恢复、容灾、监控、SQL 诊断、软件包和系统管理等接口，均可通过同一认证与任务机制调用。`path` 和字段必须以目标 OCP 版本的官方 API 参考为准。

## 创建租户

```yaml
- oceanbase.ocp.ocp_tenant:
    base_url: "{{ ocp_url }}"
    access_key: "{{ ocp_access_key }}"
    secret_key: "{{ ocp_secret_key }}"
    cluster_name: production
    name: app
    definition:
      mode: MYSQL
      primaryZone: zone1
      charset: utf8mb4
      collation: utf8mb4_general_ci
      whitelist: "%"
      rootPassword: "{{ tenant_root_password }}"
      zones:
        - name: zone1
          replicaType: FULL
          resourcePool:
            unitSpecName: S1
            unitCount: 1
    wait: true
  no_log: true
```

`present` 对已存在同名资源不自动更新；更新、扩容、容灾等操作使用 `ocp_api` 显式调用目标版本接口，避免猜测字段或意外变更。

## 日志

模块侧：

```yaml
log_file: /var/log/ansible/ocp-module.jsonl
log_level: INFO
log_request_body: false
```

控制端 `ansible.cfg`：

```ini
[defaults]
callbacks_enabled = oceanbase.ocp.ocp_log

[callback_ocp_log]
log_file = /var/log/ansible/ocp-playbook.jsonl
log_level = INFO
```

不要使用 `print()` 调试模块；使用 Ansible `-vvv`、模块日志或结构化文件日志。详见 `docs/logging.md`。

## 安全与兼容性

- 默认校验 TLS；生产环境不要设置 `validate_certs: false`。
- POST 默认不自动重试，防止重复创建；GET/PUT/DELETE 等幂等方法可重试连接错误及 429/5xx。
- 删除、停止、重启和容灾接口具有高风险，应先运行 `--check` 并核对资源 ID。
- 已在模拟 API 上验证，不代替目标 OCP 版本的端到端测试。
- 详见 `docs/api.md` 和 `docs/compatibility.md`。

## 验证

```bash
.venv/bin/python -m pytest tests/unit -q
.venv/bin/ansible-test sanity --python 3.12
.venv/bin/ansible-galaxy collection build
```

License: GPL-3.0-or-later
