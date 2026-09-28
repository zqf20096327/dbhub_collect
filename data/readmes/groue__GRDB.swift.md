<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/groue/GRDB.swift/master/GRDB~dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/groue/GRDB.swift/master/GRDB.png">
    <img alt="GRDB: A toolkit for SQLite databases, with a focus on application development." src="https://raw.githubusercontent.com/groue/GRDB.swift/master/GRDB.png">
</picture>

<p align="center">
    <strong>A toolkit for SQLite databases, with a focus on application development</strong><br>
    Proudly serving the community since 2015
</p>

<p align="center">
    <a href="https://developer.apple.com/swift/"><img alt="Swift 6.1" src="https://img.shields.io/badge/swift-6.1-orange.svg?style=flat"></a>
    <a href="https://github.com/groue/GRDB.swift/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/groue/GRDB.swift.svg?maxAge=2592000"></a>
    <a href="https://github.com/groue/GRDB.swift/actions/workflows/CI.yml"><img alt="CI Status" src="https://github.com/groue/GRDB.swift/actions/workflows/CI.yml/badge.svg?branch=master"></a>
</p>

**Latest release**: June 18, 2026 • [version 7.11.1](https://github.com/groue/GRDB.swift/tree/v7.11.1) • [CHANGELOG](CHANGELOG.md) • [Migrating From GRDB 6 to GRDB 7](Documentation/GRDB7MigrationGuide.md)

**Requirements**: iOS 13.0+ / macOS 10.15+ / tvOS 13.0+ / watchOS 7.0+ &bull; SQLite 3.20.0+ &bull; Swift 6.1+ / Xcode 16.3+

**Contact**:

- Release announcements and usage tips: follow [@groue@hachyderm.io](https://hachyderm.io/@groue) on Mastodon.
- Report bugs in a [Github issue](https://github.com/groue/GRDB.swift/issues/new). Make sure you check the [existing issues](https://github.com/groue/GRDB.swift/issues?q=is%3Aopen) first.
- A question? Looking for advice? Do you wonder how to contribute? Fancy a chat? Go to the [GitHub discussions](https://github.com/groue/GRDB.swift/discussions), or the [GRDB forums](https://forums.swift.org/c/related-projects/grdb).


## What is GRDB?

Use this library to save your application’s permanent data into SQLite databases. It comes with built-in tools that address common needs:

- **SQL Generation**
    
    Enhance your application models with persistence and fetching methods, so that you don't have to deal with SQL and raw database rows when you don't want to.

- **Database Observation**
    
    Get notifications when database values are modified. 

- **Robust Concurrency**
    
    Multi-threaded applications can efficiently use their databases, including WAL databases that support concurrent reads and writes. 

- **Migrations**
    
    Evolve the schema of your database as you ship new versions of your application.
    
- **Leverage your SQLite skills**

    Not all developers need advanced SQLite features. But when you do, GRDB is as sharp as you want it to be. Come with your SQL and SQLite skills, or learn new ones as you go!

---

<p align="center">
    <a href="#usage">Usage</a> &bull;
    <a href="#documentation">Documentation</a> &bull;
    <a href="#installation">Installation</a> &bull;
    <a href="#faq">FAQ</a>
</p>

---

## Usage

<details open>
  <summary>Start using the database in four steps</summary>

```swift
import GRDB

// 1. Open a database connection
let dbQueue = try DatabaseQueue(path: "/path/to/database.sqlite")

// 2. Define the database schema
try dbQueue.write { db in
    try db.create(table: "player") { t in
        t.primaryKey("id", .text)
        t.column("name", .text).notNull()
        t.column("score", .integer).notNull()
    }
}

// 3. Define a record type
struct Player: Codable, Identifiable, FetchableRecord, PersistableRecord {
    var id: String
    var name: String
    var score: Int
    
    enum Columns {
        static let name = Column(CodingKeys.name)
        static let score = Column(CodingKeys.score)
    }
}

// 4. Write and read in the database
try dbQueue.write { db in
    try Player(id: "1", name: "Arthur"

[...截断...]

, score: 100).insert(db)
    try Player(id: "2", name: "Barbara", score: 1000).insert(db)
}

try dbQueue.read { db in
    let player = try Player.find(db, id: "1")
    
    let bestPlayers = try Player
        .order(\.score.desc)
        .limit(10)
        .fetchAll(db)
}
```

</details>

<details>
    <summary>Access to raw SQL</summary>

```swift
try dbQueue.write { db in
    try db.execute(sql: """
        CREATE TABLE player (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          score INT NOT NULL)
        """)
    
    try db.execute(sql: """
        INSERT INTO player (id, name, score)
        VALUES (?, ?, ?)
        """, arguments: ["1", "Arthur", 100])
    
    // Avoid SQL injection with SQL interpolation
    let id = "2"
    let name = "O'Brien"
    let score = 1000
    try db.execute(literal: """
        INSERT INTO player (id, name, score)
        VALUES (\(id), \(name), \(score))
        """)
}
```

See [Executing Updates](#executing-updates)

</details>

<details>
    <summary>Access to raw database rows and values</summary>

```swift
try dbQueue.read { db in
    // Fetch database rows
    let rows = try Row.fetchCursor(db, sql: "SELECT * FROM player")
    while let row = try rows.next() {
        let id: String = row["id"]
        let name: String = row["name"]
        let score: Int = row["score"]
    }
    
    // Fetch values
    let playerCount = try Int.fetchOne(db, sql: "SELECT COUNT(*) FROM player")! // Int
    let playerNames = try String.fetchAll(db, sql: "SELECT name FROM player") // [String]
}

let playerCount = try dbQueue.read { db in
    try Int.fetchOne(db, sql: "SELECT COUNT(*) FROM player")!
}
```

See [Fetch Queries](#fetch-queries)

</details>

<details>
    <summary>Database model types aka "records"</summary>

```swift
struct Player: Codable, Identifiable, FetchableRecord, PersistableRecord {
    var id: String
    var name: String
    var score: Int
    
    enum Columns {
        static let name = Column(CodingKeys.name)
        static let score = Column(CodingKeys.score)
    }
}

try dbQueue.write { db in
    // Create database table
    try db.create(table: "player") { t in
        t.primaryKey("id", .text)
        t.column("name", .text).notNull()
        t.column("score", .integer).notNull()
    }
    
    // Insert a record
    var player = Player(id: "1", name: "Arthur", score: 100)
    try player.insert(db)
    
    // Update a record
    player.score += 10
    try player.update(db)
    
    try player.updateChanges { $0.score += 10 }
    
    // Delete a record
    try player.delete(db)
}
```

See [Records](#records)

</details>

<details>
    <summary>Query the database with the Swift query interface</summary>

```swift
try dbQueue.read { db in
    // Player
    let player = try Player.find(db, id: "1")
    
    // Player?
    let arthur = try Player.filter { $0.name == "Arthur" }.fetchOne(db)
    
    // [Player]
    let bestPlayers = try Player.order(\.score.desc).limit(10).fetchAll(db)
    
    // Int
    let playerCount = try Player.fetchCount(db)
    
    // SQL is always welcome
    let players = try Player.fetchAll(db, sql: "SELECT * FROM player")
}
```

See the [Query Interface](#the-query-interface)

</details>

<details>
    <summary>Database changes notifications</summary>

```swift
// Define the observed value
let observation = ValueObservation.tracking { db in
    try Player.fetchAll(db)
}

// Start observation
let cancellable = observation.start(
    in: dbQueue,
    onError: { error in ... },
    onChange: { (players: [Player]) in print("Fresh players: \(players)") })
```

Ready-made support for Combine and RxSwift:

```swift
// Swift concurrency
for try await players in observation.values(in: dbQueue) {
    print("Fresh players: \(players)")
}

// Combine
let cancellable = observation.publisher(in: dbQueue).sink(
    receiveCompletion: { completion in ... },
    receiveValue: { (players: [Player]) in print("Fresh players: \(players)") })

// RxS