import pymysql

# Connect to Huawei Cloud RDS MySQL
conn = pymysql.connect(
    host="your-rds-endpoint.huaweicloud.com",
    port=3306,
    user="your-username",
    password="your-password",
    database="your-db-name"
)

with conn.cursor() as cursor:
    cursor.execute("SELECT VERSION()")
    print("Database version:", cursor.fetchone()[0])
conn.close()
