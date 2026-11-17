# obmysqltcl

`obmysqltcl 0.1` is a Tcl 9 binding for OceanBase MySQL tenants. It links
dynamically to an independently installed OceanBase Connector/C (`libobclnt`).

Its commands follow mysqltcl's arguments and results, using `::obmysql::*`
and legacy names such as `obmysqlconnect`, `obmysqluse` and `obmysqlexec`.
The status array is `::obmysqlstatus`; connection and statement handles use
the `obmysql` prefix, query handles use `obquery`, and the Tcl object types
are `obmysqlhandle` and `obmysqlnull`. Handles belong to the binding and
interpreter that created them.

## Build on Linux

Provide a C compiler, a configured or installed Tcl 9 development tree with
its stub library, and the OceanBase Connector/C SDK. The SDK must contain
`include/mysql.h` and `lib/libobclnt.so` (or `lib64/libobclnt.so`).
The initial target is Linux with Tcl 9 and OceanBase Connector/C 2.2.14.
Other client versions require validation. Windows is pending availability of
a suitable Connector/C SDK and validation of the binding on that platform.

Run this from the root of the checked-out or extracted source tree.

```sh
./build.sh --tcl-config /path/to/tcl/lib/tclConfig.sh \
  --sdk /path/to/obclient \
  --output /path/to/packages/obmysqltcl0.1
```

`TCL_CONFIG` and `OBCLIENT_ROOT` can supply the SDK paths. `CC`, `CFLAGS` and
`LDFLAGS` can supply build options. The compiler is invoked without an
embedded client-library RPATH. The output contains the binding, package
index, build information and notices; no database client library is copied.

## Load and use the binding

Point Tcl 9 to the parent directory of the built package and make the client
runtime available to the Linux dynamic linker. Use `lib64` if that is where
your Connector/C runtime is installed.

```sh
export TCLLIBPATH=/path/to/packages
export LD_LIBRARY_PATH=/path/to/obclient/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
```

Run the following in a Tcl 9 shell with `OB_HOST`, `OB_PORT`, `OB_USER` and
`OB_PASSWORD` set for your OceanBase MySQL tenant. A successful `SELECT 1`
prints `1`.

```tcl
package require obmysqltcl 0.1
set connection [::obmysql::connect -host $::env(OB_HOST) -port $::env(OB_PORT) \
    -user $::env(OB_USER) -password $::env(OB_PASSWORD)]
try {
    puts [::obmysql::sel $connection {SELECT 1} -flatlist]
} finally {
    ::obmysql::close $connection
}
```

`-ssl true` requires TLS, validates the server certificate and checks the
requested host name. Supply `-sslca` or `-sslcapath` for a private CA; without
one, the client uses its default trust paths. An unavailable TLS endpoint or
an untrusted certificate is an error, not a fallback to an unencrypted login.

The mysqltcl API's optional C prepared-statement commands remain disabled,
as in the original HammerDB binding; SQL `PREPARE`/`EXECUTE` remains available.

See [NOTICE](NOTICE) for the original source and changes, and [COPYING](COPYING)
for the binding and Tcl stub notices.
