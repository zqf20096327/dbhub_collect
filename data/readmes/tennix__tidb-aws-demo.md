# Demo for deploying TiDB Cluster on AWS

**WARING**: This is for demo purpose, please don't use it in production.

## Provisioning AWS resources

A production TiDB Cluster requires several machines, it's better to use [Terraform](https://www.terraform.io) to provision AWS resources instead of managing them on cloud console.

Make sure terraform is installed on local machine

1. Clone this repo: `git clone https://github.com/tennix/tidb-aws-demo`
2. Initialize terraform: `cd tidb-aws-demo && terraform init`
3. Customize the variables in `variables.tf`
4. Applying plan: `terraform apply`

After the above steps, if executed successfully, the required AWS resources will be created and the EC2 instances IP lists are printed.

You can login to the bastion machine by: `ssh -i secrets/bench-demo ec2-user@<bastion-public-ip>`

The other ec2 instances can be accessed on bastion machine using their private IPs.

Then ssh into the bastion to deploy TiDB cluster using [TiUP](https://github.com/pingcap/tiup).
