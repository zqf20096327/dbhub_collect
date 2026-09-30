# grpcio-sys

This project is forked from [grpc-sys] and includes fixes to build with the newer g++ 15 compiler.

Add this section to your `Cargo.toml`:

```toml
[patch.crates-io]
grpcio-sys = { git = "https://github.com/fanyang89/grpcio-sys.git", branch = "main" }
```

[grpc-sys]: https://github.com/tikv/grpc-rs/tree/master/grpc-sys
