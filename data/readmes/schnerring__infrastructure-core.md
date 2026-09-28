# infrastructure

This project contains the configuration for my cloud infrastructure, for which I use [Terraform](https://www.terraform.io/), an open-source infrastructure-as-code tool.

You can find additional info about some of the code on my blog:

- [Use Terraform to Deploy the Remark42 Commenting System to Kubernetes and Integrate it with a Hugo Website](https://schnerring.net/blog/use-terraform-to-deploy-the-remark42-commenting-system-to-kubernetes-and-integrate-it-with-a-hugo-website/)

## Local Development

### Authentication

[Use the Azure CLI to authenticate to Azure](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/guides/azure_cli) to interactively run Terraform:

```shell
az login
```

For GitHub and Cloudflare, use [personal access tokens (PAT)](https://docs.github.com/en/rest/overview/other-authentication-methods#basic-authentication) and put them into the following environment variables:

- `GITHUB_TOKEN` with `public_repo` scope
- `CLOUDFLARE_API_TOKEN` with `Zone.Zone` and `Zone.DNS` permissions.

### Terraform Input Variables

Terraform input variables to configure the deployment are defined inside the [variables.tf](./variables.tf) file.

Use the `tfinfracorekv37` key vault to store sensitive Terraform variable values. It enhances operational security because storing secrets in plaintext files or environment variables can be avoided. The [map-kv-to-env-vars.ps1](./map-kv-to-env-vars.ps1) convenience script maps the `TF-VAR-*` key vault secrets to `TF_VAR_*` environment variables. The mappings are not persisted and are only available within the PowerShell session that executed the script.

```powershell
.\map-kv-to-env-vars.ps1 -KeyVault tfinfracorekv37
```

To access the key vault, the user requires the following role assignments:

- `Key Vault Administrator` and `Key Vault Secrets Officer` roles to manage secrets
- `Key Vault Secrets User` to read secrets

I like to manage these role assignments with the Azure Portal and not add them to the Terraform state.

### Initialize the Terraform Backend

Initialize the [Terraform azurerm backend](https://www.terraform.io/docs/language/settings/backends/azurerm.html):

```shell
terraform init \
  -backend-config="resource_group_name=terraform-rg" \
  -backend-config="storage_account_name=tfinfracorest37" \
  -backend-config="container_name=terraform-backend" \
  -backend-config="key=infrastructure-core.tfstate"
```

### Deploy

```shell
terraform plan -out infrastructure-core.tfplan
terraform apply infrastructure-core.tfplan
```

### Core

Core infrastructure.

| File                                                  | Description                                                                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`aks.tf`](./core/aks.tf)                             | Azure Kubernetes Service (AKS) cluster resources                                                                                                             |
| [`backup-truenas.tf`](./core/backup-truenas.tf)       | Azure storage account containers used for TrueNAS cloud sync tasks                                                                                           |
| [`backup.tf`](./core/backup.tf)                       | Azure backup vault to protect blob storage for Terraform state                                                                                               |
| [`cloudflare.tf`](./core/cloudflare.tf)               | Common Cloudflare DNS records and Page Rules                                                                                                                 |
| [`terraform-backend.tf`](./core/terraform-backend.tf) | Azure storage configuration for [Terraform Remote State](https://www.terraform.io/docs/language/state/remote.html) and Azure Key Vault for Terraform secrets |
