Terraform Module for creating PolarDB for PostgreSQL on Alibaba Cloud.


terraform-alicloud-polardb-postgresql
=====================================================================

English | [简体中文](README-CN.md)

This module is used to create a polardb PostgreSQL cluster service with `VPC` and `VSwitch` under Alibaba Cloud.

These types of resources are supported:


* [alicloud_polardb_cluster](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_cluster)
* [alicloud_polardb_endpoint](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_endpoint)
* [alicloud_polardb_endpoint_address](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_endpoint_address)
* [alicloud_polardb_account](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_account)
* [alicloud_polardb_backup_policy](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_backup_policy)
* [alicloud_polardb_cluster_endpoint](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_cluster_endpoint)
* [alicloud_polardb_primary_endpoint](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_primary_endpoint)

## Usage

<div style="display: block;margin-bottom: 40px;"><div class="oics-button" style="float: right;position: absolute;margin-bottom: 10px;">
  <a href="https://api.aliyun.com/terraform?source=Module&activeTab=document&sourcePath=terraform-alicloud-modules%3A%3Apolardb-postgresql&spm=docs.m.terraform-alicloud-modules.polardb-postgresql&intl_lang=EN_US" target="_blank">
    <img alt="Open in AliCloud" src="https://img.alicdn.com/imgextra/i1/O1CN01hjjqXv1uYUlY56FyX_!!6000000006049-55-tps-254-36.svg" style="max-height: 44px; max-width: 100%;">
  </a>
</div></div>

```hcl
module "example" {
  source                        = "terraform-alicloud-modules/polardb-postgresql/alicloud"
  #alicloud_polardb_cluster
  create_cluster                = true
  pay_type                      = "PostPaid"
  db_node_class                 = "polar.pg.x8.xlarge"
  polardb_cluster_description   = "tf-test"
  modify_type                   = "Upgrade"
  renewal_status                = "Normal"
  tde_status                    = "Disabled"
  #alicloud_polardb_endpoint
  create_endpoint               = true
  endpoint_type                 = "Custom"
  read_write_mode               = "ReadOnly"
  auto_add_new_nodes            = "Enable"
  net_type                      = "Public"
  #alicloud_polardb_endpoint_address
  create_endpoint_address       = true
  connection_prefix             = "testpolardbconn"
}
```

## Examples

* [complete example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-postgresql/tree/main/examples/complete)

## Notes

* This module using AccessKey and SecretKey are from `profile` and `shared_credentials_file`. If you have not set them
  yet, please install [aliyun-cli](https://github.com/aliyun/aliyun-cli#installation) and configure it.

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | > = 0.13.0 |
| <a name="requirement_alicloud"></a> [alicloud](#requirement\_alicloud) | > = 1.130.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_alicloud"></a> [alicloud](#provider\_alicloud) | > = 1.130.0 |

## Submit Issues

If you have any problems when using this module, please opening
a [provider issue](https://github.com/aliyun/terraform-provider-alicloud/issues/new) and let us know.

**Note:** There does not recommend opening an issue on this repo.

## Authors

Created and maintained by Alibaba Cloud Terraform Team(terraform@alibabacloud.com).

## License

MIT Licensed. See LICENSE for full details.

## Reference

* [Terraform-Provider-Alicloud Github](https://github.com/aliyun/terraform-provider-alicloud)
* [Terraform-Provider-Alicloud Release](https://releases.hashicorp.com/terraform-provider-alicloud/)
* [Terraform-Provider-Alicloud Docs](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs)
