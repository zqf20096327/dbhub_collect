<p align="center">
  <img src="assets/gopher-elephant.png" alt="The Go gopher in a PostgreSQL elephant costume" width="240">
</p>

# gopgext — PostgreSQL extensions in Go

> [!WARNING]
> gopgext is **experimental**. Don't use it in production: a bug in the
> generated code or the Go runtime runs inside the server, where it can
> crash it or corrupt data, and the API and generated SQL may change
> without notice.

`gopgext` builds PostgreSQL extensions from plain Go code, using TinyGo. A
project is just Go files: functions marked with `//gopgext:function` become
SQL functions, and gopgext supplies everything else: the C glue, the
`CREATE FUNCTION` script and the control file. Go's standard library works
(`fmt`, `strings`, `regexp`, `encoding/json`, `crypto/*`, maps, generics,
`defer`/`recover`, iterators...), and Go code can run queries through SPI.

**Documentation: <https://jespino.github.io/gopgext/>**. New to gopgext? The
[tutorial](https://jespino.github.io/gopgext/docs/tutorial/) walks you through building, installing and
calling a "hello world" extension in a few minutes.

```sh
gopgext init hello       # creates hello/go.mod and hello/main.go
gopgext install hello    # builds hello.so, hello.control, hello--1.0.sql and installs them
psql -c 'CREATE EXTENSION hello' -c "SELECT hello('world')"
#     hello
# ---------------
#  Hello, world!
```

```go
package main

// Hello returns a greeting for name.
//
//gopgext:function immutable parallel=safe
func Hello(name string) string {
	return "Hello, " + name + "!"
}

func main() {} // runs once per backend, when PostgreSQL loads the library
```

It's the same approach as [gokm](https://github.com/jespino/gokm) (Linux kernel modules in Go):
a custom TinyGo target and runtime layer for the host, a C runtime compiled
by the host's own build system (PGXS here, kbuild there), and generated glue.

## Install

Requirements: Linux x86-64, Go, TinyGo (tested with 0.43.0), PostgreSQL 14
or later with its server development files (`pg_config`, headers, PGXS),
`make`, a C compiler and binutils (`objcopy`).

```sh
go install github.com/jespino/gopgext@latest
```

See [Installation](https://jespino.github.io/gopgext/docs/install/) for details.

## Documentation

| Page | What it covers |
|---|---|
| [Tutorial](https://jespino.github.io/gopgext/docs/tutorial/) | a "hello world" extension, step by step |
| [Command line](https://jespino.github.io/gopgext/docs/commands/) | `gopgext init`, `build` and `install`, and what a project can contain |
| [SQL functions](https://jespino.github.io/gopgext/docs/functions/) | type mapping, function options, `NULL`s, sets, rows, errors |
| [Data types](https://jespino.github.io/gopgext/docs/types/) | SQL data types backed by Go types, composite and polymorphic types |
| [The pg package](https://jespino.github.io/gopgext/docs/pg/) | SPI queries, errors with SQLSTATE codes, logging, settings |
| [Frameworks](https://jespino.github.io/gopgext/docs/frameworks/) | triggers, aggregates, GiST/GIN/SP-GiST/BRIN, access methods, FDWs, hooks, ... |
| [API reference](https://jespino.github.io/gopgext/api/) | every exported identifier of the Go packages |
| [Examples and contrib ports](https://jespino.github.io/gopgext/docs/examples/) | complete extensions, including ports of PostgreSQL's contrib modules |
| [How it works](https://jespino.github.io/gopgext/docs/internals/) | the build pipeline and the runtime model |
| [Limitations](https://jespino.github.io/gopgext/docs/limitations/) | what isn't supported |

The website's source is in [`site/`](site/): `make site-serve` previews it
locally.

## Development

```sh
make test                                   # go vet + unit tests
make pgtest PG_CONFIG=/path/to/pg_config    # integration tests against a real PostgreSQL
```

See [Development](https://jespino.github.io/gopgext/docs/development/) for the test conventions.

## License

gopgext is released under the [MIT License](LICENSE).

The ports in [`contrib/`](contrib/) derive from PostgreSQL's contrib modules
and also keep the [PostgreSQL License](contrib/LICENSE-PostgreSQL). A few
files carry the notices of the third-party code they're based on (for
example, pgcrypto's DES, MD5 crypt, CAST5 and RIPEMD-160); those notices
apply to those files.

## Mascot

The gopgext mascot is the Go gopher in an elephant costume, a nod to
PostgreSQL's elephant. It's based on the Go gopher designed by
[Renée French](https://reneefrench.blogspot.com/), licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
