# How to use this template

This is the template for deploying TiDB on Cloudflare Workers using prisma.

## Pre-requisites

- Free TiDB Cloud account and a Serverless Tier on TiDB Cloud, See [TiDB Cloud Quick Start](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) for more details.
- Free Cloudflare Workers account
- Free GitHub account
- Node.js & NPM installed

## Step 1: Install dependencies

```
npm install -D prisma typescript wrangler
```

## Step 2: Using the template

Click the "Use this template" button to create a new repository from this template. Assume that your new repository is named `prisma-tidb-cloudflare`.

Get your project with git:

```
git clone git@github.com:{username}/prisma-tidb-cloudflare.git
cd prisma-tidb-cloudflare
```

## Step 3: Change the prisma/schema.prisma

You need to change the schema.prisma according to the table you want to query. `prisma/schema.prisma` is an example for you.

As for the details about schema, see [Prisma official doc](https://www.prisma.io/docs/concepts/database-connectors/mysql#type-mapping-between-mysql-to-prisma-schema).

Then push the changes to your repository.

```
git add prisma
git commit -m "change schema"
git push
```

## Step 4: Import your Project into the Prisma Data Platform

With Cloudflare Workers, you can't directly access your database because there is no TCP support. Fortunately, Prisma has your back with the Data Proxy.

1. To get started, sign up for a free [Prisma Data Platform account](https://cloud.prisma.io/).
2. Click **New Project** and then select **Import a Prisma repository**.
3. Fill in the repository and project details, and click **Next**.
![img.png](pic/project.png)
4. Fill in the **Connection string** with this pattern `mysql://USER:PASSWORD@HOST:PORT/DATABASE?sslaccept=strict`. You can find the connection information in your [TiDB Cloud dashboard](https://tidbcloud.com/console/clusters).
5. Under **Location**, select a Data Proxy location that is geographically close to your TiDB Cloud cluster location.
6. You need not enable **Static IPs** if you use serverless tier which is accessible from any IP address.
![img.png](pic/env.png)
7. After you click **Create Project**. You'll be greeted with a new connection string that starts with `prisma://.` You must copy this connection string and save it for later.
![img.png](pic/connection.png)

## Step 5: Set the Data Proxy Connection string in your environment

Add the Data Proxy connection string to your local environment .env file.

```
prisma://aws-us-east-1.prisma-data.com/?api_key=•••••••••••••••••"
```

Add the connection string in the wrangler.toml file. Create if you don't have one.

```
name = "prisma-mongodb-cloudflare"  # Change this to your project name
main = "src/main.ts"
compatibility_date = "2022-11-30"

[vars]
DATABASE_URL = "prisma://aws-us-east-1.prisma-data.com/?api_key=•••••••••••••••••"
```

> Note
> Don't push your DATABASE_URL to public repository.


## Step 6: Generate a Prisma Client

Next, you'll generate a Prisma Client that connects through the [Data Proxy](https://www.prisma.io/docs/data-platform/data-proxy) over HTTP.

```
npx prisma generate --data-proxy 
```

## Step 7: Develop the Cloudflare Worker function

You can find the example in `src/index.ts`. This example will get the table according to your URL parameter.

You can also change the code according to your needs.

You can also push the changes of `src/index.ts` to your repository.

## Step 8: Publish to Cloudflare Workers

You're now ready to deploy to Cloudflare Workers. Run the following command:

```
npx wrangler publish
```

## Step 9: Try your Cloudflare Workers

Go to [cloudflare dashboard](https://dash.cloudflare.com/), and find your worker. You can find the URL of your worker in the overview page.

Visit the URL with your table name: `https://your-worker-url/?table={table_name}`, you will get the result from the corresponding TiDB table.

## Step 10: How to update

If you just want to update `src/index.ts`. Just publish again after the change.

If you want to add new model (table) in `prisma/schema.prisma`. You need to:

1. Push the changes to your repository. `git add prisma && git commit -m "add new model" && git push`
2. Generate the Prisma Client again. `npx prisma generate --data-proxy`
3. Publish the cloudflare worker again. `npx wrangler publish`
