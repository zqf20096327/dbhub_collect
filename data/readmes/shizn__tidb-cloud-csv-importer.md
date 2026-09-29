# TiDB Cloud CSV Importer
This tool helps you easily import any *.csv files to TiDB Cloud.

## Prerequisite
- Docker
- Python 3
- MySQL CLI: `sudo apt install mysql-client`
- mysqldump CLI. This is also included in the mysql-client above.

## How to use
1. Open `.env` file and put actual values there, all these can be found in the TiDB Cloud Cluster Connect Window.
    ```env
    TIDB_USERNAME='{Your TIDB Cloud USERNAME}'
    TIDB_HOST={Your TIDB Cloud Host}
    TIDB_SSL_CA={Your Cert Path}
    TIDB_PASSWORD={Your TiDB Cloud Password}
    DB_NAME={The new database name which stores all imported data}
    ```
2. (Optional) Remove sample csv files in csv folder(`./csv/sp500_*.csv`), and paste your own csv files into the `./csv/` folder. 

3. In your terminal window, start a local MariaDB server with `docker-compose up`.

4. In your terminal window, run `sudo ./import.sh`.
