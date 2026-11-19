# encrypted-durable-object

Field-level encryption with searchable blind indexes for Cloudflare Durable Object SQLite storage.

Extend `EncryptedDurableObject` instead of `DurableObject`, declare the encrypted columns, and supply a root key. Rows are encrypted before they reach SQLite. You can still find them by exact match.

```js
import { EncryptedDurableObject, wrappedRootKey, secretKek } from "@cloudraker/encrypted-durable-object";

export class Tenant extends EncryptedDurableObject {
  static encrypted = {
    contacts: {
      email: { index: { transforms: ["lowercase"] } },
      ssn: { indexes: [{ name: "ssn_last4", transforms: ["lastFourDigits"], bits: 16 }] },
      notes: true, // encrypted, not searchable
    },
  };

  rootKey() {
    return wrappedRootKey(this.ctx, secretKek(this.ctx, this.env.KEK));
  }

  async addContact(c) {
    return this.db.insert("contacts", c);
  }

  async lookup(email) {
    return this.db.get("contacts", { email }); // decrypted row, or null
  }
}
```

> **Disclaimer.** This is an independent open-source project. It is not affiliated with, endorsed by or sponsored by Cloudflare, Inc. "Cloudflare", "Workers" and "Durable Objects" are trademarks of Cloudflare, Inc.

## Why

- **One database per tenant.** A Durable Object gives each tenant its own SQLite database. This library gives each tenant its own encryption key too.
- **Your own team cannot read the data directly.** Developers and operators who browse storage, run SQL against it, or open exports and backups see only ciphertext. This holds while they cannot read the key (the KEK secret or the KMS) and cannot deploy Worker code. Give those permissions to fewer people than storage access. See [Security model](#security-model).
- **Crypto-shredding.** Destroy or revoke a tenant's key and their data, including backups, cannot be read.
- **No dependencies.** It uses WebCrypto only. It needs no `nodejs_compat` and no WebAssembly.
- **CipherSweet-compatible.** It uses the CipherSweet `FIPSCrypto` format (AES-256-CTR + HMAC-SHA384, HKDF, PBKDF2 blind indexes). The tests check it against vectors from the PHP reference implementation. Other services can read the same data with CipherSweet.

## Install

```sh
npm i @cloudraker/encrypted-durable-object
```

Use a SQLite-backed Durable Object (`new_sqlite_classes` in your migration).

## Schema

You own the table definitions. For each blind index, add a `TEXT` column with the index name. An index on that column is recommended.

```sql
CREATE TABLE IF NOT EXISTS contacts (
  id INTEGER PRIMARY KEY,
  name TEXT,
  email TEXT, email_idx TEXT,
  ssn TEXT, ssn_last4 TEXT,
  notes TEXT
);
CREATE INDEX IF NOT EXISTS contacts_email_idx ON contacts(email_idx);
```

`static encrypted` maps `table -> column -> spec`:

| Spec | Meaning |
|---|---|
| `true` | Encrypted. Not searchable. |
| `{ index: {...} }` | Encrypted, with one blind index named `<column>_idx` by default. |
| `{ indexes: [{ name, ... }, ...] }` | Encrypted, with several blind indexes. |

Index options:

| Option | Default | Meaning |
|---|---|---|
| `name` | `<column>_idx` | Column that stores the index. |
| `transforms` | `[]` | Applied before hashing. Built-in: `"lowercase"` (ASCII, as in PHP), `"lastFourDigits"`. A function `(s) => s` also works, but it is not portable to other CipherSweet clients. |
| `bits` | `32` | Index size, a multiple of 8. Fewer bits leak less and cause more collisions. The library removes collisions for you. See the [CipherSweet planning guide](https://ciphersweet.paragonie.com/security#blind-index-planning). |
| `fast` | `true` | `true`: PBKDF2 with 1 iteration. `false`: PBKDF2 with `iterations` (minimum 50,000), which costs much more CPU. |

Encrypted values must be strings or `null`. `null` is stored as `NULL` and is not encrypted.

## API

### `this.db`

| Method | Returns |
|---|---|
| `insert(table, row)` | New `rowid`. |
| `find(table, where, { limit })` | Decrypted rows. |
| `get(table, where)` | First decrypted row or `null`. |
| `update(table, where, patch)` | Number of rows changed. Encrypted columns in `patch` are encrypted and re-indexed. |
| `delete(table, where)` | Number of rows deleted. |
| `decrypt(table, row)` | Decrypts a row that you read with raw SQL. |
| `blindIndex(table, column, value, indexName?)` | Index value for your own SQL, for example `WHERE email_idx = ?`. |

`where` is an object of equality conditions joined with `AND`. Keys are:

- plain columns, which match directly;
- encrypted columns, which match through their first blind index;
- index names, such as `{ ssn_last4: "6789" }`, which match through that index.

Blind indexes can collide. The library decrypts each candidate row and removes rows that do not match. `update` and `delete` change only the rows that really match.

`this.sql` is the normal `ctx.storage.sql`. Use it for anything else. Encrypted columns come back as ciphertext until you call `this.db.decrypt()`.

### `this.kv`

An encrypted version of the Durable Object KV API. Values are JSON.

```js
await this.kv.put("settings", { theme: "dark" });
await this.kv.get("settings");                 // { theme: "dark" }
await this.kv.list({ prefix: "session:" });     // Map
await this.kv.delete("settings");
```

Keys are not encrypted. Each value is bound to its key, so a value moved to another key fails to decrypt.

## Keys

Implement `rootKey()`. It must return 32 bytes (`Uint8Array`, `ArrayBuffer` or a hex string). The library calls it once each time the object starts, inside `blockConcurrencyWhile`, and keeps the key in memory only.

**Keep the root key stable.** Blind indexes depend on it. If the root key changes, you must re-encrypt and re-index every row.

### Envelope encryption (recommended)

`wrappedRootKey(ctx, { wrap, unwrap })` creates a random root key for each object the first time it starts. It stores the key only in wrapped form, in the object's own storage. On later starts it calls `unwrap`.

With a key-encryption key (KEK) from a Worker secret:

```js
rootKey() {
  return wrappedRootKey(this.ctx, secretKek(this.ctx, this.env.KEK)); // KEK: 64 hex chars
}
```

`secretKek` uses AES-256-GCM and binds the wrapped key to the object id.

With any KMS, such as AWS KMS, Google Cloud KMS, HashiCorp Vault or WorkOS Vault:

```js
rootKey() {
  return wrappedRootKey(this.ctx, {
    wrap: (key) => myKms.encrypt({ keyId: this.env.KMS_KEY_ID, plaintext: key }),
    unwrap: (blob) => myKms.decrypt(blob),
  });
}
```

To support customer-managed keys (BYOK), pick the KMS key per tenant inside `wrap` and `unwrap`. To rotate the KEK, unwrap with the old KEK and wrap with the new one. That does not change the root key, so no data is re-encrypted.

### Your own key

```js
async rootKey() {
  return this.env.ROOT_KEY_HEX; // one key for all objects: less isolation, simpler
}
```

## Security model

It protects against:

- reads of the stored data, exports and backups (for example point-in-time recovery) by anyone without the key, including your own staff with storage access only;
- moving ciphertext between columns or tables (each column has its own derived key);
- tampering with ciphertext (each value is authenticated).

It does **not** protect against:

- your own Worker code, or anyone who can run code in it or read its secrets. The Worker has the plaintext key in memory;
- leaks from blind indexes. Equal values have equal indexes, so an observer can see that two rows share a value. Use small `bits` and avoid indexes on low-variety columns;
- swapping one encrypted value for another in the same column (row-swap). AAD from a row id is not supported yet;
- `LIKE`, ranges, `ORDER BY` or aggregates on encrypted columns. Blind indexes support exact match only.

Revocation takes effect only when the object restarts, because the key stays in memory until then.

## Compatibility with CipherSweet

Values and indexes match `paragonie/ciphersweet` (PHP) with the `FIPSCrypto` backend and `StringProvider`, for the same table name, column name, index name, transforms, bit length and hash speed.

Text is encoded as UTF-8. `ciphersweet-js` 1.x encodes text as Latin-1, so it corrupts characters outside Latin-1. It can read this library's output only for Latin-1 text.

## Tests

```sh
npm test
```

- `test/do.test.mjs` runs a Durable Object in workerd through wrangler.
- `test/vectors.test.mjs` checks decryption and blind indexes against `test/vectors.json`. Those vectors were generated once by `paragonie/ciphersweet` v4.11.0 (PHP). The tests do not need PHP.

## License

MIT. See [LICENSE](LICENSE).
