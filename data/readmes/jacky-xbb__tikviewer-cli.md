# tikviewer-cli

Tiny Go CLI that normalizes a TikTok handle or profile URL and prints the
matching story URL for [TikViewer](https://tikviewer.org/), a browser-based
anonymous TikTok story viewer — you type a username, watch their stories, and
you never show up in their viewer list. Nothing to install, no login.

## Install

```sh
go install github.com/jacky-xbb/tikviewer-cli/cmd/tikviewer@latest
```

## Usage

```sh
$ tikviewer @Charli
https://tikviewer.org/@charli

$ tikviewer "https://www.tiktok.com/@charli/video/123456?lang=en"
https://tikviewer.org/@charli
```

Accepts a bare handle, an `@handle`, or any `tiktok.com/@handle/...` URL, with
or without query strings. Handles are lowercased and validated against TikTok's
`[A-Za-z0-9._]{2,24}` rule.

## Library

```go
import "github.com/jacky-xbb/tikviewer-cli/handle"

h, err := handle.Normalize("https://www.tiktok.com/@Charli")
url := handle.StoryURL(h) // https://tikviewer.org/@charli
```

## Why

I kept pasting messy TikTok links into <https://tikviewer.org/> by hand. This
just cleans them up first.

## License

MIT
