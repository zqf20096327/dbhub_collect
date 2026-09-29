# terraform-tici

A sample to create VMs for deploying TiDB with TiCI in AWS using [Terraform](https://www.terraform.io) with these default topology:

| Usage                                       | Size   | Count | Private IP                  |
| ------------------------------------------- | ------ | ----- | --------------------------- |
| TiKV                                        | 8c 64g | 1     | 172.31.6.1, 172.31.6.2, ... |
| TiDB                                        | 8c 16g | 1     | 172.31.7.1, 172.31.7.2, ... |
| PD + Grafana + Monitoring                   | 8c 16g | 1     | 172.31.8.1                  |
| TiFlash                                     | 8c 64g | 1     | 172.31.9.1, 172.31.9.2, ... |
| TiCI-Meta                                   | 8c 16g | 1     | 172.31.10.1                 |
| TiCI-Worker                                 | 8c 16g | 1     | 172.31.11.1                 |
| Center VM, you can run benchmarks and so on | 8c 16g | 1     | 172.31.1.1                  |

The topology and instance size can be customized via [`locals_common.tf`](./locals_common.tf) and [`locals_advanced.tf`](./locals_advanced.tf).

## Prerequisite

- [Terraform](https://www.terraform.io) must be installed.

- `~/.ssh/id_rsa.pub` must present, can be used as the public key to access VMs.

## Getting Started

### 1. Clone and create project

```shell
git clone https://github.com/Lloyd-Pottiger/terraform-tici.git
cd terraform-tici

# Generate a master key for intra cluter access (no password)
ssh-keygen -t rsa -b 4096 -f ./master_key -q -N ""

# Load terraform modules
terraform init
```

### 2. Optional: Configure

Customize the number of TiDB and TiKV VMs in [`locals_common.tf`](./locals_common.tf).

**Example:**

```terraform
locals {
  name      = "foo-benchmark"
  n_tidb    = 1     # default 1
  n_tikv    = 1     # default 1
  n_tiflash = 1     # default 1
  n_cdc     = 1     # default 1
  n_tici_meta = 1   # default 1
  n_tici_worker = 1 # default 1
}
```

### 3. Create and start VMs

```shell
terraform apply -auto-approve
```

Terraform will output like this, which contains information you need to connect to VMs:

```plain
cdc_private_ips = [
  "172.31.12.1",
]
private-ip-pd = "172.31.8.1"
private-ip-tidb = [
  "172.31.7.1",
]
private-ip-tiflash = [
  "172.31.9.1",
]
private-ip-tikv = [
  "172.31.6.1",
]
public-DSN = "mysql://root@<center_vm_ip>:4000"
ssh-center = "ssh ubuntu@<center_vm_ip>"
tici_meta_private_ips = [
  "172.31.10.1",
]
tici_worker_private_ips = [
  "172.31.11.1",
]
url-tidb-dashboard = "http://<pd_vm_ip>:2379/dashboard"
```

### 4. Connect to Center VM and deploy cluster

You can now connect to the center VM and deploy a TiDB cluster in these VMs:

```shell
# ssh to the host
`terraform output -raw ssh-center`

tiup mirror set https://staging.tiup-server.pingcap.net 

# The topology.yaml is already created for you
tiup cluster:v1.16.2-feature.fts deploy tidb-test nightly ./topology.yaml --user ubuntu -i ~/.ssh/id_rsa --yes
tiup cluster start tidb-test
```

### 5. Connect to TiDB

A HAProxy is deployed in the Center VM, load balancing multiple TiDB instances:

```shell
# ssh to the host
`terraform output -raw ssh-center`

mysql -u root --host 127.0.0.1 --port 4000
```

### 6. Finally, destroy VMs

When everything is done, you can destroy all of your VMs and resources with one line:

```shell
terraform destroy -auto-approve
```

## Features

| Status | Feature                                     |
| ------ | ------------------------------------------- |
| ✅     | Ubuntu 22.04 (x86_64)                       |
| ✅     | Intra-host public key authentication        |
| ✅     | HAProxy for multiple TiDB instances         |
| ✅     | Expose PD and Grafana for public access     |
| ✅     | Customize instance count and size           |
| ✅     | Enable core dump                            |
| ✅     | With zsh                                    |
| ✅     | TiDB recommended kernal parameters          |
| ✅     | Instance size is identical with TiDB Cloud  |
| ✅     | EC2 IAM Profile to access S3 without AK, SK |
