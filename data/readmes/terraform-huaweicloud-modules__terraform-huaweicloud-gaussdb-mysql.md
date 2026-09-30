# The Terraform module of HUAWEI Cloud GaussDB MySQL service

The terraform module for one-click deployment of GaussDB MySQL.

## Usage

```hcl
variable "vpc_id" {}
variable "subnet_id" {}
variable "security_group_id" {}
variable "master_availability_zone" {}
variable "enterprise_project_id" {}
variable "configuration_id" {}
variable "kms_key_id" {}
variable "auto_scaling_max_flavor" {}

module "gaussdb_mysql_service" {
  source = "terraform-huaweicloud-modules/terraform-huaweicloud-gaussdb-mysql"

  name                     = "test_gaussdb_mysql_name"
  password                 = "Test_password@123"
  vpc_id                   = var.vpc_id
  subnet_id                = var.subnet_id
  security_group_id        = var.security_group_id
  availability_zone_mode   = "multi"
  master_availability_zone = var.master_availability_zone
  read_replicas            = 2
  enterprise_project_id    = var.enterprise_project_id
  sql_filter_enabled       = true
  configuration_id         = var.configuration_id
  private_write_ip         = "192.168.0.1"
  port                     = "8888"
  private_dns_name_prefix  = "testprivatednsname"
  maintain_begin           = "08:00"
  maintain_end             = "11:00"
  ssl_option               = "false"
  description              = "test_description"

  seconds_level_monitoring_enabled = true
  seconds_level_monitoring_period  = 1

  slow_log_show_original_switch = true

  encryption_status = "ON"
  encryption_type   = "kms"
  kms_key_id        = var.kms_key_id

  parameters {
    name  = "auto_increment_increment"
    value = "50"
  }

  backup_strategy {
    start_time = "09:00-10:00"
    keep_days  = "7"
  }

  auto_scaling {
    status = "ON"

    scaling_strategy {
      flavor_switch    = "ON"
      read_only_switch = "OFF"
    }

    monitor_cycle       = 600
    silence_cycle       = 1800
    enlarge_threshold   = 70
    max_flavor          = var.auto_scaling_max_flavor
    reduce_enabled      = true
    max_read_only_count = 20
    read_only_weight    = 10
  }

  tags = {
    foo = "bar"
    key = "value"
  }
}
```

## Contributing

Report issues/questions/feature requests in the [issues](https://github.com/terraform-huaweicloud-modules/terraform-huaweicloud-gaussdb-mysql/issues/new)
section.

Full contributing [guidelines are covered here](.github/how_to_contribute.md).

## Requirements

| Name | Version   |
|------|-----------|
| Terraform | >= 1.3.0  |
| Huaweicloud Provider | >= 1.70.0 |

## Resources

| Name                                        | Type |
|---------------------------------------------|------|
| huaweicloud_gaussdb_mysql_instance.instance | resource |

## Inputs

| Name                             | Description                                                                                                                    | Type         | Default     | Required |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|--------------|-------------|----------|
| charging_mode                    | The charging mode of the GaussDB MySQL resources                                                                               | string       | null        | N        |
| period_unit                      | The period unit of the pre-paid purchase                                                                                       | string       | null        | N        |
| period                           | The period number of the pre-paid purchase                                                                                     | number       | null        | N        |
| is_auto_renew                    | Whether to automatically renew after expiration for GaussDB MySQL resources                                                    | bool         | null        | N        |
| force_import                     | Whether import the instance instead of creating if the name already existed                                                    | string       | null        | N        |
| vpc_id                           | The ID of the VPC to which the GaussDB MySQL resources belongs                                                                 | string       | null        | N        |
| subnet_id                        | The ID of the VPC subnet to which the GaussDB MySQL resources belongs                                                          | string       | null        | N        |
| is_instance_create               | Controls whether a GaussDB MySQL instance should be created (it affects all GaussDB MySQL related resources under this module) | bool         | true        | N        |
| name                             | The instance name                                                                                                              | string       | null        | Y        |
| password                         | The database password                                                                                                          | string       | null        | Y        |
| flavor                           | The instance specifications (e.g. gaussdb.mysql.large.x86.4)                                                                   | string       | null        | Y        |
| security_group_id                | The security group ID                                                                                                          | string       | null        | N        |
| description                      | The description of the instance                                                                                                | string       | null        | N        |
| availability_zone_mode           | The availability zone mode                                                                                                     | string       | "single"    | N        |
| master_availability_zone         | The availability zone where the master node resides                                                                            | string       | null        | N        |
| read_replicas                    | The count of read replicas                                                                                                     | number       | 1           | N        |
| enterprise_project_id            | The enterprise project id                                                                                                      | string       | null        | N        |
| audit_log_enabled                | Whether audit log is enabled                                                                                                   | bool         | false       | N        |
| configuration_id                 | The configuration ID                                                                                                           | string       | null        | N        |
| sql_filter_enabled               | Whether sql filter is enabled                                                                                                  | bool         | false       | N        |
| private_write_ip                 | The private IP address of the DB instance                                                                                      | string       | null        | N        |
| port                             | The database port                                                                                                              | number | null        | N        |
| private_dns_name_prefix          | The prefix of the private domain name                                                                                          | string       | null        | N        |
| maintain_begin                   | The start time for a maintenance window (e.g. 22:00)                                                                           | string       | null        | N        |
| maintain_end                     | The end time for a maintenance window (e.g. 22:00)                                                                             | string       | null        | N        |
| ssl_option                       | Whether to enable SSL                                                                                                          | bool         | false       | N        |
| table_name_case_sensitivity      | Whether the kernel table name is case sensitive                                                                                | bool         | false       | N        |
| time_zone                        | The time zone                                                                                                                  | string       | "UTC+08:00" | N        |
| volume_size                      | The volume size of the instance                                                                                                | string       | null        | N        |
| dedicated_resource_id            | The dedicated resource ID                                                                                                      | string       | null        | N        |
| seconds_level_monitoring_enabled | Whether to enable seconds level monitoring                                                                                     | bool         | false       | N        |
| seconds_level_monitoring_period  | The seconds level collection period                                                                                            | string| null        | N        |
| slow_log_show_original_switch    | The slow log show original switch of the instance                                                                              | bool         | false        | N        |
| encryption_status                | Whether to enable or disable encrypted backup                                                                                  | string         | null        | N        |
| encryption_type                  | The encryption type                                                                                                            | string         | null        | N        |
| kms_key_id                       | The KMS ID  | string         | null        | N        |
| parameters                       | The parameters to be set to the instance after launched | <pre>list(object({<br>  name  = string<br>  value = string<br>})         | null        | N        |
| backup_strategy                  | The advanced backup policy    | <pre>list(object({<br>  start_time  = string<br>  keep_days  = optional(string, null)<br>})         | null        | N        |
| auto_scaling                     | The auto-scaling policies    | <pre>list(object({<br>  status  = string<br><br>  scaling_strategy = list(object({<br>    flavor_switch    = string<br>    read_only_switch = string<br>  }))<br><br>  enlarge_threshold   = optional(number, null)<br>  max_flavor          = optional(string, null)<br>  max_read_only_count = optional(number, null)<br>  monitor_cycle       = optional(number, null)<br>  read_only_weight    = optional(number, null)<br>  reduce_enabled      = optional(bool, null)<br>  silence_cycle       = optional(number, null)<br>}))<br>         | null        | N        |
| datastore                        | The database information   | <pre>list(object({<br>  engine  = string<br>  version = string<br>})         | null        | N        |
| tags                             | The the key/value pairs to associate with the GaussDB Mysql instance   | map(string)  | null        | N        |

## Outputs

| Name                   | Description                                              |
|------------------------|----------------------------------------------------------|
| instance_id            | The GaussDB MySQL instance ID                            |
| status                 | The the GaussDB MySQL instance status                    |
| mode                   | The the GaussDB MySQL instance mode                      |
| db_user_name           | The default username                                     |
| private_dns_name       | The private domain name                                  |
| upgrade_flag           | Whether the version can be upgraded                      |
| current_version        | The current database version                             |
| current_kernel_version | The current database kernel version                      |
| created_at             | The creation time in the **yyyy-mm-ddThh:mm:ssZ** format |
| updated_at             | The update time in the **yyyy-mm-ddThh:mm:ssZ** format   |
| nodes                  | The instance nodes information                           |
| auto_scaling           | The auto-scaling policies                                |
