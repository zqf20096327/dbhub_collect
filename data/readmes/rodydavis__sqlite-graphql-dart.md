# gql_sqlite

A Dart package to parse GraphQL queries and mutations and run them against a SQLite database. This library allows you to use GraphQL-like syntax to interact with your SQLite database, including support for dynamic filtering.

## Features

- Execute GraphQL queries and mutations.
- Translate GraphQL to SQL.
- Support for dynamic filtering with a `where` argument.
- Uses `sqlparser` for SQL validation.

## Usage

First, add `gql_sqlite` to your `pubspec.yaml`:

```yaml
dependencies:
  gql_sqlite: ^0.0.1 # Replace with the latest version
  sqlite3: ^2.4.0 # Or your preferred sqlite3 implementation
```

Then, you can use the `Executor` to run queries against your database.

```dart
import 'package:gql_sqlite/gql_sqlite.dart';
import 'package:sqlite3/sqlite3.dart';

void main() {
  // Create a new in-memory SQLite database.
  final db = sqlite3.openInMemory();

  // Create a table.
  db.execute('''
    CREATE TABLE users (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      age INTEGER
    );
  ''');

  // Insert some data.
  db.execute('INSERT INTO users (name, age) VALUES ("Alice", 25)');
  db.execute('INSERT INTO users (name, age) VALUES ("Bob", 30)');
  db.execute('INSERT INTO users (name, age) VALUES ("Charlie", 35)');

  // Create an executor.
  final executor = GqlExecutor(GqlDatabase(db));

  // Query the data.
  final result = executor.execute('''
    query {
      users {
        id
        name
      }
    }
  ''');

  print(result);
  // {data: {users: [{id: 1, name: Alice}, {id: 2, name: Bob}, {id: 3, name: Charlie}]}}
}
```

## Queries with `where`

You can use the `where` argument to filter queries dynamically. The following operators are supported:

| Operator | Description      |
|----------|------------------|
| `_eq`    | Equal to         |
| `_gt`    | Greater than     |
| `_gte`   | Greater or equal |
| `_lt`    | Less than        |
| `_lte`   | Less or equal    |
| `_neq`   | Not equal to     |
| `_like`  | LIKE operator    |
| `_in`    | IN operator      |
| `_nin`   | NOT IN operator  |

### Example: `_eq`

```dart
final result = executor.execute('''
  query {
    users(where: { name: { _eq: "Alice" } }) {
      id
      name
    }
  }
''');

print(result); // {data: {users: [{id: 1, name: Alice}]}}
```

### Example: `_gt` and `_like`

```dart
final result = executor.execute('''
  query {
    users(where: { age: { _gt: 28 }, name: { _like: "%b%" } }) {
      id
      name
      age
    }
  }
''');

print(result); // {data: {users: [{id: 2, name: Bob, age: 30}]}}
```

### Example: `_in`

```dart
final result = executor.execute('''
  query {
    users(where: { id: { _in: [1, 3] } }) {
      id
      name
    }
  }
''');

print(result); // {data: {users: [{id: 1, name: Alice}, {id: 3, name: Charlie}]}}
```

## Mutations

You can use mutations to create, update, and delete data. The mutation name should start with `create`, `update`, or `delete`.

Mutations return the number of `affected_rows` and the `last_insert_id` for `create` mutations.

### Create

```dart
final result = executor.executeMutation('''
  mutation {
    createUsers(name: "David", age: 40)
  }
''');

print(result);
// {
//   data: {
//     createUsers: {
//       last_insert_id: 4,
//       affected_rows: 1
//     }
//   }
// }
```

### Update

The `update` mutation requires a `where` argument to identify the rows to update and a `_set` argument with the new values.

```dart
final result = executor.executeMutation('''
  mutation {
    updateUsers(where: { age: { _gt: 30 } }, _set: { age: 31 })
  }
''');

print(result);
// {
//   data: {
//     updateUsers: {
//       affected_rows: 1
//     }
//   }
// }
```

You can also still update by `id` directly.

```dart
final result = executor.executeMutation('''
  mutation {
    updateUsers(id: 1, name: "Alicia")
  }
''');

print(result);
// {
//   data: {
//     updateUsers: {
//       affected_rows: 1
//     }
//   }
// }
```

### Delete

The `delete` mutation can use a `where` argument to identify the rows to delete.

```dart
final result = executor.executeMutation('''
  mutation {
    deleteUsers(where: { age: { _lt: 30 } })
  }
''');

print(result);
// {
//   data: {
//     deleteUsers: {
//       affected_rows: 1
//     }
//   }
// }
```

You can also still delete by `id` directly.

```dart
final result = executor.executeMutation('''
  mutation {
    deleteUsers(id: 2)
  }
''');

print(result);
// {
//   data: {
//     deleteUsers: {
//       affected_rows: 1
//     }
//   }
// }
```

## Subscriptions

You can use subscriptions to listen for changes in your data. The subscription will emit the current data when you first subscribe, and then it will emit the updated data whenever a change occurs.

```dart
final stream = executor.executeSubscription('''
  subscription {
    users {
      id
      name
    }
  }
''');

stream.listen((result) {
  print(result);
});

// Insert some data to trigger the subscription
db.execute('INSERT INTO users (name, age) VALUES ("David", 40)');
```
