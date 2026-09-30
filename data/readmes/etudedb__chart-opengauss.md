# openGauss Chart 由 Etudedb 打包

## 简介

该 Helm Chart 使用 [Helm](https://helm.sh) 包管理器在 [Kubernetes](https://kubernetes.io) 集群上部署独立的 [openGauss](https://opengauss.org/zh/)。

## 准备工作

- Kubernetes 1.19+
- Helm 3.2.0+

## 安装 Chart

使用 release 名称 `my-opengauss` 安装 Chart:

```console
helm install my-opengauss oci://registry-1.docker.io/etudedb/opengauss
```

这将使用默认配置在 Kubernetes 集群中部署 openGauss。可以在 [参数](#参数) 部分找到可配置的参数列表。

> **提示**: 使用 `helm list` 查看所有发布版本

## 卸载 Chart

要删除 `my-opengauss` 部署:

```console
helm delete my-opengauss
```

该命令将删除 chart 相关的所有 Kubernetes 组件并删除该 release。

## 参数

### 常用参数

| 名称                                | 描述                                                                                         | 默认值           |
| ----------------------------------- | --------------------------------------------------------------------------------------------| ---------------- |
| `nameOverride`                     | 部分覆盖 common.names.fullname 模板的字符串(将保留 release 名称)                                | `""`             |
| `fullnameOverride`                 | 完全覆盖 common.names.fullname 模板的字符串                                                    | `""`             |
| `clusterDomain`                    | 集群域名                                                                                      | `cluster.local`  |
| `commonAnnotations`                | 添加到所有 openGauss 资源的公共注解(不考虑子图)。作为模板评估。                                      | `{}`             |
| `image.registry`                  | openGauss 镜像仓库                                                                  | `""`                  |
| `image.repository`                | openGauss 镜像名称                                                                  | `""`                  |
| `image.tag`                       | openGauss 镜像标签(推荐不可变标签)                                                   | `""`                  |
| `image.pullPolicy`                | openGauss 镜像拉取策略                                                               | `IfNotPresent`         |
| `imagePullSecrets`               | openGauss 镜像拉取 secrets 名称数组                                                       | `[]`                   |
| `RootPassword`                     | 管理员 gaussdb 用户密码。                                                                      | `[]`             |

### openGauss 主节点参数  

| 名称                                          | 描述                                                                                    | 默认值               |
| --------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------- |
| `affinity`                 | openGauss 主 Pod 分配的亲和性设置                                                                     | `{}`                 |
| `nodeSelector`             | openGauss 主 Pod 分配的节点标签                                                                       | `{}`                 |
| `tolerations`              | openGauss 主 Pod 分配的容忍设置                                                                       | `[]`                 |
| `podSecurityContext`       | 为 openGauss 主 Pod 启用安全上下文                                                                | `true`               |
| `podSecurityContext.fsGroup`          | 安装卷文件系统的组 ID                                                                  | `1001`               |
| `SecurityContext`                   | openGauss 主容器的安全上下文                                                              | `true`               |
| `SecurityContext.runAsUser`          | openGauss 主容器的用户 ID                                                                 | `1001`               |
| `SecurityContext.runAsNonRoot`        | 将openGauss 主容器的SecurityContext.runAsNonRoot设置为true                              | `true`               |
| `resources.limits`                    | openGauss 主容器的资源限制                                                                | `{}`                 |
| `resources.requests`                  | openGauss 主容器的资源请求                                                                | `{}`                 |
| `livenessProbe.enabled`               | 是否启用存活探针                                                                       | `true`               |
| `livenessProbe.initialDelaySeconds`   | 存活探针的初始延迟时间                                                                 | `5`                 | 
| `livenessProbe.periodSeconds`         | 存活探针的探测周期                                                                      | `10`                 |
| `livenessProbe.timeoutSeconds`        | 存活探针的超时时间                                                                    | `1`                  |
| `livenessProbe.failureThreshold`      | 存活探针的失败阈值                                                                    | `3`                  |
| `livenessProbe.successThreshold`      | 存活探针的成功阈值                                                                    | `1`                  |
| `readinessProbe.enabled`              | 是否启用就绪探针                                                                      | `true`               |
| `readinessProbe.initialDelaySeconds`  | 就绪探针的初始延迟时间                                                                 | `5`                  |
| `readinessProbe.periodSeconds`        | 就绪探针的探测周期                                                                     | `10`                 |
| `readinessProbe.timeoutSeconds`       | 就绪探针的超时时间                                                                     | `1`                  |
| `readinessProbe.failureThreshold`     | 就绪探针的失败阈值                                                                    | `3`                  |  
| `readinessProbe.successThreshold`     | 就绪探针的成功阈值                                                                   | `1`                  |
| `customLivenessProbe`                 | 自定义 openGauss 主容器的存活探针                                                       | `{}`                 |
| `customReadinessProbe`                | 自定义 openGauss 主容器的就绪探针                                                       | `{}`                 |
| `persistence.enabled`                 | 是否在 openGauss 主副本上使用 PersistentVolumeClaim 启用持久存储。如果为 false,使用 emptyDir | `true`               |
| `persistence.existingClaim`           | openGauss 主副本的现有 PersistentVolumeClaim 名称                                       | `""`                 |
| `persistence.subPath`                 | 持久存储的子路径名称                                                                  | `""`                 |
| `persistence.storageClass`            | openGauss 主持久卷的存储类                                                              | `""`                 |
| `persistence.annotations`             | openGauss 主持久卷申领的注解                                                             | `{}`                 |
| `persistence.accessModes`             | openGauss 主持久卷的访问模式                                                             | `["ReadWriteOnce"]`  |
| `persistence.size`                    | openGauss 主持久卷的大小                                                                | `8Gi`                |
| `persistence.selector`                | 匹配现有持久卷的标签                                                                  | `{}`                 |

### Metrics 参数

| 名称                                            | 描述                                                                       | 默认值                     |
| ----------------------------------------------- |-------------------------------------------------------------------------- | ------------------------- |
| `metrics.enabled`                               | 是否启动prometheus exporter sidecar                                         | `false`                   |
| `metrics.image.registry`                        | exporter镜像仓库(自行定义)                                                   | `""`                      |
| `metrics.image.repository`                      | exporter镜像名称(自行定义)                                                  | `""`                      |
| `metrics.image.tag`                             | exporter镜像标签(自行定义)                                                  | `""`                      |
| `metrics.image.digest`                          | exporter镜像摘要,如 sha256:aa...... 注意如果设置了该参数,会覆盖 tag           | `""`                      |
| `metrics.image.pullPolicy`                      | exporter镜像拉取策略                                                        | `IfNotPresent`            |
| `metrics.image.pullSecrets`                     | exporter镜像拉取secret名称数组                                              | `[]`                      |
| `metrics.SecurityContext.enabled`               | 是否启用metrics容器securityContext                                          | `true`                    |
| `metrics.SecurityContext.runAsUser`             | metrics容器的用户ID                                                         | `1001`                    |
| `metrics.SecurityContext.runAsNonRoot`          | 将metrics容器的SecurityContext.runAsNonRoot设置为true                        | `true`                    |
| `metrics.containerPort`                         | Metrics 容器端口                                                            | `ClusterIP`               |
| `metrics.service.type`                          | Prometheus Exporter的Kubernetes服务类型                                     | `ClusterIP`               |
| `metrics.service.clusterIP`                     | Prometheus Exporter服务的集群IP                                             | `""`                      |
| `metrics.service.port`                          | Prometheus Exporter服务端口                                                 | `9161`                    |
| `metrics.service.annotations`                   | Prometheus Exporter服务注解                                                 | `{}`                      |
| `metrics.resources.limits`                      | exporter容器的资源限制                                                      | `{}`                      |
| `metrics.resources.requests`                    | exporter容器的资源请求                                                      | `{}`                      |
| `metrics.livenessProbe`                         | liveness探针配置                                                           |                           |
| `metrics.readinessProbe`                        | readiness探针配置                                                          |                           |
| `metrics.serviceMonitor.enabled`                | 是否创建用于Prometheus Operator抓取metrics的ServiceMonitor                  | `false`                   |
| `metrics.serviceMonitor.namespace`              | ServiceMonitor资源所在的命名空间                                            | `""`                      | 
| `metrics.serviceMonitor.jobLabel`               | 抓取目标服务的标签名称                                                       | `""`                      |
| `metrics.serviceMonitor.interval`               | 抓取时间间隔                                                                | `30s`                     |
| `metrics.serviceMonitor.scrapeTimeout`          | 抓取超时时间                                                                | `""`                      |
| `metrics.serviceMonitor.relabelings`            | 重标记抓取样本的配置                                                         | `[]`                      |
| `metrics.serviceMonitor.metricRelabelings`      | 重标记指标的配置                                                             | `[]`                      |
| `metrics.serviceMonitor.selector`               | ServiceMonitor的选择器标签                                                  | `{}`                      |
| `metrics.serviceMonitor.honorLabels`            | 为抓取端点添加honorLabels参数                                               | `false`                   |
| `metrics.serviceMonitor.labels`                 | 传递给Prometheus的标签,用于选择ServiceMonitor                               | `{}`                      |
| `metrics.serviceMonitor.annotations`            | ServiceMonitor注解                                                         | `{}`                      |
| `metrics.prometheusRule.enabled`                | 是否创建Prometheus Operator的PrometheusRule(还需metrics.enabled=true和设置rules) | `false`                   |
| `metrics.prometheusRule.namespace`              | PrometheusRule资源所在命名空间(默认为Release命名空间)                        | `""`                      |
| `metrics.prometheusRule.additionalLabels`       | 被Prometheus发现的标签                                                     | `{}`                      |
| `metrics.prometheusRule.rules`                  | Prometheus规则定义                                                         | `[]`                      |


可以使用 `--set key=value[,key=value]` 参数为 `helm install` 指定每个参数。例如:

```console
helm install my-opengauss \
  --set image.tag=v8.1.2.128_ent_x86_64_ctm_pack4 \
    oci://registry-1.docker.io/etudedb/opengauss 
```

或者,可以在安装 chart 时通过 -f 参数提供一个 YAML 文件指定参数值。例如:

```console 
helm install my-opengauss -f values.yaml oci://registry-1.docker.io/etudedb/opengauss
```

> **提示**: 你可以使用默认的 [values.yaml](values.yaml)

## 持久存储

[openGauss](https://www.opengauss.com/) 镜像将数据和配置存储在容器中的 `/var/lib/opengauss/data` 路径。

该 chart 通过在该位置挂载 [Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) 来实现持久存储。默认使用动态 volume 分配。也可以预定义一个 PersistentVolumeClaim 来实现此目的。