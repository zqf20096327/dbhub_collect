# qDBManager

[![CI](https://github.com/denisbilli/qDBManager/actions/workflows/ci.yml/badge.svg)](https://github.com/denisbilli/qDBManager/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Qt](https://img.shields.io/badge/Qt-5.12%20%7C%206-41cd52.svg)](https://www.qt.io/)
[![C++](https://img.shields.io/badge/C%2B%2B-11-00599c.svg)](https://isocpp.org/)

A small ORM / entity manager for the Qt Framework. It maps `QObject` subclasses
to SQLite tables using Qt's meta-object system, so an entity is declared once —
as properties — and is then usable from C++, from QML, and as a database row.

qDBManager is deliberately narrow: no query DSL, no lazy loading graph, no code
generation step. It exists for Qt applications that want CRUD without pulling in
a full ORM.

```cpp
QDBManager *dbm = QDBManager::create("app", "QSQLITE");
QDBManager::register_entity<Person>();

dbm->openDB("app.sqlite");
dbm->createTable<Person>();

Person person;
person.setName("Leonard");
person.setSurname("Hofstadter");
dbm->insertOrUpdate<Person>(&person);   // person.getId() is now set

CriteriaBuilder criteria;
criteria.insertGrtOrEq("age", 30);
QList<Person *> adults = dbm->find<Person>(criteria, "surname");
```

## Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Declaring an entity](#declaring-an-entity)
- [Working with data](#working-with-data)
- [Querying](#querying)
- [Transactions](#transactions)
- [Schema evolution](#schema-evolution)
- [Contexts and connections](#contexts-and-connections)
- [How SQL is built](#how-sql-is-built)
- [Adding a backend](#adding-a-backend)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Requirements

| | |
|---|---|
| Qt | 5.12 or newer, including Qt 6 |
| Modules | `Qt::Core`, `Qt::Sql` (plus `Qt::Test` to build the suite) |
| Compiler | C++11 |
| Driver | `QSQLITE` |
| Build | CMake 3.16+, or qmake |

## Installation

### CMake — as a subproject

```cmake
add_subdirectory(third_party/qDBManager)
target_link_libraries(myapp PRIVATE qDBManager::qDBManager)
```

### CMake — with FetchContent

```cmake
include(FetchContent)
FetchContent_Declare(qDBManager
    GIT_REPOSITORY https://github.com/denisbilli/qDBManager.git
    GIT_TAG v0.2.0)
FetchContent_MakeAvailable(qDBManager)

target_link_libraries(myapp PRIVATE qDBManager::qDBManager)
```

### CMake — installed

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cmake --install build --prefix /usr/local
```

```cmake
find_package(qDBManager 0.2 REQUIRED)
target_link_libraries(myapp PRIVATE qDBManager::qDBManager)
```

### qmake

```pro
include(third_party/qDBManager/qdbmanager.pri)
```

### Build options

| Option | Default | Effect |
|---|---|---|
| `QDBMANAGER_BUILD_TESTS` | `ON` when top level | Build and register the `ctest` suite |
| `QDBMANAGER_BUILD_EXAMPLES` | `ON` when top level | Build `examples/basic` |
| `QDBMANAGER_INSTALL` | `ON` when top level | Generate install and package-config rules |
| `BUILD_SHARED_LIBS` | `OFF` | Build a shared library instead of a static one |

## Declaring an entity

An entity is a `BaseEntity` subclass whose columns are declared with macros. The
macros expand to `Q_PROPERTY` and `Q_CLASSINFO`, so everything the manager needs
is available through the meta-object at runtime.

```cpp
#include <qdbmanager/qdbmanager.h>

class Person : public BaseEntity
{
    Q_OBJECT
    Q_TABLENAME(PERSON)

    Q_FIELD_2(QString, Name, name)
    Q_FIELD_2(QString, Surname, surname)
    Q_FIELD_2(int, Age, age)
    Q_TRANSIENT_FIELD_2(QString, ScratchPad, scratchPad)
    Q_INDEX(surname)

public:
    explicit Person(QObject *parent = nullptr) : BaseEntity(parent) {}

    Q_ATTR_2(QString, Name)
    Q_ATTR_2(QString, Surname)
    Q_ATTR_2(int, Age)
    Q_ATTR_2(QString, ScratchPad)

signals:
    void changedName(QString value);
    void changedSurname(QString value);
    void changedAge(int value);
    void changedScratchPad(QString value);
};
```

`Q_FIELD_2(type, Accessor, property)` declares the property `property` backed by
`getAccessor()` / `setAccessor()`; `Q_ATTR_2` writes those two accessors for you.
`BaseEntity` already supplies `id` (the primary key, filled in on insert) and a
read-only `guid`.

### Macro reference

| Macro | Purpose |
|---|---|
| `Q_TABLENAME(table)` | Backing table name. Mandatory. |
| `Q_FIELD(type, name)` | Persisted property using `get_name` / `set_name` accessors you write. |
| `Q_FIELD_2(type, Accessor, name)` | Persisted property using `getAccessor` / `setAccessor`. |
| `Q_ATTR_2(type, Accessor)` | Generates the accessor pair for `Q_FIELD_2`. |
| `Q_TRANSIENT_FIELD(_2)` | Property exposed to QML but never written to the database. |
| `Q_READONLY_TRANSIENT_FIELD(_2)` | Read-only, non-persisted property. |
| `Q_FK_FIELD(type, name, parentTable, parentColumn, cascade)` | Persisted foreign key. |
| `Q_FK_FIELD_2(type, Accessor, name, parentTable, parentColumn, cascade)` | Same, `Q_FIELD_2` convention. |
| `Q_INDEX(column)` | Single-column index. |
| `Q_INDEX_MUL(a, b)` | Multi-column index. |

Cascade modes: `Q_CASCADE_ALL`, `Q_CASCADE_UPD`, `Q_CASCADE_DEL`,
`Q_CASCADE_UPD_RESTRICT_DEL`. SQLite enforces foreign keys per connection;
qDBManager turns the pragma on when it opens the database.

Supported property types map to SQLite as follows:

| Qt type | Column type |
|---|---|
| `int`, `uint`, `short`, `bool`, `qlonglong`, `qulonglong` | `INTEGER` |
| `double`, `float` | `REAL` |
| `QString`, `QDate`, `QTime`, `QDateTime`, `QUrl`, `QUuid` | `TEXT` |
| `QByteArray` | `BLOB` |

A property of any other type is ignored rather than guessed at.

## Working with data

```cpp
QDBManager::register_entity<Person>();   // before any read
dbm->openDB("app.sqlite");
dbm->createAllTables();                  // every registered entity
```

Registration is what lets the manager turn a result row back into the right C++
type; reads return empty lists until it has happened.

```cpp
Person person;
person.setName("Leonard");

dbm->insertOrUpdate<Person>(&person);  // insert, then updates on later calls
dbm->insert<Person>(&person);          // insert without the update-first probe
dbm->update("PERSON", &person);        // always update

Person *loaded = dbm->findById<Person>(person.getId());
QList<Person *> all = dbm->listAll<Person>("surname");

dbm->removeById<Person>(person.getId());
```

`insertOrUpdate` writes the generated primary key back into the entity and
clears its dirty flag. Entities returned by `find`, `listAll`, `findById` and
`query` are heap-allocated and unparented: the caller owns them.

## Querying

Conditions are built with `CriteriaBuilder`, which stores column, operator and
value separately and never renders a value into SQL text.

```cpp
CriteriaBuilder criteria;
criteria.insert("surname", "Hofstadter")     // =
        .insertNotEq("active", false)        // <>
        .insertGrtOrEq("age", 30)            // >=
        .insertLess("age", 65)               // <
        .insertLike("name", "Leo%")          // LIKE
        .insertIn("city", QVariantList() << "Pasadena" << "Omaha")
        .insertIsNotNull("email");

QList<Person *> found = dbm->find<Person>(criteria, "surname", /*desc=*/false);
```

Conditions are combined with `AND`. For anything more involved, pass SQL with
your own bindings:

```cpp
QList<Person *> found = dbm->query<Person>(
    "SELECT * FROM PERSON WHERE age BETWEEN ? AND ?",
    QVariantList() << 30 << 40);

QVariantList names = dbm->one_column_query("SELECT name FROM PERSON");
```

A compact string form is available for simple cases and is parsed into criteria,
never concatenated:

```cpp
QList<Person *> found = dbm->find<Person>("age>=30,surname=Hofstadter");
```

## Transactions

```cpp
dbm->beginTransaction();
// ...
dbm->commitTransaction();   // or dbm->rollbackTransaction();
```

Named savepoints nest:

```cpp
dbm->beginTransaction("importBatch");
// ...
dbm->rollbackTransaction("importBatch");
```

A savepoint name is an SQL identifier, so it is validated and rejected if it is
not a bare name.

## Schema evolution

`syncEntityTable()` — `sync<T>()` — compares the entity with the table and adds
the columns that are missing. The entity always wins; nothing is dropped or
retyped, and existing rows get `NULL` in the new columns.

```cpp
dbm->sync<Person>();
```

For anything beyond adding columns, write a migration with `execute()`.

## Contexts and connections

`create()` returns one manager per named context, and the context name is also
the `QSqlDatabase` connection name, so several databases can be open at once:

```cpp
QDBManager *app   = QDBManager::create("app");
QDBManager *cache = QDBManager::create("cache");

app->openDB("app.sqlite");
cache->openDB("cache.sqlite");
```

Calling `create()` again with the same name returns the same manager. Methods
that need an open connection will open one and close it again if they had to;
opening the database yourself once is both faster and clearer.

Failures are reported through a signal rather than thrown:

```cpp
connect(dbm, &QDBManager::error, this, &MyClass::onDatabaseError);
```

## How SQL is built

Values and identifiers are handled differently, on purpose.

**Values** — every value that reaches the database is passed to the driver as a
bound parameter. Entity fields, criteria operands and `IN` lists are never
rendered into SQL text, so quotes, semicolons and comment markers inside data
are stored and returned verbatim.

**Identifiers** — table names, column names, `ORDER BY` fields and savepoint
names cannot be bound by any SQL driver. They are checked against
`QDBManager::isValidIdentifier()` (`[A-Za-z_][A-Za-z0-9_]*`) and quoted before
being interpolated. Anything that fails the check is refused, and the call
returns empty or `false` after emitting `error()`.

`execute()`, `query<T>()`, `entityComplexQuery()` and `one_column_query()` take
raw SQL by design. Their bindings parameter is the supported way to pass values
into them; string concatenation there is yours to get right.

## Adding a backend

`QDBManager` is abstract. A backend subclasses it and supplies the dialect —
query templates, cascade clauses, transaction syntax — plus `openDB()`.
`qSqlite` (`include/qdbmanager/interfaces/qsqlite.h`) is around a hundred lines
and is the reference to copy. Register the new driver id in `QDBManager::create()`.

## Limitations

- SQLite is the only bundled backend.
- Conditions are joined with `AND`; `OR` and nested groups need raw SQL.
- There is no relationship graph: foreign keys are enforced by the database, and
  parent/child navigation is opt-in through `Q_CHILDREN_LIST` / `Q_FOREIGN_KEY_OBJ`.
- `sync<T>()` only adds columns.
- A manager is not thread-safe; give each thread its own context, as Qt's SQL
  module requires.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports, backends and tests are all
welcome; the test suite lives in `tests/` and runs with `ctest`.

## License

MIT — see [LICENSE](LICENSE).
