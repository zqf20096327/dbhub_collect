# tidb_work

1、构建镜像：
docker build -t worker:1.0

2、安装istio然后：
修改istio-sidecar-injector configmap：
apiVersion: v1
kind: ConfigMap
metadata:
name: istio-sidecar-injector
namespace: istio-system
data:
config: |-
    policy: enabled 
...
values: |- 下面
"hub": "docker.mirrors.ustc.edu.cn/istio",
"image": "worker:1.0", 
"tag": "1.5.4",

3、为需要自动注入的 namespace 打上标签 istio-injection: enabled（ns级别注入）：
kubectl label namespace default istio-injection=enabled

4、同时也可以在 deployment 中通过设置 annotation，sidecar.istio.io/inject=true 来控制 pod 级别的自动注入：
用户侧配置如下配置：
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
name: test
spec:
replicas: 1
template:
metadata:
annotations:
sidecar.istio.io/inject: “true”

5、定义 webhook 参数文件 MutatingWebhookConfiguration：
apiVersion: admissionregistration.k8s.io/v1beta1
kind: MutatingWebhookConfiguration
metadata:
  name: istio-sidecar-injector
 namespace: {{ .Release.Namespace }}
labels:
 app: istio-sidecar-injector
webhooks:
- name: sidecar-injector.istio.io
  clientConfig:
service:
  name: istio-sidecar-injector
namespace: {{ .Release.Namespace }}
  path: "/inject"
 caBundle: ""
rules:
- operations: [ "CREATE" ]
apiGroups: [""]
apiVersions: ["v1"]
resources: ["pods"]
failurePolicy: Fail
namespaceSelector:
matchLabels:
istio-injection: enabled

