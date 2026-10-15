=====
# Alibaba Cloud PolarDBX Terraform Module

This module is designed to create and manage **PolarDBX instances**, **one-time manual backups**, **super accounts (three-role rights separation)**, **Log Engine (CDC)**, **read-write splitting configurations**, and **read-only instances** on Alibaba Cloud Stack, providing integrated infrastructure orchestration capabilities for PolarDBX.

## Features

- Create a new PolarDBX instance (or reuse an existing one)  
- Manage PolarDBX databases and accounts within the instance  
- Trigger a one-time manual backup for the instance (`enable_backup`)  
- Create a super account with optional three-role rights separation (admin / security admin / auditor)  
- Configure the Log Engine (CDC) service, supporting multi-stream synchronization  
- Enable and manage read-write splitting policies, supporting HTAP scenarios  
- Create and manage PolarDBX read-only instances to separate read and write workloads  
- Support extending configuration using an existing PolarDBX instance  
- Backup policy management has been decoupled into a dedicated module (`polardbx_backup_policy`); this module only supports one-time manual backups, not periodic backup policies  

> ⚠️ **Important Notes**:  
> - **Backup policy management has been moved to a separate module.** To configure backup policies, please use the `polardbx_backup_policy` submodule.  
> - This module is a **composite wrapper module**, internally invoking five independent submodules: `polardbx_instance`, `polardbx_super_account`, `polardbx_log_engine`, `polardbx_read_write_splitting`, and `polardbx_readonly_instance`. Each submodule is fully decoupled and can be enabled independently.

## Usage

### Basic Usage: Create a PolarDBX Instance with All Advanced Features Enabled

```hcl
module "polardbx" {
  source = "<module-path>"

  # Primary instance configuration
  name           = "my-polardbx-cluster"
  engine_version = "5.7"
  storage        = 100
  vswitch_id     = "vsw-xxxxxxxx"
  cn_node_count  = 4
  dn_node_count  = 4
  topology_type  = "3azones"
  description    = "Production PolarDBX cluster with CDC and RW splitting"

  # Databases and accounts
  databases = {
    app_db = {
      encode      = "utf8mb4"
      description = "Main application database"
    }
  }
  accounts = {
    app_user = {
      password = "SecurePassword123!"
      description = "Application database user"
    }
  }

  # One-time manual backup
  enable_backup = true
  backup_type   = 0

  # Super account with three-role rights separation
  super_account = {
    admin_account_name           = "admin_user"
    admin_account_password       = "SecurePassword123!"
    admin_account_description    = "Super admin account"
    security_account_name        = "security_user"
    security_account_password    = "SecurePassword123!"
    security_account_description = "Security admin account"
    audit_account_name           = "audit_user"
    audit_account_password       = "SecurePassword123!"
    audit_account_description    = "Audit account"
  }

  # Log Engine (CDC)
  enable_log_engine                = true
  log_engine_cdc_node_class        = "polarx.cdc.2xlarge"
  log_engine_cdc_node_count        = 2
  log_engine_multi_streams         = []

  # Read-write splitting configuration
  enable_read_write_splitting      = true
  rw_splitting_enable_htap         = true
  rw_splitting_master_read_weight  = 30
  rw_splitting_storage_delay_threshold = 500

  # Read-only instance
  enable_readonly_instance         = true
  readonly_instance_name           = "my-polardbx-readonly"
  readonly_storage                 = 100
  readonly_cn_node_count           = 2
  readonly_dn_node_count           = 2
  readonly_cn_node_class           = "polarx.cn.2xlarge"
  readonly_dn_node_class           = "polarx.dn.2xlarge"
}
```

### Advanced Usage: Reuse an Existing PolarDBX Instance and Enable Only Selected Features

```hcl
module "polardbx" {
  source = "<module-path>"

  # Reuse an existing instance (no new instance will be created)
  instance_id    = "pxc-xxxxxxxx"
  engine_version = "5.7"

  # Enable only Log Engine (CDC)
  enable_log_engine                = true
  log_engine_cdc_node_class        = "polarx.cdc.large"
  log_engine_cdc_node_count        = 2

  # Enable only read-write splitting (no read-only instance created)
  enable_read_write_splitting      = true
  rw_splitting_enable_consistent_replica_read = true

  # Do not create a read-only instance
  enable_readonly_instance = false
}
```

### Minimal Usage: Create Only a PolarDBX Instance (All Advanced Features Disabled)

```hcl
module "polardbx" {
  source = "<module-path>"

  name           = "simple-polardbx"
  engine_version = "5.7"
  storage        = 50
  vswitch_id     = "vsw-xxxxxxxx"
  cn_node_count  = 2
  dn_node_count  = 2

  # Explicitly disable all advanced features
  enable_log_engine             = false
  enable_read_write_splitting   = false
  enable_readonly_instance      = false
}
```

## Environment Dependencies

### Terraform Core

| Name      | Version     |
|-----------|-------------|
| Terraform | >= 1.5.6    |

### Providers

| Name              | Version                   |
|-------------------|---------------------------|
| alibabacloudstack | >= 3.18.24, < 3.19.0      |

## Module Variables

### Input Variables

| Name                                    | Description                                                                                                               | Type                                                                                                                                                         | Default Value | Required?                                      |
|-----------------------------------------|---------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|------------------------------------------------|
| `name`                                  | PolarDBX instance name (takes effect only when `instance_id` is unset)                                                    | `string`                                                                                                                                                     | `""`          | No (if `instance_id` is set)                  |
| `instance_id`                           | Existing PolarDBX instance ID (if set, creation of a new instance is skipped)                                               | `string`                                                                                                                                                     | `""`          | No (if `name` is set)                         |
| `engine_version`                        | Database engine version; valid values: `"5.7"` or `"8.0"`                                                                   | `string`                                                                                                                                                     | `"5.7"`       | No                                            |
| `storage`                               | Primary instance storage size (GB)                                                                                          | `number`                                                                                                                                                     | `50`          | No                                            |
| `vswitch_id`                            | VSwitch ID used for network configuration (required when creating a new instance or read-only instance)                    | `string`                                                                                                                                                     | `""`          | No (but required if creating an instance)     |
| `cn_node_class`                         | Compute Node (CN) specification                                                                                             | `string`                                                                                                                                                     | `""`          | No                                            |
| `cn_node_count`                         | Number of Compute Nodes (CN)                                                                                                | `number`                                                                                                                                                     | `2`           | No                                            |
| `dn_node_class`                         | Data Node (DN) specification                                                                                                | `string`                                                                                                                                                     | `""`          | No                                            |
| `dn_node_count`                         | Number of Data Nodes (DN)                                                                                                   | `number`                                                                                                                                                     | `2`           | No                                            |
| `topology_type`                         | Topology type; valid values: `"1azone"` or `"3azones"`                                                                     | `string`                                                                                                                                                     | `""`          | No                                            |
| `description`                           | Primary instance description                                                                                                | `string`                                                                                                                                                     | `""`          | No                                            |
| `databases`                             | Map of databases to create (keys are database names; values are configuration objects)                                     | `map(object({encode=optional(string,"utf8mb4"),mode=optional(string,"auto"),description=optional(string,"")}))`                                             | `{}`          | No                                            |
| `accounts`                              | Map of accounts to create (keys are account names; values are configuration objects)                                        | `map(object({password=string,description=optional(string,""),account_privileges=optional(map(string),{})}))`                                                | `{}`          | No                                            |
| `use_account_database_binding`        | Whether to use the `account_database_binding` resource for privilege management (recommended for complex permission scenarios) | `bool`                                                                                                                                                       | `false`       | No                                            |
| `enable_backup`                         | Whether to trigger a one-time manual backup for the instance                                                              | `bool`                                                                                                                                                       | `false`       | No                                            |
| `backup_type`                           | Type of the manual backup; valid values: `0` (physical backup); only used when `enable_backup` is true                     | `number`                                                                                                                                                     | `0`           | No                                            |
| `super_account`                         | Super account configuration (sensitive); set to `null` to skip. Fields: `admin_account_name`/`admin_account_password` (required), `admin_account_description`, `security_account_*`, `audit_account_*` (security and audit groups must be provided together) | `object({admin_account_name=string,admin_account_password=string,admin_account_description=optional(string,""),security_account_name=optional(string),security_account_password=optional(string),security_account_description=optional(string,""),audit_account_name=optional(string),audit_account_password=optional(string),audit_account_description=optional(string)})` | `null`        | No                                            |
| `enable_log_engine`                     | Whether to enable Log Engine (CDC) configuration                                                                            | `bool`                                                                                                                                                       | `false`       | No                                            |
| `log_engine_cdc_node_class`             | CDC node specification                                                                                                      | `string`                                                                                                                                                     | `""`          | No                                            |
| `log_engine_cdc_node_count`             | Number of CDC nodes                                                                                                         | `number`                                                                                                                                                     | `2`           | No                                            |
| `log_engine_multi_streams`              | List of multi-stream synchronization configurations                                                                       | `list(object({group_name=string,comment=optional(string,""),hash_level=string,node_class=string,node_count=number}))`                                       | `[]`          | No                                            |
| `enable_read_write_splitting`           | Whether to enable read-write splitting configuration                                                                      | `bool`                                                                                                                                                       | `false`       | No                                            |
| `rw_splitting_attend_htap_list`         | List of HTAP instance IDs to join read-write splitting                                                                    | `list(string)`                                                                                                                                               | `[]`          | No                                            |
| `rw_splitting_auto_attend_htap`         | Whether to automatically join HTAP instances                                                                                | `bool`                                                                                                                                                       | `false`       | No                                            |
| `rw_splitting_delay_execution_strategy` | Delay execution strategy (`0` or `1`)                                                                                       | `number`                                                                                                                                                     | `0`           | No                                            |
| `rw_splitting_enable_consistent_replica_read` | Whether to enable consistent replica reads                                                                             | `bool`                                                                                                                                                       | `false`       | No                                            |
| `rw_splitting_enable_htap`              | Whether to enable HTAP support                                                                                              | `bool`                                                                                                                                                       | `false`       | No                                            |
| `rw_splitting_master_read_weight`       | Master instance read weight (1–100)                                                                                         | `number`                                                                                                                                                     | `50`          | No                                            |
| `rw_splitting_storage_delay_threshold`  | Storage delay threshold (milliseconds)                                                                                      | `number`                                                                                                                                                     | `1000`        | No                                            |
| `enable_readonly_instance`              | Whether to create a read-only instance                                                                                      | `bool`                                                                                                                                                       | `false`       | No                                            |
| `readonly_instance_name`                | Read-only instance name                                                                                                     | `string`                                                                                                                                                     | `""`          | No                                            |
| `readonly_storage`                      | Read-only instance storage size (GB)                                                                                        | `number`                                                                                                                                                     | `50`          | No                                            |
| `readonly_cn_node_count`                | Number of CN nodes in the read-only instance                                                                              | `number`                                                                                                                                                     | `2`           | No                                            |
| `readonly_dn_node_count`                | Number of DN nodes in the read-only instance                                                                              | `number`                                                                                                                                                     | `2`           | No                                            |
| `readonly_cn_node_class`                | CN node specification for the read-only instance                                                                          | `string`                                                                                                                                                     | `""`          | No                                            |
| `readonly_dn_node_class`                | DN node specification for the read-only instance                                                                          | `string`                                                                                                                                                     | `""`          | No                                            |
| `readonly_description`                | Read-only instance description                                                                                              | `string`                                                                                                                                                     | `""`          | No                                            |

> 💡 **Mutual Exclusion Rules**:  
> - `instance_id` and `name`: Exactly one of these must be set.  
> - When `instance_id` is set, instance creation parameters such as `name`, `storage`, `vswitch_id`, `cn_node_*`, `dn_node_*`, and `topology_type` are ignored (they are only used for managing resources like `databases`/`accounts`).

### Output Variables

| Name                                    | Description                                                                                                              |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| `instance_id`                           | Primary PolarDBX instance ID                                                                                             |
| `instance_name`                         | Primary PolarDBX instance name                                                                                           |
| `database_names`                        | List of created database names                                                                                           |
| `account_names`                         | List of created account names                                                                                            |
| `vswitch_id`                            | VSwitch ID used by the primary instance                                                                                  |
| `cn_node_class`                         | CN node specification of the primary instance                                                                            |
| `dn_node_class`                         | DN node specification of the primary instance                                                                            |
| `backup_set_id`                         | ID of the backup set created by the manual backup (`null` when `enable_backup` is false)                                 |
| `backup_status`                         | Status of the manual backup: `0` creating, `1` success, `2` failed (`null` when `enable_backup` is false)                |
| `super_account_admin_name`              | Name of the super (admin) account, marked sensitive (`null` when `super_account` is not configured)                        |
| `super_account_three_roles`             | Whether three-role rights separation (admin/security/audit) is enabled (`null` when `super_account` is not configured)   |
| `log_engine_id`                         | Log Engine (CDC) configuration ID (returned if enabled)                                                                  |
| `log_engine_cdc_node_class`             | CDC node specification                                                                                                   |
| `log_engine_cdc_node_count`             | Number of CDC nodes                                                                                                      |
| `log_engine_multi_stream`               | Multi-stream synchronization configuration (returned if enabled)                                                         |
| `rw_splitting_id`                       | Read-write splitting configuration ID (returned if enabled)                                                              |
| `rw_splitting_attend_htap_list`         | List of joined HTAP instances                                                                                            |
| `rw_splitting_auto_attend_htap`         | Whether HTAP instances are joined automatically                                                                          |
| `rw_splitting_delay_execution_strategy` | Delay execution strategy                                                                                                 |
| `rw_splitting_enable_consistent_replica_read` | Whether consistent replica reads are enabled                                                                         |
| `rw_splitting_enable_htap`              | Whether HTAP is enabled                                                                                                  |
| `rw_splitting_master_read_weight`       | Master instance read weight                                                                                              |
| `rw_splitting_storage_delay_threshold`  | Storage delay threshold                                                                                                  |
| `readonly_instance_id`                  | Read-only instance ID (returned if enabled)                                                                              |
| `readonly_instance_name`                | Read-only instance name                                                                                                  |
| `readonly_is_read_db_instance`        | Whether the instance is read-only (always `true`)                                                                        |
| `readonly_cn_node_class`                | CN node specification of the read-only instance                                                                          |
| `readonly_dn_node_class`                | DN node specification of the read-only instance                                                                          |
| `readonly_connection_string`            | Connection string for the read-only instance (returned if enabled)                                                       |
| `readonly_status`                       | Status of the read-only instance (returned if enabled)                                                                   |

## Examples

For more usage scenarios, refer to the [`examples/`](./examples) directory:  
- `create-polardbx-full-feature` — Complete example enabling instance creation, CDC, read-write splitting, and read-only instances  
- `use-existing-instance-with-cdc` — Example reusing an existing instance and enabling only the Log Engine (CDC)  
- `enable-rw-splitting-only` — Lightweight example enabling only read-write splitting  
- `create-readonly-instance` — Example creating a read-only instance independently  

## Notes

- This module is a **composite wrapper module**; its behavior is entirely determined by the referenced submodules (`polardbx_instance`, `polardbx_super_account`, `polardbx_log_engine`, `polardbx_read_write_splitting`, `polardbx_readonly_instance`).  
- **Backup policies are not managed by this module.** Always use the dedicated `polardbx_backup_policy` submodule to configure backups. `enable_backup` only triggers a **one-time manual backup**; the backup resource is trigger-style (no update, all arguments ForceNew) and its delete is a no-op (the backup set remains on the instance after destroy).  
- When `instance_id` is specified, primary instance resources (e.g., `alibabacloudstack_polardbx_instance`) are **not created**; only databases, accounts, and advanced features (CDC/RW/RO) are managed.  
- The Log Engine (CDC), read-write splitting, and read-only instances **strongly depend on the primary instance ID**, so either `instance_id` must be provided or the primary instance must have been successfully created and its output made available.  
- For the super account, the **security account group and the audit account group must be provided together**; providing only one of them is rejected by the provider (`RequiredWith` validation). The `super_account` variable is sensitive, and the provider's delete for the super account resource is a no-op (accounts remain on the instance after destroy).  
- `use_account_database_binding = true` is recommended for production environments requiring fine-grained control over account-database privilege bindings.  
- All advanced features (CDC, RW splitting, read-only instances, super account, manual backup) are **disabled by default**; enable them explicitly to avoid unintended resource creation.  
- For managing multiple read-only instances or complex CDC multi-stream topologies, consider directly invoking the corresponding submodules to achieve finer-grained control.