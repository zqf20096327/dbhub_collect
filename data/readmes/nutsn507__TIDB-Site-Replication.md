
# TiDB Site Replication Setup Guide

This guide provides step-by-step instructions to set up site replication between two TiDB clusters, including backup, restore, and incremental replication using TiCDC. Follow these steps to ensure a successful and consistent migration.

## Prerequisites

- **Source Cluster**: The existing TiDB cluster where data originates.
- **Destination Cluster**: A newly deployed TiDB cluster for replication.
- **TiCDC**: Installed and configured on the destination cluster.
- **S3-Compatible Storage**: Configured to store and restore backups (e.g., MinIO).
- **Access**: Ensure both clusters have network access to the S3-compatible storage and each other.

## Step 1: Deploy TiDB Cluster in the Destination Cluster

Deploy the TiDB cluster in the destination environment using TiDB Operator and Kubernetes. Ensure the cluster is functional and all components are healthy before proceeding.

## Step 2: Install TiCDC in the Destination Cluster

To minimize the impact of network latency, install and configure TiCDC in the destination cluster.

### Modify `tidb-cluster.yaml`

Add the following configuration under the `ticdc` section:

```yaml
ticdc:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/component
            operator: In
            values:
            - ticdc
        topologyKey: kubernetes.io/hostname
  baseImage: pingcap/ticdc
  replicas: 3
  limits:
    cpu: "8"
    memory: "16Gi"
  requests:
    cpu: "1"
    memory: "2Gi"
    storage: "10Gi"
```

### Apply the Configuration

```bash
kubectl apply -f tidb-cluster.yaml
```

## Step 3: Disable GC in the Source Cluster

Disabling GC ensures that historical data is not deleted during the migration process.

### Disable GC

```sql
SET GLOBAL tidb_gc_enable=FALSE;
```

### Verify GC is Disabled

```sql
SELECT @@global.tidb_gc_enable;
```

Expected output:

```
+-------------------------+
| @@global.tidb_gc_enable |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
```

## Step 4: Backup All Databases in the Source Cluster

Use the `BACKUP` SQL command to create a full backup of all databases in the source cluster.

### Backup Command

Run the following query on the source cluster:

```sql
BACKUP DATABASE * TO 's3://backuptidb?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

### S3 Details

- **Bucket Name**: `backuptidb`
- **Access Key**: `UgL2VKb5AOeIWw5S`
- **Secret Key**: `cNuXvK2762qcHWWetubRHuhco0CR1AqZ`
- **Endpoint**: `http://10.111.0.167`

### Explanation of the S3 URL

The `s3://backuptidb` URL specifies the destination for the backup files. It includes:
- **Bucket Name**: `backuptidb` is the S3-compatible storage bucket where backups will be saved.
- **Access and Secret Keys**: Used to authenticate with the S3-compatible storage.
- **Endpoint**: `http://10.111.0.167` is the server address for the storage.
- **Path Style**: `force-path-style=true` ensures compatibility with MinIO by enforcing path-style URLs.

### Optional: Specify Backup Folder

To organize backups by folders, you can specify a folder path in the S3 URL. For example, to back up all databases to a folder named `full_backup`:

```sql
BACKUP DATABASE * TO 's3://backuptidb/full_backup?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

### Backup a Specific Database

To back up a specific database (e.g., `example_db`):

```sql
BACKUP DATABASE example_db TO 's3://backuptidb/example_db_backup?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

To specify a folder for a database backup:

```sql
BACKUP DATABASE example_db TO 's3://backuptidb/specific_folder/example_db_backup?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

## Step 5: Restore All Databases to the Destination Cluster

Restore the backup to the destination cluster using the `RESTORE` SQL command.

### Restore Command

Run the following query on the destination cluster:

```sql
RESTORE DATABASE * FROM 's3://backuptidb?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

### Explanation of the S3 URL

The `s3://backuptidb` URL specifies the source of the backup files. It includes:
- **Bucket Name**: `backuptidb` is the S3-compatible storage bucket where the backup is stored.
- **Access and Secret Keys**: Used to authenticate with the S3-compatible storage.
- **Endpoint**: `http://10.111.0.167` is the server address for the storage.
- **Path Style**: `force-path-style=true` ensures compatibility with MinIO by enforcing path-style URLs.

### Optional: Restore from a Specific Folder

To restore from a specific folder (e.g., `full_backup`):

```sql
RESTORE DATABASE * FROM 's3://backuptidb/full_backup?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

### Restore a Specific Database

To restore a specific database (e.g., `example_db`) from its backup:

```sql
RESTORE DATABASE example_db FROM 's3://backuptidb/example_db_backup?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

To restore from a specific folder for a database backup:

```sql
RESTORE DATABASE example_db FROM 's3://backuptidb/specific_folder/example_db_backup?access-key=UgL2VKb5AOeIWw5S&secret-access-key=cNuXvK2762qcHWWetubRHuhco0CR1AqZ&endpoint=http://10.111.0.167&force-path-style=true';
```

## Step 6: Create a Changefeed for Incremental Replication

After restoring the backup, configure TiCDC to enable incremental replication from the source cluster to the destination cluster.

### Changefeed Command

Run the following command from the TiCDC CLI:

```bash
./cdc cli changefeed create     --pd=http://10.111.0.143:2379     --sink-uri="mysql://cdc_user:eA\$@m1n@10.111.0.166:4000/"     --changefeed-id="dr-primary-to-secondary"
```

## Step 7: Validate the Changefeed State

### Check Changefeed List

Verify that the changefeed is in a `normal` state:

```bash
./cdc cli changefeed list --pd=http://10.111.0.143:2379
```

Expected output:

```json
[
  {
    "id": "dr-primary-to-secondary",
    "summary": {
      "state": "normal",
      "tso": 454108735118508034,
      "checkpoint": "2024-11-22 21:55:50.153",
      "error": null
    }
  }
]
```

### Query Changefeed Details

```bash
./cdc cli changefeed query --pd=http://10.111.0.143:2379 --changefeed-id="dr-primary-to-secondary"
```

## Step 8: Re-enable GC in the Source Cluster

Once the destination cluster has fully caught up, re-enable GC in the source cluster to resume normal operations.

### Enable GC

```sql
SET GLOBAL tidb_gc_enable=TRUE;
```

### Verify GC is Enabled

```sql
SELECT @@global.tidb_gc_enable;
```

Expected output:

```
+-------------------------+
| @@global.tidb_gc_enable |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set (0.00 sec)
```

## Notes and Best Practices

- Ensure network connectivity between the source cluster, destination cluster, and S3-compatible storage.
- Monitor the status of TiCDC changefeeds regularly using CLI commands.
- Perform the entire process in a staging environment before applying it to production to ensure data consistency.

This guide provides a complete, step-by-step process for setting up TiDB site replication with both full and incremental data synchronization.
