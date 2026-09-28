<a class="badge" href="https://circleci.com/gh/aimeos/upscheme"><img src="https://circleci.com/gh/aimeos/upscheme.svg?style=shield" alt="Build Status" height="20"></a>
<a class="badge" href="https://coveralls.io/github/aimeos/upscheme"><img src="https://coveralls.io/repos/github/aimeos/upscheme/badge.svg" alt="Coverage Status" height="20"></a>
<a class="badge" href="https://packagist.org/packages/aimeos/upscheme"><img src="https://poser.pugx.org/aimeos/upscheme/license.svg" alt="License" height="20"></a>

# Upscheme: Database schema updates made easy

Easy to use PHP package for updating the database schema of your application
and migrate data between versions.

```bash
composer req aimeos/upscheme
```

**Table of contents**

* [Why Upscheme](#why-upscheme)
* [Database support](#database-support)
* [Integrating Upscheme](#integrating-upscheme)
* [Writing migrations](#writing-migrations)
  * [Naming](#naming-migrations)
  * [Dependencies](#dependencies)
  * [Messages](#messages)
  * [Schemas](#schemas)
  * [Generate from database](#generate-from-database)
* [Database](#database)
  * [Accessing objects](#accessing-objects)
  * [Checking existence](#checking-existence)
  * [Renaming objects](#renaming-objects)
  * [Removing objects](#removing-objects)
  * [Query/modify table rows](#querymodify-table-rows)
  * [Executing custom SQL](#executing-custom-sql)
  * [Database methods](#database-methods)
* [Tables](#tables)
  * [Creating tables](#creating-tables)
  * [Setting table options](#setting-table-options)
  * [Checking table existence](#checking-table-existence)
  * [Changing tables](#changing-tables)
  * [Renaming tables](#renaming-tables)
  * [Dropping tables](#dropping-tables)
  * [Table methods](#table-methods)
* [Columns](#columns)
  * [Adding columns](#adding-columns)
  * [Available column types](#available-column-types)
  * [Column modifiers](#column-modifiers)
  * [Checking column existence](#checking-column-existence)
  * [Changing columns](#changing-columns)
  * [Renaming columns](#renaming-columns)
  * [Dropping columns](#dropping-columns)
  * [Column methods](#column-methods)
* [Foreign keys](#foreign-keys)
  * [Creating foreign keys](#creating-foreign-keys)
  * [Checking foreign key existence](#checking-foreign-key-existence)
  * [Dropping foreign keys](#dropping-foreign-keys)
  * [Foreign key methods](#foreign-key-methods)
* [Sequences](#sequences)
  * [Adding sequences](#adding-sequences)
  * [Checking sequence existence](#checking-sequence-existence)
  * [Dropping sequences](#dropping-sequences)
  * [Sequence methods](#sequence-methods)
* [Indexes](#indexes)
  * [Adding indexes](#adding-indexes)
  * [Checking index existence](#checking-index-existence)
  * [Renaming indexes](#renaming-indexes)
  * [Dropping indexes](#dropping-indexes)
  * [Custom index naming](#custom-index-naming)
* [Customizing Upscheme](#customizing-upscheme)
  * [Adding custom methods](#adding-custom-methods)
  * [Implementing custom columns](#implementing-custom-columns)
* [Upgrade Upscheme](#upgrade-upscheme)



## Why Upscheme

Migrations are like version control for your database. They allow you to get the
exact same state in every installation. Using Upscheme, you get:

* one place for defining tables, columns, indexes, etc. easily
* upgrades from any state in between to the expected schema
* consistent, reliable and hassle-free schema upgrades
* minimal code required for writing migrations
* perfect solution for continuous deployments
* best package for cloud-based PHP applications

Here's an example of a table definition that you can adapt whenever your table
layout must change. Then, Upscheme will automatically add and modify existing
columns and table properties (but don't delete anything for safety reasons):

```php
$this->db()->table( 'test', function( $t ) {
	$t->engine = 'InnoDB';

	$t->id();
	$t->string( 'domain', 32 );
	$t->string( 'code', 64 )->opt( 'charset', 'binary', ['mariadb', 'mysql'] );
	$t->string( 'label', 255 );
	$t->

[...截断...]

int( 'pos' )->default( 0 );
	$t->smallint( 'status' );
	$t->default();

	$t->unique( ['domain', 'code'] );
	$t->index( ['status', 'pos'] );
} );
```

For upgrading relational database schemas, two packages are currently used most
often: Doctrine DBAL and Doctrine migrations. While Doctrine DBAL does a good job
in abstracting the differences of several database implementations, it's API
requires writing a lot of code. Doctrine migrations on the other site has some
drawbacks which make it hard to use in all applications that support 3rd party
extensions.

### Doctrine DBAL drawbacks

The API of DBAL is very verbose and you need to write lots of code even for simple
things. Upscheme uses Doctrine DBAL to offer an easy to use API for upgrading the
database schema of your application with minimal code. For the Upscheme example
above, these lines of code are the equivalent for DBAL in a migration:

```php
$dbalManager = $conn->createSchemaManager();
$from = $manager->createSchema();
$to = $manager->createSchema();

if( $to->hasTable( 'test' ) ) {
	$table = $to->getTable( 'test' );
} else {
	$table = $to->createTable( 'test' );
}

$table->addOption( 'engine', 'InnoDB' );

$table->addColumn( 'id', 'integer', ['autoincrement' => true] );
$table->addColumn( 'domain', 'string', ['length' => 32] );

$platform = $conn->getDatabasePlatform();
if( $platform instanceof \Doctrine\DBAL\Platform\MySQLPlatform
	|| $platform instanceof \Doctrine\DBAL\Platform\MariaDBPlatform
) {
	$table->addColumn( 'code', 'string', ['length' => 64, 'customSchemaOptions' => ['charset' => 'binary']] );
} else {
	$table->addColumn( 'code', 'string', ['length' => 64]] );
}

$table->addColumn( 'label', 'string', ['length' => 255] );
$table->addColumn( 'pos', 'integer', ['default' => 0] );
$table->addColumn( 'status', 'smallint', [] );
$table->addColumn( 'mtime', 'datetime', [] );
$table->addColumn( 'ctime', 'datetime', [] );
$table->addColumn( 'editor', 'string', ['length' => 255] );

$table->setPrimaryKey( ['id'] );
$table->addUniqueIndex( ['domain', 'code'] );
$table->addIndex( ['status', 'pos'] );

foreach( $from->getMigrateToSql( $to, $conn->getDatabasePlatform() ) as $sql ) {
	$conn->executeStatement( $sql );
}
```

### Doctrine Migration drawbacks

Doctrine Migration relies on migration classes that are named by the time they
have been created to ensure a certain order. Furthermore, it stores which migrations
has been executed in a table of your database. There are three major problems that
arise from that:

* dependencies between 3rd party extensions
* tracking changes is out of sync
* data loss when using `down()`

If your application supports 3rd party extensions, these extensions are likely to
add columns to existing tables and migrate data themselves. As there's no way to
define dependencies between migrations, it can get almost impossible to run
migrations in an application with several 3rd party extensions without conflicts.
To avoid that, Upscheme offers easy to use `before()` and `after()` methods in
each migration task where the tasks can define its dependencies to other tasks.

Because Doctrine Migrations uses a database table to record which migration
already has been executed, these records can get easily out of sync in case of
problems. Contrary, Upscheme only relies on the actual schema so it's possible
to upgrade from any state, regardless of what has happend before.

Doctrine Migrations also supports the reverse operations in `down()` methods so
you can roll back migrations which Upscheme does not. Experience has shown that
it's often impossible to roll back migrations, e.g. after adding a new colum,
migrating the data of an existing column and dropping the old column afterwards.
If the migration of the data was lossy, you can't recreate the same state in a
`down()` method. The same is the case if you've dropped a table. Thus, Upscheme
only offers scheme upgrading but no downgrading to avoid implicit data loss.


## Database support

Upscheme us