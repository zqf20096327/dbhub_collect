# Huawei Cloud GaussDB NoSQL Redis
<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | ~> 1.4 |
| <a name="requirement_huaweicloud"></a> [huaweicloud](#requirement\_huaweicloud) | ~>1.47 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_huaweicloud"></a> [huaweicloud](#provider\_huaweicloud) | ~>1.47 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [huaweicloud_gaussdb_redis_instance.main](https://registry.terraform.io/providers/huaweicloud/huaweicloud/latest/docs/resources/gaussdb_redis_instance) | resource |
| [huaweicloud_availability_zones.zones](https://registry.terraform.io/providers/huaweicloud/huaweicloud/latest/docs/data-sources/availability_zones) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_availability_zones"></a> [availability\_zones](#input\_availability\_zones) | Specifies the AZ name, if omitted, AZ calculates automatically | `list(string)` | `[]` | no |
| <a name="input_az_number"></a> [az\_number](#input\_az\_number) | Number of AZ, if 'availability\_zones' is omitted, AZ calculates automatically based on this variable | `number` | `3` | no |
| <a name="input_datastore"></a> [datastore](#input\_datastore) | Specifies the database information | <pre>object({<br>    engine         = optional(string, "redis")<br>    storage_engine = optional(string, "rocksDB")<br>    version        = optional(string, "5.0")<br>  })</pre> | `{}` | no |
| <a name="input_flavor"></a> [flavor](#input\_flavor) | Specifies the instance specifications | `string` | `"geminidb.redis.small.4"` | no |
| <a name="input_name"></a> [name](#input\_name) | Specifies the instance name | `string` | n/a | yes |
| <a name="input_name_postfix"></a> [name\_postfix](#input\_name\_postfix) | Specifies the instance name postfix | `string` | `null` | no |
| <a name="input_node_num"></a> [node\_num](#input\_node\_num) | Specifies the number of nodes | `number` | `3` | no |
| <a name="input_password"></a> [password](#input\_password) | Specifies the database password | `string` | `"VerY_5tr0nG-Pa55w0R^d"` | no |
| <a name="input_region"></a> [region](#input\_region) | Specifies the region in which to create the resource, if omitted, the provider-level region will be used | `string` | `null` | no |
| <a name="input_secgroup_id"></a> [secgroup\_id](#input\_secgroup\_id) | Specifies the security group ID, required if the selected subnet doesn't enable network ACL | `string` | n/a | yes |
| <a name="input_subnet_id"></a> [subnet\_id](#input\_subnet\_id) | Specifies the network ID of a subnet | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | Specifies the key/value pairs to associate with the Gaussdb Redis Instance | `map(string)` | `{}` | no |
| <a name="input_volume_size"></a> [volume\_size](#input\_volume\_size) | Specifies the storage space in GB<br>  The minimum and maximum storage space depends on the flavor and nodes\_num variables<br>  See https://support.huaweicloud.com/intl/en-us/redisug-nosql/nosql_05_0059.html | `number` | `10` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | Specifies the VPC ID | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_db_user_name"></a> [db\_user\_name](#output\_db\_user\_name) | Indicates the default username |
| <a name="output_id"></a> [id](#output\_id) | Specifies a resource ID in UUID format |
| <a name="output_lb_ip_address"></a> [lb\_ip\_address](#output\_lb\_ip\_address) | Indicates the LB IP address of the db |
| <a name="output_lb_port"></a> [lb\_port](#output\_lb\_port) | Indicates the LB port of the db |
| <a name="output_mode"></a> [mode](#output\_mode) | Indicates the instance type |
| <a name="output_nodes"></a> [nodes](#output\_nodes) | Indicates the instance nodes information |
| <a name="output_port"></a> [port](#output\_port) | Indicates the database port |
| <a name="output_private_ips"></a> [private\_ips](#output\_private\_ips) | Indicates the IP address list of the db |
| <a name="output_status"></a> [status](#output\_status) | Indicates the DB instance status |
<!-- END_TF_DOCS -->