<div align="center">
  <img src="./docs/imgs/model-logo-bg.png" alt="Model logo" width="140px">
</div>
<br>
<p align="center">
<a href="https://github.com/el1s7/model/actions/workflows/tests.yml">
  <img src="https://github.com/el1s7/model/actions/workflows/tests.yml/badge.svg?branch=master&amp;event=push" alt="Tests">
</a>
<a href="https://pypi.org/project/model-py">
    <img src="https://img.shields.io/pypi/v/model-py?color=34D058" alt="PyPI version">
</a>
<!-- Add downloads badge later
<a href="https://pypi.org/project/model-py">
    <img src="https://static.pepy.tech/badge/model-py/month" alt="PyPI Downloads">
</a>
-->
</p>

# Model
A minimal Python ORM for **MariaDB**/**MySQL** and **SQLite**. Explicit, predictable, and made for humans.

## Motivation

Many ORMs try to abstract SQL away entirely, introducing their own query languages and complex concepts that force you to spend time learning “their way” before getting productive.

**Model** takes a different approach: it embraces native type definitions and SQL instead of hiding them behind unnecessary abstractions. 

## Features
- Intuitive and simple to use.
- Advanced **static type checking** for fool-proof schema definition. (*Fun fact: the `Column` method has 73 typing @overloads*.) 
- Fast and predictable performance, with no hidden bloated queries slowing down your app.
- One command for automatic schema updates. Safe, rapid and versionless schema evolution. 
- One command to automatically generate models from your existing tables.
- Primarily written by hand.
<div align="center">
<img 
    alt="Example usage."
    width="750px"
    src="./docs/imgs/example-model-usage.webp" 
    style="border: 1px solid;"> 
    
<img 
    width="750px"
    alt="Example usage of Model CLI."
    src="./docs/imgs/example-model-cli.webp" 
    style="border: 1px solid;">

</div>

## Installation
```console
python -m pip install model-py
``` 
> Note: You import the package as `model`

## Documentation

Read the documentation at https://model.elis.cc

## Quickstart

### 1. Define a model

A model represents a database table. You just need to define the database instance, table name and columns.

<small>Create example file: ./models/user.py</small>
```python
from model import Model
from model.database import SQLiteDatabase

db = SQLiteDatabase("./example.db") # this could be MySQLDatabase

class User(Model):
    table = "user"
    db = db

    id: int = Model.Column(
        type="INT",
        index="PRIMARY",
        auto_increment=True,
    )
    email: str = Model.Column(
        type="VARCHAR",
        length=255,
        index="UNIQUE",
        can_be_null=False,
    )
    age: int | None = Model.Column(type="INT")
```

### 2. Configure model discovery

Create `model.config.yaml` in the project root:

```yaml
include_dirs:
  - ./models
```


### 3. Create the table

The *model sync* CLI is the easiest way to 'sync' models with the database. It automatically generates SQL diffs based on your model definitions. To keep it safe, there are some restrictions in place for column deletion and renaming.

Run CLI commands from your project root so Model can find the configuration.

Preview the generated schema change:

```console
model sync check
```

If the SQL looks correct, apply it:

```console
model sync apply
```

Run `model sync check` once more. It should report nothing left to apply.

That's it!
<hr>

### Now we can use the model

Model instances always represent persisted database records. Loading, inserting, updating, and querying are explicit operations, so it's easy to understand exactly what your code is doing - no complex object lifecycle, no ambiguous `save()`.

#### Insert

`insert()` creates the row and returns a loaded model instance.

```python
from models.user import User

user = User.insert({
    "email": "john.doe@example.com",
    "age": 30
})

print(user.id, user.email)
# prints: 1, john.doe@example.com
```

#### Load by the primary key

Constructing a model loads an existing row.

The primary key is automatically inferred for the model class initialization:

![Automatic initialization column inferring](./docs/imgs/example-model-loading.png)

```python
from models.user import User

user = User(id=1)

print(user.id, user.email)
# prints: 1, john.doe@example.com
```

It raises `ModelRecordNotFoundError` when no row matches.

#### Query

Find records with SQL conditions. SQLite uses `?`
for parameter placeholders (while MySQL uses `%s`):

```python
from models.user import User

user = User.find_one("email = ?", ["john.doe@example.com"])
assert user is not None

print(user.id, user.email) # prints: 1, john.doe@example.com

all_users = User.find_all("age > 24 ORDER BY age")
count = User.count("email LIKE ?", ["%@example.com"])

print(all_users) # prints: [User(...)] 
print(count) # prints: 1
```
`find_one()` returns `None` when there is no match, while `find_all()` returns
an empty list.

#### Update

Records are updated explicitly; assign new values through `update()`.

```python
from models.user import User

user = User(id=1)

print(user.email)
# prints: john.doe@example.com

user.update({
    "email": "johnny@example.com"
})

print(user.email)
# prints: johnny@example.com
```
#### Delete

```python
user.delete()
```

This deletes the row in the database. After deletion, that instance can no longer be used for record operations.