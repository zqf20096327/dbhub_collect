Alibaba Cloud PolarDB AI Search Terraform Module

================================================ 

# terraform-alicloud-polardb-ai-search

English | [简体中文](https://github.com/alibabacloud-automation/terraform-alicloud-polardb-ai-search/blob/main/README-CN.md)

This Terraform module creates a complete infrastructure for implementing AI-powered multimodal intelligent search capabilities using PolarDB for PostgreSQL. The module implements the solution architecture described in [Native SQL enables effortless multimodal intelligent search](https://www.aliyun.com/solution/tech-solution/polardb-ai-search), involving the deployment of Virtual Private Cloud (VPC), Virtual Switch (VSwitch), PolarDB Database (PolarDB), and Object Storage Service (OSS) resources.

## Usage

To use this module, you need to provide the basic network configuration and database credentials. The module will create all necessary resources for a PolarDB AI search solution.

```terraform
data "alicloud_polardb_node_classes" "default" {
  db_type  = "PostgreSQL"
  pay_type = "PostPaid"
  category = "SENormal"
}

data "alicloud_polardb_endpoints" "default" {
  db_cluster_id = module.polardb_ai_search.polardb_cluster_id
}

module "polardb_ai_search" {
  source = "alibabacloud-automation/polardb-ai-search/alicloud"

  # VPC configuration
  vpc_config = {
    cidr_block = "192.168.0.0/16"
  }

  # VSwitch configuration
  vswitch_config = {
    cidr_block = "192.168.1.0/24"
    zone_id    = data.alicloud_polardb_node_classes.default.classes[0].zone_id
  }

  # PolarDB account configuration
  polardb_account_config = {
    account_name     = "polar_ai"
    account_password = "YourSecurePassword123!"
  }

  # PolarDB endpoint configuration
  polardb_endpoint_config = {
    db_endpoint_id = data.alicloud_polardb_endpoints.default.endpoints[0].db_endpoint_id
  }

  # PolarDB database configuration
  polardb_database_config = {
    db_name = "ai_search_db"
  }

  # OSS bucket configuration
  oss_bucket_config = {
    bucket_name = "polardb-ai-search-bucket"
  }
}
```

## Examples

* [Complete Example](https://github.com/alibabacloud-automation/terraform-alicloud-polardb-ai-search/tree/main/examples/complete)

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_alicloud"></a> [alicloud](#requirement\_alicloud) | >= 1.200.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_alicloud"></a> [alicloud](#provider\_alicloud) | >= 1.200.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [alicloud_oss_bucket.bucket](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/oss_bucket) | resource |
| [alicloud_polardb_account.account](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_account) | resource |
| [alicloud_polardb_cluster.polardb_cluster](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_cluster) | resource |
| [alicloud_polardb_database.database](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_database) | resource |
| [alicloud_polardb_endpoint_address.endpoint_address](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/polardb_endpoint_address) | resource |
| [alicloud_vpc.vpc](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/vpc) | resource |
| [alicloud_vswitch.vswitch](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/vswitch) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_common_tags"></a> [common\_tags](#input\_common\_tags) | Common tags to be applied to all resources. | `map(string)` | `{}` | no |
| <a name="input_oss_bucket_config"></a> [oss\_bucket\_config](#input\_oss\_bucket\_config) | Configuration for OSS bucket. The 'bucket\_name' attribute is required. | <pre>object({<br/>    bucket_name     = string<br/>    force_destroy   = optional(bool, true)<br/>    redundancy_type = optional(string, "ZRS")<br/>    storage_class   = optional(string, "Standard")<br/>  })</pre> | n/a | yes |
| <a name="input_polardb_account_config"></a> [polardb\_account\_config](#input\_polardb\_account\_config) | Configuration for PolarDB account. The 'account\_name' and 'account\_password' attributes are required. | <pre>object({<br/>    account_name     = string<br/>    account_password = string<br/>    account_type     = optional(string, "Super")<br/>  })</pre> | n/a | yes |
| <a name="input_polardb_cluster_config"></a> [polardb\_cluster\_config](#input\_polardb\_cluster\_config) | Configuration for PolarDB cluster. All attributes have sensible defaults. | <pre>object({<br/>    db_type             = optional(string, "PostgreSQL")<br/>    db_version          = optional(string, "14")<br/>    creation_category   = optional(string, "SENormal")<br/>    storage_space       = optional(number, 20)<br/>    hot_standby_cluster = optional(string, "OFF")<br/>    db_node_class       = optional(string, "polar.pg.g2.2xlarge.c")<br/>    pay_type            = optional(string, "PostPaid")<br/>    storage_type        = optional(string, "ESSDPL1")<br/>    security_ips        = optional(list(string), ["127.0.0.1", "0.0.0.0/0"])<br/>    db_node_num         = optional(number, 2)<br/>    description         = optional(string, "PolarDB cluster for AI search")<br/>  })</pre> | `{}` | no |
| <a name="input_polardb_database_config"></a> [polardb\_database\_config](#input\_polardb\_database\_config) | Configuration for PolarDB database. The 'db\_name' attribute is required. | <pre>object({<br/>    db_name = string<br/>  })</pre> | n/a | yes |
| <a name="input_polardb_endpoint_config"></a> [polardb\_endpoint\_config](#input\_polardb\_endpoint\_config) | Configuration for PolarDB endpoint address. The 'db\_endpoint\_id' attribute is required. | <pre>object({<br/>    db_endpoint_id = string<br/>    net_type       = optional(string, "Public")<br/>  })</pre> | n/a | yes |
| <a name="input_vpc_config"></a> [vpc\_config](#input\_vpc\_config) | Configuration for VPC. The 'cidr\_block' attribute is required. | <pre>object({<br/>    cidr_block = string<br/>    vpc_name   = optional(string, "polardb-ai-search-vpc")<br/>  })</pre> | n/a | yes |
| <a name="input_vswitch_config"></a> [vswitch\_config](#input\_vswitch\_config) | Configuration for VSwitch. The 'cidr\_block' and 'zone\_id' attributes are required. | <pre>object({<br/>    cidr_block   = string<br/>    zone_id      = string<br/>    vswitch_name = optional(string, "polardb-ai-search-vswitch")<br/>  })</pre> | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_oss_bucket_creation_date"></a> [oss\_bucket\_creation\_date](#output\_oss\_bucket\_creation\_date) | The creation date of the OSS bucket |
| <a name="output_oss_bucket_extranet_endpoint"></a> [oss\_bucket\_extranet\_endpoint](#output\_oss\_bucket\_extranet\_endpoint) | The extranet endpoint of the OSS bucket |
| <a name="output_oss_bucket_id"></a> [oss\_bucket\_id](#output\_oss\_bucket\_id) | The ID of the OSS bucket |
| <a name="output_oss_bucket_intranet_endpoint"></a> [oss\_bucket\_intranet\_endpoint](#output\_oss\_bucket\_intranet\_endpoint) | The intranet endpoint of the OSS bucket |
| <a name="output_oss_bucket_location"></a> [oss\_bucket\_location](#output\_oss\_bucket\_location) | The location of the OSS bucket |
| <a name="output_oss_bucket_name"></a> [oss\_bucket\_name](#output\_oss\_bucket\_name) | The name of the OSS bucket |
| <a name="output_polardb_account_name"></a> [polardb\_account\_name](#output\_polardb\_account\_name) | The name of the PolarDB account |
| <a name="output_polardb_account_status"></a> [polardb\_account\_status](#output\_polardb\_account\_status) | The status of the PolarDB account |
| <a name="output_polardb_cluster_connection_string"></a> [polardb\_cluster\_connection\_string](#output\_polardb\_cluster\_connection\_string) | The connection string of the PolarDB cluster |
| <a name="output_polardb_cluster_id"></a> [polardb\_cluster\_id](#output\_polardb\_cluster\_id) | The ID of the PolarDB cluster |
| <a name="output_polardb_cluster_port"></a> [polardb\_cluster\_port](#output\_polardb\_cluster\_port) | The port of the PolarDB cluster |
| <a name="output_polardb_cluster_status"></a> [polardb\_cluster\_status](#output\_polardb\_cluster\_status) | The status of the PolarDB cluster |
| <a name="output_polardb_database_name"></a> [polardb\_database\_name](#output\_polardb\_database\_name) | The name of the PolarDB database |
| <a name="output_polardb_database_status"></a> [polardb\_database\_status](#output\_polardb\_database\_status) | The status of the PolarDB database |
| <a name="output_polardb_endpoint_connection_string"></a> [polardb\_endpoint\_connection\_string](#output\_polardb\_endpoint\_connection\_string) | The connection string of the PolarDB endpoint address |
| <a name="output_polardb_endpoint_ip_address"></a> [polardb\_endpoint\_ip\_address](#output\_polardb\_endpoint\_ip\_address) | The IP address of the PolarDB endpoint |
| <a name="output_vpc_cidr_block"></a> [vpc\_cidr\_block](#output\_vpc\_cidr\_block) | The CIDR block of the VPC |
| <a name="output_vpc_id"></a> [vpc\_id](#output\_vpc\_id) | The ID of the VPC |
| <a name="output_vpc_name"></a> [vpc\_name](#output\_vpc\_name) | The name of the VPC |
| <a name="output_vswitch_cidr_block"></a> [vswitch\_cidr\_block](#output\_vswitch\_cidr\_block) | The CIDR block of the VSwitch |
| <a name="output_vswitch_id"></a> [vswitch\_id](#output\_vswitch\_id) | The ID of the VSwitch |
| <a name="output_vswitch_name"></a> [vswitch\_name](#output\_vswitch\_name) | The name of the VSwitch |
| <a name="output_vswitch_zone_id"></a> [vswitch\_zone\_id](#output\_vswitch\_zone\_id) | The availability zone of the VSwitch |
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