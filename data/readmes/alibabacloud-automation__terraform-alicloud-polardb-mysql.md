Terraform module which creates polardb MySQL cluster service on Alibaba Cloud

terraform-alicloud-polardb-mysql
=====================================================================

English | [简体中文](README-CN.md)

This module is used to create a polardb MySQL cluster service with `VPC` and `VSwitch` under Alibaba Cloud.

These types of resources are supported:


* [alicloud_polardb_cluster](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_cluster)
* [alicloud_polardb_database](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_database)
* [alicloud_polardb_account](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_account)
* [alicloud_polardb_endpoint](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_endpoint)
* [alicloud_polardb_endpoint_address](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_endpoint_address)
* [alicloud_polardb_account_privilege](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_account_privilege)
* [alicloud_polardb_backup_policy](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_backup_policy)

## Usage

<div style="display: block;margin-bottom: 40px;"><div class="oics-button" style="float: right;position: absolute;margin-bottom: 10px;">
  <a href="https://api.aliyun.com/terraform?source=Module&activeTab=document&sourcePath=terraform-alicloud-modules%3A%3Apolardb-mysql&spm=docs.m.terraform-alicloud-modules.polardb-mysql&intl_lang=EN_US" target="_blank">
    <img alt="Open in AliCloud" src="https://img.alicdn.com/imgextra/i1/O1CN01hjjqXv1uYUlY56FyX_!!6000000006049-55-tps-254-36.svg" style="max-height: 44px; max-width: 100%;">
  </a>
</div></div>

```hcl
module "example" {
  source = "terraform-alicloud-modules/polardb-mysql/alicloud"
  #alicloud_polardb_cluster
  create_cluster              = true
  db_version                  = "8.0"
  pay_type                    = "PostPaid"
  db_node_class               = "polar.mysql.x4.medium"
  polardb_cluster_description = "tf-test"
  modify_type                 = "Upgrade"
  renewal_status              = "Normal"
  tde_status                  = "Disabled"
  parameters = [
    {
      name  = "wait_timeout"
      value = "86"
    }
  ]
  deletion_lock                                       = 0
  imci_switch                                         = "OFF"
  sub_category                                        = "Exclusive"
  creation_category                                   = "Normal"
  hot_standby_cluster                                 = "ON"
  creation_option                                     = "Normal"
  cluster_backup_retention_policy_on_cluster_deletion = "LATEST"
  target_db_revision_version_code                     = "20240314"
  db_node_id                                          = "1"
  hot_replica_mode                                    = "ON"
  default_time_zone                                   = "-4:00"
  lower_case_table_names                              = 1
  db_node_num                                         = 1
  loose_polar_log_bin                                 = "ON"
  planned_end_time                                    = "2024-04-12T13:50:00Z"
  planned_start_time                                  = "2024-04-12T14:10:00Z"
  from_time_service                                   = "false"
  upgrade_type                                        = "ALL"
  #alicloud_polardb_database
  create_database = true
  db_name         = "tf-dbname"
  #alicloud_polardb_account
  create_account   = true
  account_name     = "tf_test123"
  account_password = "tf_test123"
  account_type     = "Normal"
  #alicloud_polardb_endpoint
  create_endpoint            = true
  endpoint_type              = "Custom"
  read_write_mode            = "ReadOnly"
  auto_add_new_nodes         = "Enable"
  net_type                   = "Private"
  endpoint_connection_prefix = "endpointprivateprefix"
  db_endpoint_description    = "test01"
  endpoint_port              = "3308"
  #alicloud_polardb_endpoint_address
  create_endpoint_address = true
  connection_prefix       = "testpolardbconn"
  account_privilege       = "ReadOnly"
  endpoint_address_port   = "3306"
  #alicloud_polardb_account_privilege
  create_account_privilege = true
  #alicloud_polardb_backup_policy
  create_backup_policy                               = true
  preferred_backup_period                            = ["Tuesday", "Saturday"]
  preferred_backup_time                              = "02:00Z-03:00Z"
  data_level1_backup_retention_period                = "7"
  data_level2_backup_retention_period                = "60"
  backup_retention_policy_on_cluster_deletion        = "LATEST"
  backup_frequency                                   = "Normal"
  data_level1_backup_frequency                       = "Normal"
  data_level1_backup_time                            = "02:00Z-03:00Z"
  data_level1_backup_period                          = ["Tuesday", "Saturday"]
  data_level2_backup_period                          = ["Tuesday", "Saturday"]
  log_backup_retention_period                        = "7"
  data_level2_backup_another_region_region           = "cn-hangzhou"
  data_level2_backup_another_region_retention_period = "30"
  log_backup_another_region_region                   = "cn-hangzhou"
  log_backup_another_region_retention_period         = "30"
  #alicloud_polardb_cluster_endpoint
  create_cluster_endpoint                    = true
  cluster_endpoint_private_connection_prefix = "polardbmysqlprivateprefix"
  cluster_endpoint_private_port              = "5432"
  cluster_endpoint_description               = "test_cluster_endpoint"
  cluster_endpoint_nodes                     = []
  cluster_endpoint_read_write_mode           = "ReadWrite"
  cluster_endpoint_auto_add_new_nodes        = "Enable"
  cluster_endpoint_config                    = {}
  cluster_endpoint_ssl_enabled               = "Disable"
  cluster_endpoint_net_type                  = "Private"
  cluster_endpoint_ssl_auto_rotate           = "Disable"
  #alicloud_polardb_cluster_endpoint_address
  create_cluster_endpoint_address           = true
  cluster_endpoint_public_connection_prefix = "polardbmysqlpublicprefix"
  cluster_endpoint_public_port              = "3999"
  #alicloud_polardb_global_database_network
  create_global_database_network      = true
  global_database_network_description = "test01"
  #alicloud_polardb_parameter_group
  create_parameter_group      = true
  parameter_group_name        = "test_group"
  db_type                     = "MySQL"
  parameter_group_db_version  = "8.0"
  parameter_group_parameters  = {
    name = "wait_timeout"
    value = "86"
  }
  parameter_group_description = "test01"
  #alicloud_polardb_primary_endpoint
  create_primary_endpoint            = true
  primary_endpoint_ssl_enabled       = "Disable"
  primary_endpoint_net_type          = "Public"
  primary_endpoint_ssl_auto_rotate   = "Disable"
  primary_endpoint_description       = "test01"
  primary_endpoint_connection_prefix = "testpolardbconn110"
  primary_endpoint_port              = "3307"
}
```

## Examples

* [complete example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/complete)
* [clone-from-polardb example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/clone-from-polardb)
* [clone-from-rds example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/clone-from-rds)
* [migration-from-rds example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/migration-from-rds)
* [multimaster-polardb example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/multimaster-polardb)
* [se-normal-polardb example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/se-normal-polardb)
* [serverless-polardb example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/serverless-polardb)
* [steady-serverless-polardb example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/steady-serverless-polardb)
* [cluster-endpoint example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/cluster-endpoint)
* [global-database-network-and-parameter-group example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/global-database-network-and-parameter-group)
* [primary-endpoint example](https://github.com/terraform-alicloud-modules/terraform-alicloud-polardb-mysql/tree/main/examples/primary-endpoint)
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
