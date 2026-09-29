# tikviewer-util

Small helpers for working with TikTok usernames and story URLs.

This is a companion crate for [TikViewer](https://tikviewer.org/) — an
anonymous TikTok story viewer that lets you type a username and watch
someone's stories without showing up in their viewer list.

## Usage

```rust
use tikviewer_util::{is_valid_handle, normalize_handle};

assert_eq!(normalize_handle("@example_user"), "example_user");
assert!(is_valid_handle("@example.user_1"));
```

## License

MIT
