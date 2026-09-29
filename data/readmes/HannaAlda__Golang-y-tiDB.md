# Golang-y-tiDB
Una mancuerna perfecta para hacer un buen PIN.
Pasos a seguir para un buen PINaje: Desarrollo de aplicacion para go-sql-driver/mysql

1. Inicie un clúster pseudo TiDB en su almacenamiento local:
   docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0

2. En el shell de SQL, cree la base de go_mysqldatos que usará su aplicación:
   CREATE DATABASE NOMBREDATABASE;

3. Cree un usuario SQL para la aplicación:
   CREATE USER <username> IDENTIFIED BY <password>;

   Recuerde: nombre de usuario y la contraseña. Los utilizará en el código de su aplicación al inicializar el proyecto.

4. Otorgue los permisos necesarios al usuario de SQL que acaba de crear:
   GRANT ALL ON go_mysql.* TO <username>;

5. El código main.go usa go-sql-driver/mysql para asignar los métodos de Golang a las operaciones de SQL. 
   (Revisar los comentarios escritos en el código)

6. Puede guardar el código de la aplicación de ejemplo como un archivo Golang nombrado main.goen su máquina local.

7.  Actualice los parámetros de conexión y conéctese a TiDB
    En el main.go archivo anterior, reemplace la cadena pasada sql.Open()con la cadena de conexión que obtuvo al crear la base de datos. La sql.Open()llamada a la función debe ser similar a la siguiente:

    db, err := sql.Open("mysql", "{user}:{password}@{globalhost}:{puerto}/go_mysql?charset=utf8mb4")
    

    Ejemplo: 
            user/ USER/ username     :  Hanna/otro/alguien
            password / contraseña    :  2456WRTYOPK678 / alguna contraseña
            puerto                   :  4000 / 3606 / 8000 / 26257 / cualquier puerto activo

8.  Inicialice el módulo go-sql-driver/mysql:  
    go mod init mysql-driver-demo    

9.  Ejecute el main.gocódigo:
    go run main.go

10. Espere un resultado como el siguiente:
    2 2 122.00
    3 2 72.50
    Alice 72.50
    Alice 122.00

11. Desde Shell mySQL:
    
    mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| django             |
| go_mysql           |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
6 rows in set (0.01 sec)

mysql> USE go_mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
+--------------------+
| Tables_in_go_mysql |
+--------------------+
| customer           |
| orders             |
+--------------------+
2 rows in set (0.00 sec)
mysql> SELECT * FROM customer;
+-----+----------+--------+
| cid | name     | gender |
+-----+----------+--------+
|   1 | Ben      | Male   |
|   2 | Alice    | Female |
|   3 | Peter    | Male   |
|   4 | Enzo     | Male   |
|   5 | Ben      | Male   |
|   6 | Alice    | Female |
|   7 | Peter    | Male   |
|   8 | Sthefano | Male   |
|   9 | Ben      | Male   |
|  10 | Alice    | Female |
|  11 | Peter    | Male   |
|  12 | Sthefano | Male   |
+-----+----------+--------+
12 rows in set (0.00 sec)

NOTA: Lo que se muestra en el resultado de Shell mySQL, es despues de varios (3)  RUN en el código Golang, además hay una inserción con comando (cid:4 , Enzo, Male) y en las dos ultimas RUN, se agrego a Sthefano.
    
