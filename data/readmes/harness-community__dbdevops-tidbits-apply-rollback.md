# DB DevOps | Tidbits | Apply and Rollback

> **Bite-sized how-to** | ~20 min setup

---

## What is Database DevOps?

Database schema changes are often done manually — someone runs SQL scripts directly against the database. This approach is risky, hard to track, and difficult to reverse when something goes wrong.

Harness Database DevOps treats your database schema like application code — version-controlled in Git, deployed through a pipeline, and reversible with a rollback. Every schema change is tracked, tagged, and auditable through the Migration State view.

---

## What does this Tidbit demonstrate?

A real-world scenario using the e-commerce products table:

1. **Apply V1 (Base Schema)** — create the `products` table with 4 columns
2. **Apply V2 (Add Column)** — add a `discount_percentage` column — app starts lagging
3. **Apply V3 (Data Type Change)** — change `price` from `DECIMAL` to `FLOAT` — pricing precision lost
4. **Rollback V3 → V2** — revert the data type change, restore price precision
5. **Rollback V2 → V1** — remove the discount column, restore base schema

**Key teaching point:** Database and application rollbacks must happen simultaneously to keep them in sync.

---

## Key Concepts

**DB Schema** — a Harness entity that maps to a Git repository containing your changelog file. Defines what schema changes exist and in what order.

**DB Instance** — connects a DB Schema to an actual database via a JDBC connector. One schema can have multiple instances (dev, staging, prod).

**Apply Pipeline** — runs the `DBSchemaApply` step to deploy pending changesets to the database. Liquibase tracks which changesets have already run.

**Rollback Pipeline** — runs the `DBSchemaRollback` step to revert the database to a previous tagged state.

**Migration State** — the Harness view showing every deployed changeset with its deployment tag. Use this to find the rollback tag.

**Rollback Tag** — to rollback a changeset, find the row **below** it in Migration State and copy its tag. This is the database state before that changeset was applied.

---

## Repository Structure

```
dbdevops-tidbits-apply-rollback/
├── .harness/
│   ├── apply-pipeline.yaml     — Apply Schema pipeline
│   └── rollback-pipeline.yaml  — Rollback Schema pipeline (tag as runtime input)
├── sql/
│   └── V1__create_products_table.sql  — base schema (SQL file)
├── changelog.yml               — Liquibase changelog (includes SQL + 2 YAML changesets)
└── k8s/
    └── postgres.yaml           — PostgreSQL deployment on Kubernetes
```

---

## Prerequisites

- A Harness account with the Database DevOps module enabled
- A Kubernetes cluster with a Harness delegate running inside it
- A GitHub connector pointing to this repository
- `kubectl` installed and configured to connect to your cluster

---

## Step 1 — Deploy PostgreSQL

```bash
kubectl create namespace dbdevops-demo
kubectl apply -f k8s/postgres.yaml
kubectl get pods -n dbdevops-demo
```

Verify the pod is in `Running` state.

---

## Step 2 — Create a JDBC Connector

1. Go to **Project Settings → Connectors → + New Connector → JDBC**
2. **Name:** `postgres-dbdevops`
3. **JDBC URL:** `jdbc:postgresql://postgres.dbdevops-demo.svc.cluster.local:5432/appdb`
4. **Username:** `appuser`
5. **Password:** `apppassword`
6. **Delegate:** select your delegate
7. Test and save

---

## Step 3 — Create the DB Schema

1. Go to **Database DevOps → DB Schemas → + Add New DB Schema**
2. **Name:** `ecommerce-products-schema`
3. **Migration Type:** Liquibase Compatible
4. Click **Continue**
5. **Source:** Connect to External Changelog
6. **Connector:** your GitHub connector
7. Click **Continue**
8. **Path to Root Changelog:** `changelog.yml`
9. Click **Add Schema**

---

## Step 4 — Create the DB Instance

1. In the DB Schema, click **+ New**
2. **Name:** `ecommerce-db-instance`
3. **Branch:** `main`
4. **Connector:** `postgres-dbdevops`
5. Click **Add New DB Instance**

---

## Step 5 — Create the Pipelines

**Apply Pipeline:**
1. Go to **Database DevOps → Pipelines → + Create a Pipeline**
2. Use the YAML from `.harness/apply-pipeline.yaml`
3. Update the placeholders:

| Placeholder | Value |
|---|---|
| `YOUR_PROJECT_ID` | Your Harness project identifier |
| `YOUR_ORG_ID` | Your Harness org identifier |
| `YOUR_DOCKER_CONNECTOR` | Your Docker Hub connector identifier (used to pull the Harness Liquibase plugin image) |
| `YOUR_K8S_CONNECTOR` | Your Kubernetes connector identifier |
| `YOUR_DB_SCHEMA_ID` | The DB Schema identifier (e.g., `ecommerceproductsschema`) |
| `YOUR_DB_INSTANCE_ID` | The DB Instance identifier (e.g., `ecommercedbinstance`) |

**Rollback Pipeline:**
1. Create a second pipeline using `.harness/rollback-pipeline.yaml`
2. Update the same placeholders
3. The `tag: <+input>` means Harness will prompt for the rollback tag each time you run it

---

## Step 6 — Run the Demo

**Run 1 — Apply V1 (Base Schema)**
- Run the Apply pipeline
- Verify: `kubectl exec -it <postgres-pod> -n dbdevops-demo -- psql -U appuser -d appdb -c "\d products"`
- Expected: 4 columns (id, name, price DECIMAL, stock_quantity)

**Run 2 — Apply V2 (Add Column)**
- Run the Apply pipeline again
- Expected: 5 columns (+ discount_percentage)

**Run 3 — Apply V3 (Data Type Change)**
- Run the Apply pipeline again
- Expected: price column is now `double precision` (FLOAT)

**Run 4 — Rollback V3 → V2**
- Go to **Migration State** → find the row **below** `change-price-to-float` → copy its tag
- Run the Rollback pipeline → enter that tag → Run
- Expected: price reverts to `DECIMAL(10,2)`, discount_percentage remains

**Run 5 — Rollback V2 → V1**
- Go to **Migration State** → find the row **below** `add-discount-percentage` → copy its tag
- Run the Rollback pipeline → enter that tag → Run
- Expected: discount_percentage removed, back to 4 columns

---

## Resources

- [Harness DB DevOps Onboarding Guide](https://developer.harness.io/database-devops/new-to-database-devops/onboarding-guide)
- [Deploying Database Schema Updates](https://developer.harness.io/database-devops/use-db-devops/deployment-pipeline-configuration/deploying-database-schema)
- [Automated Rollback for Database Schemas](https://developer.harness.io/docs/database-devops/use-database-devops/rollback-for-database-schemas/)
- [Using Rollback Tags with Apply Schema Step](https://developer.harness.io/3k-docs/database-devops/use-database-devops/using-rollback-tags/)
