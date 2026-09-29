# CACM | Tidbits | Cost Categorization

> **Bite-sized how-to** | ~30 min setup


## What is Cost Categorization?

Cloud bills tell you the total — they don't tell you who or what is driving the spend. Cost Categorization in Harness CACM solves this by letting you define custom groupings called **Cost Categories**. Each category contains **Cost Buckets** — named segments that match costs based on rules you define using labels, tags, cloud services, accounts, or regions.

The result: instead of a flat total, your Cost Explorer shows costs broken out by the dimensions that matter to your team — workload, environment, service type, or any other label you apply to your resources.


## What does this Tidbit demonstrate?

Two Cost Categories built from real cost data:

1. **By Label** — breaks out Kubernetes workload costs using label names, showing spend per workload 
2. **By AWS Service** — groups AWS service costs into logical categories: Compute, Storage, and Security


## Key Concepts

**Cost Category** — a custom grouping of costs. Think of it as a dimension you add on top of your cloud bill. You define it once and it appears as a Group By option in Cost Explorer.

**Cost Bucket** — an individual segment inside a Cost Category. Each bucket has a name and one or more rules that define which costs belong to it.

**Label** — a Kubernetes label or AWS resource tag used to filter costs. In Harness CACM, labels from your connected K8s clusters are immediately available as cost dimensions.

**Unallocated costs** — costs that don't match any bucket rule. Configured to show as "Other" so no spend is hidden.


## Prerequisites

Before you start, make sure you have:

- A Harness account with the CACM module enabled
- An AWS account with billing access
- A Harness CACM AWS connector connected to your account (Steps 1–3 below)
- A Kubernetes cluster connected to Harness (for the By Label category)


## Step 1 — Set Up AWS CUR 2.0

1. Go to **AWS Billing and Cost Management → Data Exports → Create export**
2. Select **Standard data export** (this is CUR 2.0)
3. Enter an export name (e.g., `harness-ccm-cur2`)
4. Under **Additional export content**, check all four options:
   - Include resource IDs
   - Split cost allocation data
   - Include caller identity (IAM principal) allocation data
   - Include capacity reservation columns and granularity
5. Under **Delivery and storage options**:
   - **Compression type:** Parquet
   - **S3 bucket:** select or create a bucket (note the name)
   - **S3 path prefix:** enter a prefix (e.g., `harness-cur2`)
   - **Time granularity:** Hourly
6. Review and click **Create**

> **Note:** It can take up to 24 hours for AWS to start delivering reports to your Amazon S3 bucket. After delivery starts, AWS updates the AWS Cost and Usage Reports files at least once a day. — [AWS Documentation](https://docs.aws.amazon.com/cur/latest/userguide/cur-create.html)


## Step 2 — Connect AWS to Harness CACM and Create the IAM Role

1. Go to **Account Settings → Connectors → + New Connector → Cloud & AI Costs → AWS - Cloud Cost**
2. Enter a connector **Name** and your **AWS Account ID** → click **Continue**
3. On the **Cost and Usage Report** step, select **CUR 2.0 (recommended)** and enter:
   - **Data Export Name:** the export name you created in AWS (e.g., `harness-ccm-cur2`)
   - **S3 Bucket Name:** the bucket where the export is delivered (e.g., `storage-ccm-cur`)
   - Click **Continue**
4. On the **Choose Requirements** step, select:
   - Cost Visibility
   - Resource Inventory Management
   - Cloud Governance
   - Commitment Orchestration
   - Click **Continue**
5. On the **Create Cross Account Role** step, Harness needs a cross-account IAM role in your AWS account to access the CUR data:
   - Click **Launch Template on AWS console** — this opens a CloudFormation Quick Create stack pre-filled with all required parameters
   - Scroll to the bottom, check the **IAM capabilities acknowledgment**, and click **Create stack**
   - Wait for the stack status to show **CREATE_COMPLETE**
   - Copy the **Cross Account Role ARN** back into the Harness connector wizard
   - Click **Save and Test** — the connection test will pass once the first CUR file has been delivered to S3

**Add CUR 2.0 permissions:**

The default CloudFormation template predates CUR 2.0 and does not include the required `bcm-data-exports` permissions. Add an inline policy to the created role:

1. Go to **AWS IAM → Roles → HarnessCERole-[id]**
2. Click **Add permissions → Create inline policy**
3. Use the JSON editor and paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bcm-data-exports:ListExports",
        "bcm-data-exports:GetExport"
      ],
      "Resource": "*"
    }
  ]
}
```

4. Name the policy `HarnessCUR2DataExportsPolicy` and save


## Step 3 — Create the Cost Category: By Label

1. Go to **CACM → Cost Categories → + New Cost Category**
2. **Cost Category Name:** `By Label`
3. **Unallocated Values:** Show as → `Other`
4. Click **+ Add** to create the first bucket:
   - **Name:** `Cluster Orchestration`
   - **Operand:** Common → Label → Name
   - **Value:** select your workload label (e.g., `cluster-orchestration-test`)
   - Click ✓ to save
5. Click **+ Add** for the second bucket:
   - **Name:** `Pipeline Runner`
   - **Operand:** Common → Label → Name
   - **Value:** select your workload label (e.g., `track-pipeline-runner`)
   - Click ✓ to save
6. Click **Next: Define Shared Costs** → **Save**


## Step 4 — Create the Cost Category: By AWS Service

1. **+ New Cost Category**
2. **Cost Category Name:** `By AWS Service`
3. **Unallocated Values:** Show as → `Other`
4. Add three buckets:

**Compute bucket:**
- Name: `Compute`
- Operand: AWS → Service
- Values: `Amazon Elastic Compute Cloud`, `Amazon EC2 Container Registry (ECR)`, `Amazon Elastic Container Registry Public`, `Elastic Load Balancing`

**Storage bucket:**
- Name: `Storage`
- Operand: AWS → Service
- Values: `Amazon Simple Storage Service`, `Amazon Elastic File System`

**Security bucket:**
- Name: `Security`
- Operand: AWS → Service
- Values: `Amazon GuardDuty`, `AWS Key Management Service`, `AWS Secrets Manager`, `AWS Security Hub`, `AWS CloudTrail`

5. Click **Next: Define Shared Costs** → **Save**

> **Note:** Only add services that appear in the dropdown — these are services with actual cost data in your account.



## Step 5 — View Cost Breakdown in Cost Explorer

1. Go to **CACM → Cost Explorer**
2. Click **Group by** → select **Name** (for label-based breakdown)
3. The chart shows daily costs segmented by workload label — each label appears as a different color in the stacked bar chart
4. To view by service category, change **Group by** to **By AWS Service**



## Resources

- [Harness CACM Cost Categories](https://developer.harness.io/docs/category/cost-categories)
- [AWS CUR 2.0 (Standard Data Export)](https://developer.harness.io/docs/cloud-cost-management/get-started/?cur=cur2#aws)
- [Connect AWS to Harness CACM](https://developer.harness.io/docs/cloud-cost-management/get-started/ccm-smp/aws-smp/)
- [Cost Explorer Overview](https://developer.harness.io/docs/cloud-cost-management/cost-explorer)
