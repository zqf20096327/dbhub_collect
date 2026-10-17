# library (media toolkit)

A wise philosopher once told me: "the future is [autotainment](https://www.youtube.com/watch?v=F9sZFrsjPp0)".

Manage and curate large media libraries. An index for your archive.
Primary usage is local filesystem but also supports some virtual constructs like
tracking online video playlists (eg. YouTube subscriptions) and scheduling browser tabs.

<img align="right" width="300" height="600" src="https://raw.githubusercontent.com/chapmanjacobd/library/main/.github/examples/art.avif" />

[![Downloads](https://static.pepy.tech/badge/library)](https://pepy.tech/project/library)

## Getting started

<details><summary>Install</summary>

Linux recommended but [Windows setup instructions](./Windows.md) available.

    pip install library

Mac OS is also supported.

### External dependencies

Required: `ffmpeg`

Some features work better with: `mpv`, `fd-find`, `fish`

Optional Python extras are grouped under `library[deluxe]`. This includes
`gallery-dl` (used by `database add gallery`), `internetarchive` (used for
Internet Archive downloads), and `cdx_toolkit` (used by the
`--webcache`/`--wayback` CDX extractor):

    pip install "library[deluxe]"

Torrent metadata commands (`database add torrents` and `torrent dump`) require
the `libtorrent` Python bindings. They are included by `library[deluxe]` on
Python 3.12 and 3.13. On Python 3.14, libtorrent-rasterbar bindings are
usually provided by distro packages rather than PyPI:

* Debian/Ubuntu: `sudo apt install python3-libtorrent`
* Fedora: `sudo dnf install rb_libtorrent-python3`
* macOS/Homebrew: `brew install libtorrent-rasterbar`

The Debian, Fedora, and Homebrew packages are built for their system or
Homebrew Python and are not importable from a separate uv virtualenv. There
is no official Scoop package for the Python bindings; on Windows, use Python
3.13 and `pip install "library[deluxe]"`.

</details>

<details><summary>Local media</summary>

### 1. Extract Metadata

For thirty terabytes of video the initial scan takes about four hours to complete.
After that, subsequent scans of the path (or any subpaths) are much quicker--only
new files are read by `ffprobe`.

    library database add filesystem tv.db ./video/folder/

![termtosvg](./examples/extract.svg)

### 2. Watch / Listen from local files

    library play video tv.db                           # the default post-action is to do nothing
    library play video tv.db --post-action delete      # delete file after playing
    library play audio finalists.db -k ask_delete      # ask whether to delete file after playing

To stop playing press Ctrl+C in either the terminal or mpv

</details>

<details><summary>Online media</summary>

### 1. Download Metadata

Download playlist and channel metadata. Break free of the YouTube algo~

    library database add video educational.db https://www.youtube.com/c/BranchEducation/videos

[![termtosvg](./examples/tubeadd.svg "library database add video example")](https://asciinema.org/a/BzplqNj9sCERH3A80GVvwsTTT)

And you can add more at any time--even from different websites.

    library database add video maker.db https://vimeo.com/terburg

To prevent mistakes the default configuration is to download metadata for only
the most recent 20,000 videos per playlist/channel.

    library database add video maker.db --extractor-config playlistend=1000

Be aware that there are some YouTube Channels which have many items--for example
the TEDx channel has about 180,000 videos. Some channels even have upwards of
two million videos. More than you could likely watch in one sitting--maybe even one lifetime.
On a high-speed connection (>500 Mbps), it can take up to five hours to download
the metadata for 180,000 videos.

TIP! If you often copy and paste many URLs you can paste line-delimited text as arguments via a subshell. For example, in `fish` shell with [cb](https://github.com/niedzielski/cb):

    library database add video my.db (cb)

Or in BASH:

    library database add 

[...截断...]

video my.db $(xclip -selection c)

#### 1a. Get new videos for saved playlists

Tubeupdate goes through the list of stored playlists and fetches metadata for
any videos not seen before.

    library database update video tube.db

### 2. Watch / Listen from websites

    library play video maker.db

To stop playing press Ctrl+C in either the terminal or mpv

</details>

<details><summary>List all subcommands</summary>

Commands are organized by resource. Use `database` (or `db`) for database
operations, `filesystem` (or `fs`) for filesystem operations, `document` (or
`doc`/`docs`) for document operations, and `file` (or `files`) for file
operations. The `ls` alias can be used for nested list commands. Resource group
names and their aliases take precedence over flat command names, so a few former
flat commands are now only reachable through a group (for example
`database filesystem list`, `captions`, `table markdown`, `tabs open`,
`links extract`, `text extract`, and `torrent info`).

    $ library
    library (v4.0.0; 118 subcommands)

    Create database subcommands:
    ╭──────────────────────────┬──────────────────────────────────────────╮
    │ database add filesystem  │ Add local media                          │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add video       │ Add online video media (yt-dlp)          │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add web         │ Add open-directory media                 │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add gallery     │ Add online gallery media (gallery-dl)    │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add tabs        │ Create a tabs database; Add URLs         │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add links       │ Create a link-scraping database          │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add site        │ Auto-scrape website data to SQLite       │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add tables      │ Add table-like data to SQLite            │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add reddit      │ Create a reddit database; Add subreddits │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add hackernews  │ Create / Update a Hacker News database   │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add getty       │ Create / Update a Getty Museum database  │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add substack    │ Backup substack articles                 │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add tildes      │ Backup tildes comments and topics        │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database import nicotine │ Import paths from nicotine+              │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database import places   │ Import places of interest (POIs)         │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add row         │ Add arbitrary data to SQLite             │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add computers   │ Add computer info to SQLite              │
    ├──────────────────────────┼──────────────────────────────────────────┤
    │ database add torrents    │ Add torrent info to SQLite               │
    ╰──────────────────────────┴──────────────────────────────────────────╯

    Text subcommands:
    ╭───────────────────────┬────────────────────────────────────────────────╮
  