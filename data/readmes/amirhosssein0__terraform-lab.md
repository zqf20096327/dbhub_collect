<div align="center">

<img src="https://www.vectorlogo.zone/logos/terraformio/terraformio-icon.svg" width="60" alt="Terraform" />
&nbsp;&nbsp;&nbsp;
<img src="https://raw.githubusercontent.com/github/explore/main/topics/azure/azure.png" width="60" alt="Azure" />

# terraform-lab

**Modular Azure Infrastructure as Code with Terraform**

![Terraform](https://img.shields.io/badge/Terraform-1.9+-844FBA?style=flat-square&logo=terraform)
![Azure](https://img.shields.io/badge/Azure-AKS%20%7C%20ACR%20%7C%20PostgreSQL-0078D4?style=flat-square&logo=microsoftazure)
![Remote State](https://img.shields.io/badge/State-Azure%20Storage-blue?style=flat-square)

</div>

---

## What is this?

A modular Terraform project that provisions a complete Azure environment from scratch: networking, a Kubernetes cluster with autoscaling, a container registry, a managed PostgreSQL database, and a Key Vault for secrets — all wired together and using a remote state backend.

The goal of this lab is to demonstrate clean Terraform module design, not a single monolithic `main.tf`.

---

## Architecture

```
                    ┌──────────────────────────────────────────────┐
                    │              Resource Group                  │
                    │                                                │
                    │   ┌────────────┐        ┌──────────────────┐  │
                    │   │   VNet     │        │   Key Vault       │  │
                    │   │  + Subnet  │        │  (postgres secret)│  │
                    │   └─────┬──────┘        └─────────▲─────────┘  │
                    │         │                          │           │
                    │   ┌─────▼──────┐        ┌──────────┴────────┐ │
                    │   │    AKS     │◄───────┤  random_password  │ │
                    │   │ (autoscale │        └──────────┬────────┘ │
                    │   │  1-3 nodes)│                   │          │
                    │   └─────┬──────┘        ┌──────────▼────────┐ │
                    │         │ AcrPull        │   PostgreSQL       │ │
                    │   ┌─────▼──────┐        │  Flexible Server   │ │
                    │   │    ACR     │        └────────────────────┘ │
                    │   └────────────┘                                │
                    └──────────────────────────────────────────────┘

Remote State (Azure Storage) ──── stores terraform.tfstate with locking
```

---

## Modules

| Module | Purpose |
|---|---|
| `modules/resource-group` | Creates the Azure Resource Group |
| `modules/vnet` | Virtual Network + Subnet for AKS |
| `modules/acr` | Azure Container Registry |
| `modules/aks` | AKS cluster with autoscaling node pool (1–3 nodes) |
| `modules/postgresql` | PostgreSQL Flexible Server (burstable tier) |
| `modules/keyvault` | Key Vault storing the generated PostgreSQL password |

Each module is self-contained with its own `main.tf`, `variables.tf`, and `outputs.tf` — designed to be reused across multiple environments (`dev`, `staging`, `prod`) by simply pointing a new `environments/<env>` folder at them with different variable values.

---

## Key Design Decisions

### Autoscaling — how it actually works
The AKS node pool uses `auto_scaling_enabled = true` with `min_count = 1` and `max_count = 3`. Node count is **not** driven directly by CPU/memory usage on existing nodes — it's driven by scheduling pressure:

```
Pod can't be scheduled (insufficient capacity on existing nodes)
  └── Pod stays Pending
        └── Cluster Autoscaler detects the Pending pod
              └── Provisions a new node (up to max_count)
                    └── Pod gets scheduled
```

This pairs with the Horizontal Pod Autoscaler (HPA) used in `k8s-gitops-lab`: HPA scales **pod count** based on CPU/memory metrics; Cluster Autoscaler scales **node count** when those pods don't fit.

### Secrets are never hardcoded
The PostgreSQL administrator password is generated at apply-time with `random_password` and stored directly in Azure Key Vault — it never appears in `.tfvars`, environment variables, or git history.

```hcl
resource "random_password" "postgres" {
  length  = 20
  special = true
}
```

Additional secrets (API keys, third-party tokens, connection strings) follow the same pattern and scale cleanly with `for_each`:

```hcl
variable "secrets" {
  type      = map(string)
  sensitive = true
}

resource "azurerm_key_vault_secret" "this" {
  for_each     = var.secrets
  name         = each.key
  value        = each.value
  key_vault_id = azurerm_key_vault.this.id
}
```

In a real workload, AKS pods would read these via the **Key Vault CSI Driver** — the Azure-native equivalent of the Vault Agent Injector pattern used in [`vault-cicd-lab`](https://github.com/amirhosssein0/vault-cicd-lab).

### Remote State with Locking
State is stored in an Azure Storage Account (`azurerm` backend) instead of locally, with automatic locking to prevent concurrent writes — the same pattern used in real team environments.

---

## Region Strategy

This project's infrastructure spans multiple Azure regions due to **subscription-level restrictions** on a free-tier account — not a design choice:

| Resource | Region | Reason |
|---|---|---|
| AKS, ACR, VNet, Key Vault, PostgreSQL | **Canada East** | Free-tier subscription allowed the required VM sizes and had no PostgreSQL offer restrictions here |
| ~~West Europe~~ / ~~North Europe~~ | — | Hit `LocationIsOfferRestricted` (PostgreSQL) and AKS VM size restrictions on this free subscription |
| Terraform Remote State (Storage Account) | **West Europe** | Created first, before the region constraints above were discovered — intentionally left as-is |

> Keeping remote state in a separate, stable region from the infrastructure it manages is itself a common best practice — state should not depend on the lifecycle of the resources it describes. On a paid subscription these restrictions don't apply, and all resources would typically share one region for lower latency between services.

---

## Multi-Environment Ready

Because every piece of infrastructure is a module, adding a `staging` or `prod` environment doesn't require rewriting anything — only a new `environments/staging/` folder with its own `terraform.tfvars` and the **same backend pattern with a different state key**:

```hcl
# environments/staging/backend.tf
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateamir2026"
    container_name        = "tfstate"
    key                   = "staging.terraform.tfstate"   # only this changes
  }
}
```

```hcl
module "aks" {
  source    = "../../modules/aks"
  min_count = 2          # different scaling per environment
  max_count = 5
  ...
}
```

The module library stays identical — only `terraform.tfvars` and the state `key` change between environments.

---

## Screenshots

### Terraform Plan — AKS Cluster
![Plan AKS](docs/screenshots/plan1.png)

### Terraform Plan — PostgreSQL + VNet + Summary
![Plan Postgres](docs/screenshots/plan2.png)

### Terraform Apply — All Resources Created
![Apply](docs/screenshots/apply.png)

### AKS Cluster — Node Ready
![Nodes](docs/screenshots/nodes.png)

### Azure Portal — All Provisioned Resources
![Resources](docs/screenshots/resources.png)

---

## How to Run

### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.9.0
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- An Azure subscription

### 1. Login to Azure

```bash
az login
```

### 2. Create the remote state backend (one-time setup)

```bash
az group create --name terraform-state-rg --location westeurope

az storage account create \
  --name <your-unique-storage-name> \
  --resource-group terraform-state-rg \
  --sku Standard_LRS \
  --encryption-services blob

az storage container create \
  --name tfstate \
  --account-name <your-unique-storage-name>
```

Update `environments/dev/backend.tf` with your storage account name.

### 3. Initialize and plan

```bash
cd environments/dev
terraform init
terraform plan
```

### 4. Apply

```bash
terraform apply
```

### 5. Connect to the cluster

```bash
az aks get-credentials \
  --resource-group terraform-lab-dev-rg \
  --name terraform-lab-dev-aks

kubectl get nodes
```

### 6. Destroy when done (avoid unnecessary cost)

```bash
terraform destroy
```

---

## Repository Structure

```
terraform-lab/
├── modules/
│   ├── resource-group/
│   ├── vnet/
│   ├── acr/
│   ├── aks/
│   ├── postgresql/
│   └── keyvault/
├── environments/
│   └── dev/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── providers.tf
│       ├── backend.tf
│       └── terraform.tfvars
└── docs/
    └── screenshots/
```

---

<div align="center">
<sub>Part of a DevOps portfolio — <a href="https://github.com/amirhosssein0/k8s-gitops-lab">k8s-gitops-lab</a> | <a href="https://github.com/amirhosssein0/vault-cicd-lab">vault-cicd-lab</a></sub>
</div>