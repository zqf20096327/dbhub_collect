# gosigar process timing compatibility

This module implements only the `ProcTime` API used by TiKV's PD resource
controller. It uses `gopsutil/v4`, preserving millisecond
units and error reporting. It is not a general replacement for gosigar.

Upstream `cloudfoundry/gosigar` requires CGO on macOS. This replacement keeps
TiKV clients buildable with `CGO_ENABLED=0`, including on macOS.
The original module path is retained for use as a Go module replacement:

```go
replace github.com/cloudfoundry/gosigar => github.com/awaken/gosigar v0.1.0
```

Validate from this repository's root:

```sh
CGO_ENABLED=0 go test ./...
CGO_ENABLED=1 go test -race ./...
```
