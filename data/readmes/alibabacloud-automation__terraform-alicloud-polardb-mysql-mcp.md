Alicloud PolarDB MySQL MCP Terraform Module

# terraform-alicloud-polardb-mysql-mcp

English | [简体中文](https://github.com/alibabacloud-automation/terraform-alicloud-polardb-mysql-mcp/blob/main/README-CN.md)

Terraform module which creates a comprehensive PolarDB MySQL solution for MCP (Model Context Protocol) empowered visual OLAP intelligent agent applications on Alibaba Cloud. This module implements the infrastructure requirements for [MCP empowers visual OLAP intelligent agent applications](https://www.aliyun.com/solution/tech-solution/polardb-mysql-mcp), providing a complete database environment with VPC network isolation, PolarDB cluster setup, account management, and public endpoint configuration.

## Usage

This module creates a complete PolarDB MySQL environment suitable for MCP-enabled applications, including VPC, VSwitch, PolarDB cluster with public endpoint, database account, and application database.

```terraform
module "polardb_mysql_mcp" {
  source = "alibabacloud-automation/polardb-mysql-mcp/alicloud"

  vpc_config = {
    cidr_block = "192.168.0.0/16"
  }

  vswitch_config = {
    cidr_block = "192.168.0.0/24"
    zone_id    = "cn-hangzhou-i"
  }

  polardb_config = {
    db_node_class = "polar.mysql.g1.large.c"
    storage_space = 100
    security_ips  = ["192.168.1.0/24"]
  }

  account_config = {
    account_name = "mcp_user"
  }

  account_password = "YourSecurePassword123!"

  database_config = {
    db_name = "mcp_database"
  }
}
```

## Examples

* [Complete Example](https://github.com/alibabacloud-automation/terraform-alicloud-polardb-mysql-mcp/tree/main/examples/complete)

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_alicloud"></a> [alicloud](#requirement\_alicloud) | >= 1.120.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_alicloud"></a> [alicloud](#provider\_alicloud) | >= 1.120.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [alicloud_polardb_account.account](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_account) | resource |
| [alicloud_polardb_cluster.polardb_cluster](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_cluster) | resource |
| [alicloud_polardb_database.polardb_database](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_database) | resource |
| [alicloud_vpc.vpc](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/vpc) | resource |
| [alicloud_vswitch.vswitch](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/vswitch) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_account_config"></a> [account\_config](#input\_account\_config) | Configuration for PolarDB account. The attributes 'account\_name' and 'account\_type' are required. | <pre>object({<br/>    account_name = string<br/>    account_type = optional(string, "Super")<br/>  })</pre> | <pre>{<br/>  "account_name": "polar_admin",<br/>  "account_type": "Super"<br/>}</pre> | no |
| <a name="input_account_password"></a> [account\_password](#input\_account\_password) | Password for PolarDB account. | `string` | `null` | no |
| <a name="input_database_config"></a> [database\_config](#input\_database\_config) | Configuration for PolarDB database. The attributes 'db\_name' and 'character\_set\_name' are required. | <pre>object({<br/>    db_name            = string<br/>    character_set_name = optional(string, "utf8")<br/>  })</pre> | <pre>{<br/>  "character_set_name": "utf8",<br/>  "db_name": "default_db"<br/>}</pre> | no |
| <a name="input_polardb_config"></a> [polardb\_config](#input\_polardb\_config) | Configuration for PolarDB cluster. The attributes 'db\_type', 'db\_version', 'creation\_category', 'storage\_space', 'db\_node\_class', 'pay\_type', 'storage\_type' are required. | <pre>object({<br/>    db_type           = string<br/>    db_version        = string<br/>    creation_category = string<br/>    storage_space     = number<br/>    db_node_class     = string<br/>    pay_type          = string<br/>    storage_type      = string<br/>    security_ips      = optional(list(string), ["127.0.0.1", "0.0.0.0/0"])<br/>    description       = optional(string, "PolarDB MySQL cluster")<br/>  })</pre> | <pre>{<br/>  "creation_category": "SENormal",<br/>  "db_node_class": "polar.mysql.g1.tiny.c",<br/>  "db_type": "MySQL",<br/>  "db_version": "8.0",<br/>  "pay_type": "PostPaid",<br/>  "storage_space": 40,<br/>  "storage_type": "ESSDAUTOPL"<br/>}</pre> | no |
| <a name="input_vpc_config"></a> [vpc\_config](#input\_vpc\_config) | Configuration for VPC. The attribute 'cidr\_block' is required. | <pre>object({<br/>    cidr_block = string<br/>    vpc_name   = optional(string, "default-vpc")<br/>  })</pre> | <pre>{<br/>  "cidr_block": null<br/>}</pre> | no |
| <a name="input_vswitch_config"></a> [vswitch\_config](#input\_vswitch\_config) | Configuration for VSwitch. The attributes 'cidr\_block' and 'zone\_id' are required. | <pre>object({<br/>    cidr_block   = string<br/>    zone_id      = string<br/>    vswitch_name = optional(string, "default-vswitch")<br/>  })</pre> | <pre>{<br/>  "cidr_block": null,<br/>  "zone_id": null<br/>}</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_polardb_account_name"></a> [polardb\_account\_name](#output\_polardb\_account\_name) | The name of the PolarDB account |
| <a name="output_polardb_cluster_connection_string"></a> [polardb\_cluster\_connection\_string](#output\_polardb\_cluster\_connection\_string) | The connection string of the PolarDB cluster |
| <a name="output_polardb_cluster_id"></a> [polardb\_cluster\_id](#output\_polardb\_cluster\_id) | The ID of the PolarDB cluster |
| <a name="output_polardb_cluster_port"></a> [polardb\_cluster\_port](#output\_polardb\_cluster\_port) | The port of the PolarDB cluster |
| <a name="output_polardb_database_character_set"></a> [polardb\_database\_character\_set](#output\_polardb\_database\_character\_set) | The character set of the PolarDB database |
| <a name="output_polardb_database_name"></a> [polardb\_database\_name](#output\_polardb\_database\_name) | The name of the PolarDB database |
| <a name="output_vpc_cidr_block"></a> [vpc\_cidr\_block](#output\_vpc\_cidr\_block) | The CIDR block of the VPC |
| <a name="output_vpc_id"></a> [vpc\_id](#output\_vpc\_id) | The ID of the VPC |
| <a name="output_vswitch_id"></a> [vswitch\_id](#output\_vswitch\_id) | The ID of the VSwitch |
| <a name="output_vswitch_zone_id"></a> [vswitch\_zone\_id](#output\_vswitch\_zone\_id) | The zone ID of the VSwitch |
<!-- END_TF_DOCS -->

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