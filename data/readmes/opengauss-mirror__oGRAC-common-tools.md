# oGRAC-common-tools

oGRAC 定制适配工具管理仓库。

## 工具清单

### ograc-docs-review

oGRAC 中文文档低级错误检视与修复 skill。

- 作用：自动扫描 `docs/zh/` 下 Markdown（含 `_toc.yaml`），按规则修复错别字、产品命名不一致、中英文混排空格、行内代码缺失、SQL 关键字大小写、Markdown 格式、口语化表述、Shell 代码块可复制性、弯引号等。
- 触发：在 OpenCode 中处理「检视/审校/修复/规范化 docs/zh 文档」「文档低级错误」「文档格式检查」「清理口语化」「PR 文档自检」「同步官方文档前批量检查」或任何涉及 oGRAC 中文文档质量批处理的任务时，agent 会自动加载本 skill。
- 使用：将 `ograc-docs-review/` 目录复制到 `.opencode/skills/ograc-docs-review/` 或 `.agents/skills/ograc-docs-review/` 下即可生效。
- 规则文件：`ograc-docs-review/references/ograc_rules.json`

### ograc_sim_single

单文件创建 oGRAC 单集群 LUN 开发环境（4 个 LUN，每个 LUN 两条 loopback 路径）。

- 作用：在 Docker 容器内启动双节点主集群，支持 `status`、`verify`、SQL 登录、重启和清理等常用操作。
- 特点：脚本内嵌 Dockerfile 与 CMS `cluster.sh`，不依赖 `docker/lun-sim/` 下的其他文件；复制到 oGRAC 源码树任意目录即可运行。
- 位置：`common-scripts/ograc_sim_single.sh`

前置条件：

- 宿主机安装 Docker，并支持 LIO/configfs、`tcm_loop`、`sg3_utils`。
- oGRAC 源码树包含 `build/build_ograc.sh`；编译时还需三方库，默认搜索源码根目录及 `third_party/`，也可设置 `THIRD_PARTY_PATH`。
- `install` 需要 `package/oGRAC-*.tgz` 部署包；如果已有合适部署包，可跳过 `make`。

使用：

```bash
cp common-scripts/ograc_sim_single.sh /path/to/oGRAC/
cd /path/to/oGRAC

sudo bash ./ograc_sim_single.sh create         # 创建 LUN、镜像和容器
sudo bash ./ograc_sim_single.sh init           # 安装容器内编译依赖
sudo bash ./ograc_sim_single.sh make debug     # 编译（已有部署包时可跳过）
sudo bash ./ograc_sim_single.sh install debug  # 安装双节点
sudo bash ./ograc_sim_single.sh start
sudo bash ./ograc_sim_single.sh verify
```

常用命令：

```bash
sudo bash ./ograc_sim_single.sh status
sudo bash ./ograc_sim_single.sh sql 0 "SELECT OPEN_STATUS FROM DV_DATABASE;"
sudo bash ./ograc_sim_single.sh login 0
sudo bash ./ograc_sim_single.sh stop
sudo bash ./ograc_sim_single.sh restart
sudo bash ./ograc_sim_single.sh log 100
sudo bash ./ograc_sim_single.sh destroy
```

默认环境目录为 `/home/<用户>/ogracsim_single/cluster`，容器名为 `ograc-dev-<用户>`，默认端口为 CMS `18520/18521`、DSS `19100/19101`、oGRAC `19300/19301`。

### security-developing-skills

安全研发技能归档。

- 作用：存放可复用的安全研发技能。当前包含：
  - `opengauss-secret-scan`：扫描 openGauss 公开主仓历史提交中的 AK/SK、GitCode/Gitee access_token、OBS 访问密钥和大模型 API Key，并只读核验是否仍有效。说明见 `security-developing-skills/opengauss-secret-scan/README.md`。
  - `opengauss-third-party-cve`：给定 openGauss-third_party 仓库和 issue，排查 master、7.0.0、6.0.0，修复受影响分支并编译验证，只在本地 bugfix 分支提交。用法见 `security-developing-skills/opengauss-third-party-cve/README.md`。
- 使用：将对应技能目录复制到 Cursor、OpenCode 或 `~/.codex/skills/` 后，按该目录里的 `SKILL.md` 运行。
- 注意：secret-scan 的报告含密钥原文，只留本地，不要提交进 git。

## 许可证

MulanPSL-2.0
