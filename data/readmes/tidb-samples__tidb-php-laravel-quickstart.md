# Connecting to TiDB with Laravel 

[![Language](https://img.shields.io/badge/Language-PHP-f1e05a.svg)](https://www.php.net/)
[![Framework](https://img.shields.io/badge/Framework-laravel-red.svg)](https://laravel.com)

The following guide will show you how to connect to the TiDB cluster with Laravel and perform basic SQL operations like create, read, update, and delete.

> **Notice:**
>
> TiDB is a MySQL-compatible database, which means you can connect to a TiDB cluster in your application using the familiar driver/ORM framework from the MySQL ecosystem.
>
> The only difference is that if you connect to a TiDB Serverless cluster with public endpoint, you **MUST** [enable TLS connection](#connect-to-tidb-cluster).

## Prerequisites

To complete this guide, you need:

- [PHP](https://www.php.net/) >= 8.0 installed on your machine
- [composer](https://getcomposer.org/) >= 2.5.8 installed on your machine
- [Laravel](https://laravel.com/) >= 10.0 installed on your machine
- [Git](https://git-scm.com/downloads) installed on your machine
- A TiDB cluster running

**If you don't have a TiDB cluster yet, please create one with one of the following methods:**

1. (**Recommend**) [Start up a TiDB Serverless cluster](https://tidbcloud.com/free-trial?utm_source=github&utm_medium=quickstart) instantly with a few clicks on TiDB Cloud.
2. [Start up a TiDB Playground cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) with TiUP CLI on your local machine.

## Getting started

This section demonstrates how to run the sample application code and connect to TiDB with Laravel.

### 1. Clone the repository

Run the following command to clone the sample code locally：

```shell
git clone https://github.com/tidb-samples/tidb-php-laravel-quickstart.git
cd tidb-php-laravel-quickstart
```

### 2. Obtain connection parameters

<details open>
<summary><b>(Option 1) TiDB Serverless</b></summary>

You can obtain the database connection parameters on [TiDB Cloud's Web Console](https://tidbcloud.com/free-trial?utm_source=github&utm_medium=quickstart) through the following steps:

1. Navigate to the [Clusters](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner.
3. In the connection dialog, select `General` from the **Connect With** dropdown and keep the default setting of the **Endpoint Type** as `Public`.
4. If you have not set a password yet, click **Create password** to generate a random password.
5. Copy the connection parameters shown on the code block.

    <div align="center">
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="./static/images/tidb-cloud-connect-dialog-dark-theme.png" width="600">
            <img alt="The connection dialog of TiDB Serverless" src="./static/images/tidb-cloud-connect-dialog-light-theme.png" width="600">
        </picture>
        <div><i>The connection dialog of TiDB Serverless</i></div>
    </div>

</details>

<details>
<summary><b>(Option 2) TiDB Dedicated</b></summary>

You can obtain the database connection parameters on [TiDB Cloud's Web Console](https://tidbcloud.com/console) through the following steps:

1. Navigate to the [Clusters](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Create a traffic filter for the cluster.

    1. Click **Allow Access from Anywhere** to add a new CIDR address rule to allow clients from any IP address to access.
    2. Click **Create Filter** to confirm the changes.

4. Under **Step 2: Download TiDB cluster CA** in the dialog, click **Download TiDB cluster CA** for TLS connection to TiDB clusters.
5. Under **Step 3: Connect with a SQL client** in the dialog, select `General` from the **Connect With** dropdown and select `Public` from the **Endpoint Type** dropdown.
6. Copy the connection parameters shown on the code block.

</details>

<details>
<summary><b>(Option 3) TiDB Self-Hosted</b></summary>

Prepare the following connection parameters for your cluster:

- **host**: The IP address or domain name where the TiDB cluster running (For example: `127.0.0.1`).
- **port**: The port on which your database server is running (Default: `4000`).
- **user**: The name of your database user (Default: `root`).
- **password**: The password of your database user (No password for TiDB Playground by default).

</details>

### 3. Set up the environment variables

<details open>
   <summary><b>(Option 1) TiDB Serverless</b></summary>

1. Make a copy of the `.env.example` file to the `.env` file.
2. Edit the `.env` file, and replace the placeholders for `<host>`, `<user>`, and `<password>` with the copied connection parameters.
3. Modify `DATABASE_ENABLE_SSL` to `true` to enable a TLS connection. (Required for public endpoint)

   ```dotenv
   DB_CONNECTION=mysql
   DB_HOST=<host>
   DB_PORT=4000
   DB_DATABASE=<database>
   DB_USERNAME=<user>
   DB_PASSWORD=<password>
   MYSQL_ATTR_SSL_CA=<CA file Path>
   ```

</details>

<details>
   <summary><b>(Option 2) TiDB Dedicated</b></summary>

1. Make a copy of the `.env.example` file to the `.env` file.
2. Edit the `.env` file, and replace the placeholders for `<host>`, `<user>`, and `<password>` with the copied connection parameters.
3. Modify `DATABASE_ENABLE_SSL` to `true` to enable a TLS connection. (Required for public endpoint)
4. Modify `DATABASE_SSL_CA` to the file path of the CA certificate provided by TiDB Cloud. (Required for public endpoint)

   ```dotenv
   DB_CONNECTION=mysql
   DB_HOST=<host>
   DB_PORT=4000
   DB_DATABASE=<database>
   DB_USERNAME=<user>
   DB_PASSWORD=<password>
   MYSQL_ATTR_SSL_CA=<CA file Path>
   ```

</details>

<details>
   <summary><b>(Option 3) TiDB Self-Hosted</b></summary>

1. Make a copy of the `.env.example` file to the `.env` file.
2. Edit the `.env` file, and replace the placeholders for `<host>`, `<user>`, and `<password>` with the copied connection parameters.

> The TiDB Self-Hosted cluster using non-encrypted connection between TiDB's server and clients by default, SKIP the below steps if your cluster doesn't [enable TLS connections](https://docs.pingcap.com/tidb/stable/enable-tls-between-clients-and-servers#configure-tidb-server-to-use-secure-connections).

3. (Optional) Modify `DATABASE_ENABLE_SSL` to `true` to enable a TLS connection.
4. (Optional) Modify `DATABASE_SSL_CA` to the file path of the trusted CA certificate defined with [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca) option.

   ```dotenv
   DB_CONNECTION=mysql
   DB_HOST=<host>
   DB_PORT=4000
   DB_DATABASE=<database>
   DB_USERNAME=<user>
   DB_PASSWORD=<password>
   ```

</details>

### 4. Run the sample code

Import the table into TiDB.

```shell
php artisan migrate
```

If the import is successful, the console will output the import detail info.

**Expected execution output:**

```
  INFO  Preparing migrations.

  Creating migration table .............................................................................................................. 833ms DONE

  INFO  Running migrations.

  2014_10_12_000000_create_users_table ................................................................................................ 6,915ms DONE
  2014_10_12_100000_create_password_reset_tokens_table ................................................................................ 6,940ms DONE
  2019_08_19_000000_create_failed_jobs_table .......................................................................................... 6,993ms DONE
  2019_12_14_000001_create_personal_access_tokens_table .............................................................................. 13,056ms DONE
  2023_08_22_054837_create_products_table ............................................................................................... 605ms DONE

```

Run the following command to execute the sample code:

```shell
php artisan serve
```

If the connection is successful, the console will output the version of the TiDB cluster.

**Expected execution output:**

```
  INFO  Server running on [http://127.0.0.1:8000].

  Press Ctrl+C to stop the server
```

## Example codes

### Connect to TiDB cluster

The following code use the environment variables (stored in the `.env` file) as the connection options to establish a database connection with the TiDB cluster:

```dotenv
DB_CONNECTION=mysql
DB_HOST=<TiDB URL>
DB_PORT=<TiDB Port>
DB_DATABASE=<Database Name>
DB_USERNAME=<Username>
DB_PASSWORD=<Password>
MYSQL_ATTR_SSL_CA=<CA File Path>
```

<details open>
   <summary><b>For TiDB Serverless</b></summary>

To connect **TiDB Serverless** with the public endpoint, please set up the environment variable `MYSQL_ATTR_SSL_CA` to CA certificate file path to enable TLS connection. You can download CA certificate from [TiDB Cloud Web Console](#3-obtain-connection-parameters).

</details>

<details>
   <summary><b>For TiDB Dedicated</b></summary>

To connect **TiDB Dedicated** with the public endpoint, please set up the environment variable `MYSQL_ATTR_SSL_CA` to CA certificate file path to enable TLS connection. You can download CA certificate from [TiDB Cloud Web Console](#3-obtain-connection-parameters).

</details>


**Example 1: Connect to TiDB Serverless with public endpoint**

**MUST** enable SSL (TLS) connection via set the `MYSQL_ATTR_SSL_CA` parameter of `.env` file.

```dotenv
DB_CONNECTION=mysql
DB_HOST=<TiDB URL>
DB_PORT=<TiDB Port>
DB_DATABASE=<Database Name>
DB_USERNAME=<Username>
DB_PASSWORD=<Password>
MYSQL_ATTR_SSL_CA=<CA File Path>
```

**Example 2: Connect to local TiDB playground cluster**

```dotenv
DB_CONNECTION=mysql
DB_HOST=<TiDB URL>
DB_PORT=<TiDB Port>
DB_DATABASE=<Database Name>
DB_USERNAME=<Username>
DB_PASSWORD=<Password>
```

### Insert data

The following query creates a single `Product` with three fields and redirect to product edit view:

```php
public function store(Request $request){
    $newPost = Product::create([
        'title' => $request->title,
        'short_notes' => $request->short_notes,
        'price' => $request->price
    ]);

    return redirect('product/' . $newPost->id . '/edit');
}
```

For more information, refer to [Insert Data](https://docs.pingcap.com/tidbcloud/dev-guide-insert-data).

### Query data

The following query a single `Product` record by ID and redirect to product view:

*app\Http\Controllers\ProductController.php* `show` method
```php
public function show(Product $product){
    $product = Product::find($product->id);
    return view('product.show', [
        'product' => $product,
    ]);
}
```

For more information, refer to [Query Data](https://docs.pingcap.com/tidbcloud/dev-guide-get-data-from-single-table).

### Update data

The following query updated a single `PHP` record by ID:

```php
public function update(Request $request, Product $product){
    $product->update([
        'title' => $request->title,
        'short_notes' => $request->short_notes,
        'price' => $request->price
    ]);

    return redirect('product/' . $product->id . '/edit');
}}
```

For more information, refer to [Update Data](https://docs.pingcap.com/tidbcloud/dev-guide-update-data).

### Delete data

The following query deletes a single `Product` record:

```php
public function destroy(Product $product){
    $product->delete($product->id);
    return redirect('product/');
}
```

For more information, refer to [Delete Data](https://docs.pingcap.com/tidbcloud/dev-guide-delete-data).

## What's next

- Explore the real-time analytics feature on the [TiDB Cloud Playground](https://play.tidbcloud.com/real-time-analytics).
- Read the [TiDB Developer Guide](https://docs.pingcap.com/tidbcloud/dev-guide-overview) to learn more details about application development with TiDB.
    - [HTAP Queries](https://docs.pingcap.com/tidbcloud/dev-guide-hybrid-oltp-and-olap-queries)
    - [Transaction](https://docs.pingcap.com/tidbcloud/dev-guide-transaction-overview)
    - [Optimizing SQL Performance](https://docs.pingcap.com/tidbcloud/dev-guide-optimize-sql-overview)
