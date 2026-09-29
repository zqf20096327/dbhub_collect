# Geo-distributed TiDB cluster in Akamai Cloud
This project deploys a geo-distributed TiDB cluster on Linode Kubernetes Engine (LKE) in 3 different regions using Terraform, with Kuma Service Mesh enabling secure cross-cluster communication.

## 📦 Stack Overview

- **Infrastructure**: [Akamai Cloud](https://www.linode.com/)
- **Provisioning**: [Terraform](https://www.terraform.io/)
- **Kubernetes**: [k8s](https://kubernetes.io/)
- **Multi-Cluster Service Mesh**: [Kuma](https://kuma.io/)
- **Database**: [TiDB](https://pingcap.com/tidb)

## Architecture Diagram
![image](https://github.com/user-attachments/assets/777509c2-a2f5-42e3-af3f-4bd54733dbcb)


## Prerequisites
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [Akamai Cloud account](https://www.linode.com/)
- [Linode API token](https://techdocs.akamai.com/linode-api/reference/get-started#personal-access-tokens)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (debugging + perf-test)

## Deployment steps
1. `git clone <repo-url>`
2. Configure your [Linode API token](https://techdocs.akamai.com/cloud-computing/docs/manage-personal-access-tokens#create-an-api-token) and [regions code](https://www.linode.com/global-infrastructure/availability/) for each cluster in the `config.tfvars` file
```
#Akamai Connected Cloud configuration
linode_token = "<your-linode-token>"
region_lke_tidb_1 = "<region-1>"
region_lke_tidb_2 = "<region-2>"
region_lke_tidb_3 = "<region-3>"
region_lke_kuma_global_cp = "<region-1>"
lke_worker_node_type = "g6-dedicated-2"
lke_worker_node_count = 3
```
3. Initialize Terraform `terraform init`
4. Apply the Terraform configuration `terraform apply -var-file='config.tfvars'`


## Database Access Setup

### Create MySQL Client Pod

Launch a temporary MySQL client pod to interact with your TiDB cluster:

```bash
kubectl run mysql-client -n tidb -it --rm --image=mysql:8 --restart=Never -- sh
```

**Note**: This command creates an ephemeral pod that will be automatically removed when you exit.

### Connect to TiDB

From within the client pod, establish a connection to your TiDB cluster:

```bash
mysql --comments -h cluster-<your_region>-tidb -P 4000 -u root
```

Replace `<your_region>` with your actual region identifier (e.g., `nl-ams`, `de-fra-2`, or `gb-lon`).

## Database and Schema Setup

### Initialize Demo Database

Create a dedicated database for testing:

```sql
CREATE DATABASE demo_db;
USE demo_db;
```

### Configure Placement Policies

Set up region-specific placement policies to control data distribution across your multi-region cluster:

```sql
-- Netherlands (Amsterdam) placement policy
CREATE PLACEMENT POLICY even_distribution_nl_ams
PRIMARY_REGION="nl-ams"
REGIONS="nl-ams,de-fra-2,gb-lon"
SCHEDULE="EVEN";

-- Germany (Frankfurt) placement policy
CREATE PLACEMENT POLICY even_distribution_de_fra
PRIMARY_REGION="de-fra-2"
REGIONS="nl-ams,de-fra-2,gb-lon"
SCHEDULE="EVEN";

-- United Kingdom (London) placement policy
CREATE PLACEMENT POLICY even_distribution_gb_lon
PRIMARY_REGION="gb-lon"
REGIONS="nl-ams,de-fra-2,gb-lon"
SCHEDULE="EVEN";
```

**Key Points**:
- Each policy designates a different primary region while maintaining replicas across all three regions
- The `EVEN` schedule ensures balanced data distribution
- Modify the region codes to match your actual deployment regions

### Create Partitioned Test Table

Create a sample table with region-based partitioning:

```sql
CREATE TABLE test_data_partitioned (
    id BIGINT NOT NULL AUTO_RANDOM,
    region VARCHAR(10) NOT NULL
        CHECK (region IN ('nl-ams','de-fra-2','gb-lon')),
    payload VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, region)
) PARTITION BY LIST COLUMNS (region) (
    PARTITION p_region_nl_ams VALUES IN('nl-ams') PLACEMENT POLICY even_distribution_nl_ams,
    PARTITION p_region_de_fra VALUES IN('de-fra-2') PLACEMENT POLICY even_distribution_de_fra,
    PARTITION p_region_gb_lon VALUES IN('gb-lon') PLACEMENT POLICY even_distribution_gb_lon
);
```

**Table Features**:
- Region-based partitioning ensures data locality
- Each partition is assigned its corresponding placement policy
- Constraint validation ensures only valid region values are accepted

## Performance Testing

### Execute Workload Tests

Navigate to the performance testing directory and deploy the test workload:

```bash
# From your local machine (outside the MySQL client pod)
cd perf-test
kubectl apply -f perf-test.yaml
```

The Kubernetes deployment in this directory will execute comprehensive INSERT and SELECT performance tests against your configured database setup.
