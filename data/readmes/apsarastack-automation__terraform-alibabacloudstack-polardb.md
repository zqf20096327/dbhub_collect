# Alibaba Cloud PolarDB Terraform Module

This module creates **PolarDB instances, databases, accounts, backup policies, and connection configurations** on Alibaba Cloud Stack.

## Features

- Creates a new PolarDB DB instance
- Manages PolarDB databases within the instance
- Manages PolarDB accounts and privileges
- Configures backup policies for the instance
- Manages database connections
- Supports using an existing PolarDB instance or creating a new one
- Supports both `account_privilege` and `account_database_binding` for privilege management

## Usage

### Basic Usage: Create PolarDB Instance with Database and Account

```hcl
module "polardb" {
  source = "<Module Path>"

  name = "my-polardb-instance"
  
  # Instance configuration
  engine         = "MySQL"
  engine_version = "8.0"
  instance_type  = "rds.mysql.c1.large"
  storage        = 20
  storage_type   = "local_ssd"
  
  # VPC configuration
  vswitch_id = "vsw-xxxxxxxx"
  
  # Database configuration
  databases = {
    mydb = {
      character_set_name = "utf8mb4"
      description        = "My application database"
    }
  }
  
  # Account configuration
  accounts = {
    app_user = {
      password           = "SecurePassword123!"
      account_type       = "Normal"
      account_privileges = {
        mydb = "ReadWrite"
      }
    }
  }
}
```

### Advanced Usage: Enable Backup Policy

```hcl
module "polardb" {
  source = "<Module Path>"

  name           = "my-polardb-instance"
  engine         = "MySQL"
  engine_version = "8.0"
  instance_type  = "rds.mysql.c1.large"
  storage        = 20
  storage_type   = "local_ssd"
  vswitch_id     = "vsw-xxxxxxxx"
  
  # Backup policy configuration
  backup_policy = {
    backup_retention_period = 7
    preferred_backup_period = "Monday,Wednesday,Friday"
    preferred_backup_time   = "02:00Z-03:00Z"
    enable_backup_log       = 1
  }
}
```

### Use Existing PolarDB Instance

```hcl
module "polardb" {
  source = "<Module Path>"

  # Use existing instance
  db_instance_id = "rm-xxxxxxxx"
  
  # Create databases and accounts on existing instance
  databases = {
    newdb = {
      character_set_name = "utf8mb4"
    }
  }
  
  accounts = {
    newuser = {
      password     = "SecurePassword123!"
      account_type = "Normal"
    }
  }
}
```

### Use Account Database Binding for Privileges

```hcl
module "polardb" {
  source = "<Module Path>"

  name           = "my-polardb-instance"
  engine         = "MySQL"
  engine_version = "8.0"
  instance_type  = "rds.mysql.c1.large"
  storage        = 20
  vswitch_id     = "vsw-xxxxxxxx"
  
  # Use account_database_binding resource instead of account_privilege
  use_account_database_binding = true
  
  databases = {
    mydb = {
      character_set_name = "utf8mb4"
    }
  }
  
  accounts = {
    app_user = {
      password           = "SecurePassword123!"
      account_type       = "Normal"
      account_privileges = {
        mydb = "ReadWrite"
      }
    }
  }
}
```

## Environment Dependencies

### Terraform Core

| Name      | Version   |
|-----------|-----------|
| Terraform | >= 1.5.6  |

### Provider

| Name              | Version                |
|-------------------|------------------------|
| alibabacloudstack | >= 3.18.24, < 3.19.0   |

## Module Variables

### Input Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| `name` | PolarDB instance name | `string` | `""` | Yes (if creating new instance) |
| `db_instance_id` | Existing PolarDB instance ID | `string` | `""` | No |
| `engine` | Database engine type | `string` | `"MySQL"` | No |
| `engine_version` | Database engine version | `string` | `"8.0"` | No |
| `instance_type` | Instance type/class | `string` | `""` | Yes (if creating new instance) |
| `storage` | Storage size in GB | `number` | `20` | No |
| `storage_type` | Storage type | `string` | `"local_ssd"` | No |
| `vswitch_id` | VSwitch ID for network configuration | `string` | `""` | No |
| `vpc_id` | VPC ID for network configuration | `string` | `""` | No |
| `zone_id` | Zone ID for instance | `string` | `""` | No |
| `instance_charge_type` | Instance charge type | `string` | `"PostPaid"` | No |
| `security_ips` | List of security IPs | `list(string)` | `[]` | No |
| `parameters` | Database parameters | `map(string)` | `{}` | No |
| `databases` | Map of databases to create | `map(object)` | `{}` | No |
| `accounts` | Map of accounts to create | `map(object)` | `{}` | No |
| `backup_policy` | Backup policy configuration | `object` | `null` | No |
| `db_connection_prefix` | Connection prefix | `string` | `""` | No |
| `port` | Database port | `number` | `3306` | No |
| `tags` | Tags for resources | `map(string)` | `{}` | No |
| `use_account_database_binding` | Use account_database_binding for privileges | `bool` | `false` | No |

### Output Variables

| Name | Description |
|------|-------------|
| `db_instance_id` | ID of the PolarDB instance |
| `instance_name` | Name of the PolarDB instance |
| `connection_string` | Connection string of the instance |
| `port` | Database connection port |
| `database_names` | List of created database names |
| `account_names` | List of created account names |

## Examples

For more usage scenarios, see the [`examples/`](./examples) directory:
- `create-polardb-instance-complete` - Complete example with all features
- `use-existing-instance` - Example using existing PolarDB instance
- `create-instance-with-backup` - Example with backup policy configuration

## Notes

- This module supports both creating a new PolarDB instance and using an existing one.
- When `db_instance_id` is provided, the module will not create a new instance.
- Database and account management can be done independently of instance creation.
- Backup policy configuration is optional and only applied when provided.
- Set `use_account_database_binding = true` to use the newer `account_database_binding` resource for privilege management.

## License

MIT License. See LICENSE for details.
