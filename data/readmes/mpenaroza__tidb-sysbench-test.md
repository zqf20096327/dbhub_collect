
# tidb-sysbench-test

## Instructions

### Make Scripts Executable
Before running scripts, ensure they have executable permissions:
```bash
chmod +x run_dummy_upload.sh
chmod +x run_sysbench_test.sh
```

---

### Set Up EC2 Server
- **Instance Recommendation**: Use an Ubuntu instance with 96 vCPUs (e.g., `c5.24xlarge`) for the demo. Smaller instances may work but might require reducing the thread count in the `.sh` files if scripts fail to run. This is the most common reason for a failed execution.
- **Security Permissions**: Configure security groups to allow necessary connections to the EC2 instance.

---

### Transfer Files to EC2 Server
Use `scp` to transfer the required files to your EC2 instance. Replace the paths and IP address with your own:
```bash
scp -i "/path/to/key-pair.pem" \
/path/to/high_concurrency_test.lua \
/path/to/insert_dummy_data.lua \
/path/to/run_dummy_upload.sh \
ubuntu@<your-ec2-instance-ip>:/home/ubuntu/
```

---

### Create a TiDB Cluster

#### Step 1: Log In
- Go to the [TiDB Cloud Console](https://tidbcloud.com/console/).
- Log in or create a new account.

#### Step 2: Create a Cluster
- Navigate to the **Clusters** section and click **Create Cluster**.
- Choose **Dedicated Tier** (Serverless Tier is suitable for testing but may yield variable performance).

#### Step 3: Configure the Cluster
- **Cloud Provider**: Choose AWS or GCP.
- **Region**: Select a region close to your application for lower latency.
- **TiDB (SQL Layer)**: 3 nodes, each with 16 vCPUs.
- **TiKV (Storage Layer)**: 3 nodes, each with 16 vCPUs.
- **TiFlash (Analytics Layer)**: 1 node, with 16 vCPUs.

#### Step 4: Prepare for Testing
- Use the **SQL Users** tab to create a user for testing.
- In the **Overview** tab, click **Connect**, and select **Public** as the Connection Type.
- Download the CA certificate and note the connection parameters.

---

### Set Up a Local Connection to TiDB
- **Recommended Tool**: Use DBeaver (or any MySQL-compatible connector). Command-line tools also work.
- **Connection Configuration**:
  - **Host**: TiDB server host  
  - **Port**: 4000 (default)  
  - **User**: Testing username  
  - **Password**: Testing password  
  - **SSL Settings**: Enable SSL and set the CA certificate path to the downloaded `.cer` file.

---

### Run Scripts for Performance Testing

1. **Update Connection Info**: Modify the `.lua` and `.sh` files to include your TiDB connection details.
2. **Initialize Schema**: Use DBeaver (or your preferred tool) to run the `schema.sql` file on the target database (default: `transaction_demo`).
3. **Populate Data**: Run `./run_dummy_upload.sh` on your EC2 instance to populate the `cards_on_file` and `member_wallet_preferences` tables. Allow the script to run for at least as long as your planned sysbench test duration to ensure sufficient data for concurrency testing.

---

### Start the Test
Run the performance test using:
```bash
./run_sysbench_test.sh
```
**Note**: Sysbench metrics may be unreliable. Use the **Metrics** tab in the TiDB Dashboard or Grafana for accurate performance insights.

---

### Reset for Re-run
To reset and re-run the test:
- Truncate the tables to avoid duplicate key errors by running the `sys-reset.sql` file on your TiDB database.

---

### Troubleshooting

- **Error: Duplicate Key**  
  This occurs when you re-run scripts without clearing the existing data.  
  **Solution**: Run the `sys-reset.sql` script to truncate the tables before re-running the tests.

- **Error: Unable to Connect to EC2**  
  This might happen if the firewall rules or security groups on your EC2 instance block traffic.  
  **Solution**: Ensure the firewall rules allow incoming traffic on the relevent ip/ports.

- **Sysbench Fails to Run**  
  A common cause is the thread count being too high for your EC2 instance.  
  **Solution**: Reduce the thread count in the `run_sysbench_test.sh` and `run_dummy_upload.sh` scripts.  
  Example: Change `--threads=96` to a lower value like `--threads=32`.

- **SSL Certificate Issues**  
  If you encounter errors related to the SSL certificate path, it’s likely the path is incorrect.  
  **Solution**: Verify that the `ssl_ca` path in your `.lua` script points to the correct `.cer` file.

---
