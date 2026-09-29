## README

**Prerequisites:** You must have Java (preferably version 17) and Maven installed. If you have a version of Java other than 17 installed, you will need to edit the pom.xml file and update the target version for <code>maven.compiler.source</code> and <code>maven.compiler.target</code>.

This app will create mocked up data in various formats and including JSON data, also in various formats. 
Before running this code, a database and table must be created using the following:

<pre>
CREATE DATABASE db_name;
USE db_name
CREATE TABLE test_table(
    id INT unsigned auto_increment not null,
    field1 SMALLINT,
    field2 INT,
    field3 VARCHAR(20),
    field4 FLOAT,
    field5 DECIMAL(6,2),
    field6 JSON,
    primary key (id)
);
</pre>
Note that the database name does not matter as it will be specified in the parameters file. 
Once the database is created, edit the values in <code>resources/system.properties</code> to match the database host, port, and name as well as the login and password.
These are stored in plaintext and this file should be protected if used on a production database.

To use the code, you must first compile it using __maven__ as follows. Change directory to the project root (the one above src) and issue the following command:

<pre>mvn package</pre>

To run the code, issue the following (also from the project root directory):

<pre>java -DPROP_FILE=resources/system.properties -DNUM_RECORDS=5000 -jar target/tidb-data-mock-1.1-jar-with-dependencies.jar</pre>

Replace the number after <code>-DNUM_RECORDS=</code> with the number of records to insert. You can also specify a different path to the properties file in the <code>PROP_FILE</code> parameter.