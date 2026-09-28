# abstract-level

**Abstract class for a lexicographically sorted key-value database.** Provides encodings, sublevels, events and hooks. If you are upgrading, please see [`UPGRADING.md`](UPGRADING.md).

> :pushpin: Wondering what happened to `levelup`? Visit [Frequently Asked Questions](https://github.com/Level/community#faq).

[![level badge][level-badge]](https://github.com/Level/awesome)
[![npm](https://img.shields.io/npm/v/abstract-level.svg)](https://www.npmjs.com/package/abstract-level)
[![Node version](https://img.shields.io/node/v/abstract-level.svg)](https://www.npmjs.com/package/abstract-level)
[![Test](https://img.shields.io/github/actions/workflow/status/Level/abstract-level/test.yml?branch=main\&label=test)](https://github.com/Level/abstract-level/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/codecov/c/github/Level/abstract-level?label=\&logo=codecov\&logoColor=fff)](https://codecov.io/gh/Level/abstract-level)
[![Standard](https://img.shields.io/badge/standard-informational?logo=javascript\&logoColor=fff)](https://standardjs.com)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)
[![Donate](https://img.shields.io/badge/donate-orange?logo=open-collective\&logoColor=fff)](https://opencollective.com/level)

## Usage

This module exports an abstract class. End users should instead use modules like [`level`](https://github.com/Level/level) that export a concrete implementation. The purpose of the abstract class is to provide a common interface that looks like this:

```js
// Create a database
const db = new Level('./db', { valueEncoding: 'json' })

// Add an entry with key 'a' and value 1
await db.put('a', 1)

// Add multiple entries
await db.batch([{ type: 'put', key: 'b', value: 2 }])

// Get value of key 'a': 1
const value = await db.get('a')

// Iterate entries with keys that are greater than 'a'
for await (const [key, value] of db.iterator({ gt: 'a' })) {
  console.log(value) // 2
}
```

Usage from TypeScript requires generic type parameters.

<details><summary>TypeScript example</summary>

```ts
// Specify types of keys and values (any, in the case of json).
// The generic type parameters default to Level<string, string>.
const db = new Level<string, any>('./db', { valueEncoding: 'json' })

// All relevant methods then use those types
await db.put('a', { x: 123 })

// Specify different types when overriding encoding per operation
await db.get<string, string>('a', { valueEncoding: 'utf8' })

// Though in some cases TypeScript can infer them
await db.get('a', { valueEncoding: db.valueEncoding('utf8') })

// It works the same for sublevels
const abc = db.sublevel('abc')
const xyz = db.sublevel<string, any>('xyz', { valueEncoding: 'json' })
```

</details>

TypeScript users can benefit from the `using` keyword because `abstract-level` implements [`Symbol.asyncDispose`](https://github.com/tc39/proposal-explicit-resource-management) on its resources. For example:

<details><summary>Using example</summary>

```ts
await db.put('example', 'before')
await using snapshot = db.snapshot()
await db.put('example', 'after')
await db.get('example', { snapshot })) // Returns 'before'
```

The equivalent in JavaScript would be:

```js
await db.put('example', 'before')
const snapshot = db.snapshot()

try {
  await db.put('example', 'after')
  await db.get('example', { snapshot })) // Returns 'before'
} finally {
  await snapshot.close()
}
```

</details>

## Install

With [npm](https://npmjs.org) do:

```shell
npm install abstract-level
```

## Supported Platforms

We aim to support Active LTS and Current Node.js releases, as well as evergreen browsers that are based on Chromium, Firefox or Webkit. Features that the runtime must support include [`queueMicrotask`](https://developer.mozilla.org/en-US/docs/Web/API/queueMicrotask#browser_compatibility), [`Promise.allSettled()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled#br

[...截断...]

owser_compatibility), [`globalThis`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis#browser_compatibility) and [async generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function*#browser_compatibility). Supported runtimes may differ per implementation.

## Public API For Consumers

This module has a public API for consumers of a database and a [private API](#private-api-for-implementors) for concrete implementations. The public API, as documented in this section, offers a simple yet rich interface that is common between all implementations. Implementations may have additional options or methods. TypeScript [type declarations](https://www.typescriptlang.org/docs/handbook/2/type-declarations.html) are [included](./index.d.ts) (and exported for reuse) only for the public API.

An `abstract-level` database is at its core a [key-value database](https://en.wikipedia.org/wiki/Key%E2%80%93value_database). A key-value pair is referred to as an _entry_ here and typically returned as an array, comparable to [`Object.entries()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries).

### `db = new Level(...[, options])`

Creating a database is done by calling a class constructor. Implementations export a class that extends the [`AbstractLevel`](./abstract-level.js) class and has its own constructor with an implementation-specific signature. All constructors should have an `options` argument as the last. Typically, constructors take a `location` as their first argument, pointing to where the data will be stored. That may be a file path, URL, something else or none at all, since not all implementations are disk-based or persistent. Others take another database rather than a location as their first argument.

The optional `options` object may contain:

- `keyEncoding` (string or object, default `'utf8'`): encoding to use for keys
- `valueEncoding` (string or object, default `'utf8'`): encoding to use for values.

See [Encodings](#encodings) for a full description of these options. Other `options` (except `passive`) are forwarded to `db.open()` which is automatically called in a next tick after the constructor returns. Any read & write operations are queued internally until the database has finished opening. If opening fails, those queued operations will yield errors.

### `db.status`

Getter that returns a string reflecting the current state of the database:

- `'opening'` - waiting for the database to be opened
- `'open'` - successfully opened the database
- `'closing'` - waiting for the database to be closed
- `'closed'` - database is closed.

### `db.open([options])`

Open the database. Returns a promise. Options passed to `open()` take precedence over options passed to the database constructor. Not all implementations support the `createIfMissing` and `errorIfExists` options (notably [`memory-level`](https://github.com/Level/memory-level) and [`browser-level`](https://github.com/Level/browser-level)) and will indicate so via `db.supports.createIfMissing` and `db.supports.errorIfExists`.

The optional `options` object may contain:

- `createIfMissing` (boolean, default: `true`): If `true`, create an empty database if one doesn't already exist. If `false` and the database doesn't exist, opening will fail.
- `errorIfExists` (boolean, default: `false`): If `true` and the database already exists, opening will fail.
- `passive` (boolean, default: `false`): Wait for, but do not initiate, opening of the database.

It's generally not necessary to call `open()` because it's automatically called by the database constructor. It may however be useful to capture an error from failure to open, that would otherwise not surface until another method like `db.get()` is called. It's also possible to reopen the database after it has been closed with [`close()`](#dbclose). Once `open()` has then been called, any read & write oper