# TikViewerKit

Small helpers for working with TikTok usernames and story URLs.

This is a companion package for [TikViewer](https://tikviewer.org/) — an
anonymous TikTok story viewer that lets you type a username and watch
someone's stories without showing up in their viewer list.

## Usage

```swift
import TikViewerKit

TikViewerKit.normalizeHandle("@example_user") // "example_user"
TikViewerKit.isValidHandle("@example.user_1") // true
```

## Installation

Add the package to your `Package.swift`:

```swift
.package(url: "https://github.com/jacky-xbb/TikViewerKit.git", from: "0.1.0")
```

## License

MIT
