# Database Access Object wrapper for PHP and PDO in a single class

PdoOne. It's a simple wrapper for PHP's PDO library compatible with SQL Server (2008 R2 or higher), MySQL (5.7 or
higher) and Oracle (12.1 or higher).

This library tries to **work as fast as possible**. Most of the operations are simple string/array managements and work
in the bare metal of the PDO library, but it also allows to create an ORM using the extension [eftec/PdoOneORM](https://github.com/EFTEC/PdoOneORM).

[![Packagist](https://img.shields.io/packagist/v/eftec/PdoOne.svg)](https://packagist.org/packages/eftec/PdoOne)
[![Total Downloads](https://poser.pugx.org/eftec/PdoOne/downloads)](https://packagist.org/packages/eftec/PdoOne)
[![Maintenance](https://img.shields.io/maintenance/yes/2025.svg)]()
[![composer](https://img.shields.io/badge/composer-%3E1.6-blue.svg)]()
[![php](https://img.shields.io/badge/php-7.4-green.svg)]()
[![php](https://img.shields.io/badge/php-8.4-green.svg)]()
[![CocoaPods](https://img.shields.io/badge/docs-70%25-yellow.svg)]()

Turn this

```php
$stmt = $pdo->prepare("SELECT * FROM myTable WHERE name = ?");
$stmt->bindParam(1,$_POST['name'],PDO::PARAM_STR);
$stmt->execute();
$result = $stmt->get_result();
$products=[];
while($row = $result->fetch_assoc()) {
  $product[]=$row; 
}
$stmt->close();
```

into this

```php
$products=$pdoOne
    ->select("*")
    ->from("myTable")
    ->where("name = ?",[$_POST['name']]) 
    ->toList();
```

or using the ORM (using [eftec/PdoOneORM](https://github.com/EFTEC/PdoOneORM) library)

```php
ProductRepo // this class was generated with echo $pdoOne()->generateCodeClass(['Product']); or using the cli.
    ::where("name = ?",[$_POST['name']])
    ::toList();
```

# Table of contents

<!-- TOC -->
* [Database Access Object wrapper for PHP and PDO in a single class](#database-access-object-wrapper-for-php-and-pdo-in-a-single-class)
* [Table of contents](#table-of-contents)
  * [Examples](#examples)
  * [Installation](#installation)
    * [Install (using composer)](#install-using-composer)
    * [Install (manually)](#install-manually)
  * [How to create a Connection?](#how-to-create-a-connection)
    * [OCI](#oci)
  * [How to run a SQL command?](#how-to-run-a-sql-command)
    * [1. Running a raw query](#1-running-a-raw-query)
    * [2. Running a native PDO statement](#2-running-a-native-pdo-statement)
    * [3. Running using the query builder](#3-running-using-the-query-builder)
    * [4. Running using an ORM](#4-running-using-an-orm)
    * [5. Run a query with a different mode](#5-run-a-query-with-a-different-mode)
  * [How to work with Date values?](#how-to-work-with-date-values)
  * [How to run a transaction?](#how-to-run-a-transaction)
  * [Custom Queries](#custom-queries)
    * [tableExist($tableName)](#tableexisttablename)
    * [statValue($tableName,$columnName)](#statvaluetablenamecolumnname)
    * [columnTable($tablename)](#columntabletablename)
    * [foreignKeyTable($tableName)](#foreignkeytabletablename)
    * [createTable($tableName,$definition,$primaryKey=null,$extra='',$extraOutside='')](#createtabletablenamedefinitionprimarykeynullextraextraoutside)
    * [tableSorted($maxLoop = 5, $returnProblems = false, $debugTrace = false)](#tablesortedmaxloop--5-returnproblems--false-debugtrace--false)
    * [validateDefTable($pdoInstance,$tablename,$defTable,$defTableKey)](#validatedeftablepdoinstancetablenamedeftabledeftablekey)
    * [foreignKeyTable](#foreignkeytable)
  * [Query Builder (DQL)](#query-builder-dql)
    * [select($columns)](#selectcolumns)
    * [count($sql,$arg='*')](#countsqlarg)
    * [min($sql,$arg='*')](#minsqlarg)
    * [max($sql,$arg='*')](#maxsqlarg)
    * [sum($sql,$arg='*')](#sumsqlarg)
    * [avg($sql,$arg='*')](#avgsqlarg)
    * [distinct($distinct='distinct')](#distinctdistinctdistinct)
    * [from($tables)](#fromtables)
    * [where($where,[$arrayParameters=array()])](#wherewherearrayparametersarray)
      * [Where() without parameters.](#where-without-paramet

[...截断...]

ers)
      * [Where() with parameters defined by an indexed array.](#where-with-parameters-defined-by-an-indexed-array)
      * [Where() using an associative array](#where-using-an-associative-array)
      * [Where() using an associative array and named arguments](#where-using-an-associative-array-and-named-arguments)
      * [Examples of where()](#examples-of-where)
    * [order($order)](#orderorder)
    * [group($group)](#groupgroup)
    * [having($having,[$arrayParameters])](#havinghavingarrayparameters)
    * [End of the chain](#end-of-the-chain)
      * [runGen($returnArray=true)](#rungenreturnarraytrue)
      * [toList($pdoMode)](#tolistpdomode)
* [toPdoStatement($pdoMode)](#topdostatementpdomode)
* [fetchLoop($callable,$pdoMode)](#fetchloopcallablepdomode)
      * [toMeta()](#tometa)
      * [toListSimple()](#tolistsimple)
      * [toListKeyValue()](#tolistkeyvalue)
      * [toResult()](#toresult)
      * [firstScalar($colName=null)](#firstscalarcolnamenull)
      * [first()](#first)
      * [last()](#last)
      * [sqlGen()](#sqlgen)
  * [Query Builder (DML)](#query-builder-dml)
    * [insert($table,$schema,[$values])](#inserttableschemavalues)
    * [insertObject($table,[$declarativeArray],$excludeColumn=[])](#insertobjecttabledeclarativearrayexcludecolumn)
    * [update($$table,$schema,$values,[$schemaWhere],[$valuesWhere])](#updatetableschemavaluesschemawherevalueswhere)
    * [delete([$table],[$schemaWhere],[$valuesWhere])](#deletetableschemawherevalueswhere)
  * [Cache](#cache)
    * [How to configure it?](#how-to-configure-it)
    * [Example using apcu](#example-using-apcu)
  * [Sequence](#sequence)
    * [Creating a sequence](#creating-a-sequence)
    * [Creating a sequence without a table.](#creating-a-sequence-without-a-table)
    * [Using the sequence](#using-the-sequence)
  * [Fields](#fields)
  * [Encryption](#encryption)
  * [How to debug and trace errors in the database?](#how-to-debug-and-trace-errors-in-the-database)
    * [Setting the log level](#setting-the-log-level)
    * [Throwing errors](#throwing-errors)
    * [Getting the last Query](#getting-the-last-query)
    * [Generating a log file](#generating-a-log-file)
  * [CLI](#cli)
    * [Run as cli](#run-as-cli)
    * [Run as CLI interative](#run-as-cli-interative)
      * [Examples](#examples-1)
    * [Run CLI to generate repository classes.](#run-cli-to-generate-repository-classes)
    * [cli-classcode](#cli-classcode)
    * [cli-selectcode](#cli-selectcode)
    * [cli-arraycode](#cli-arraycode)
    * [cli-json](#cli-json)
    * [cli-csv](#cli-csv)
    * [UI](#ui)
    * [How to run the UI?](#how-to-run-the-ui)
    * [DDL  Database Design Language](#ddl--database-design-language)
    * [Nested Operators](#nested-operators)
    * [DQL Database Query Language](#dql-database-query-language)
    * [DML Database Model Language](#dml-database-model-language)
    * [Validate the model](#validate-the-model)
    * [Recursive](#recursive)
      * [recursive()](#recursive-1)
      * [getRecursive()](#getrecursive)
      * [hasRecursive()](#hasrecursive)
  * [Benchmark (mysql, estimated)](#benchmark-mysql-estimated)
  * [migration from 3 to 4](#migration-from-3-to-4)
  * [Error FAQs](#error-faqs)
    * [Uncaught Error: Undefined constant eftec\_BasePdoOneRepo::COMPILEDVERSION](#uncaught-error-undefined-constant-eftec_basepdoonerepocompiledversion)
  * [Changelist](#changelist)
<!-- TOC -->

## Examples

| [ExampleTicketPHP](https://github.com/jorgecc/ExampleTicketPHP)                                                                                                                                                                                                        | [Example cupcakes](https://github.com/EFTEC/example.cupcakes)                                                                     | [Example Search](https://github.com/EFTEC/example-search)                                                                              | [Example Different Method](http