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

Should also work on Mac OS.

### External dependencies

Required: `ffmpeg`

Some features work better with: `mpv`, `fd-find`, `fish`

Optional Python extras are grouped under `library[deluxe]`. This includes
`gallery-dl` (used by `gallery-add`), `internetarchive` (used for Internet
Archive downloads), and `cdx_toolkit` (used by the `--webcache`/`--wayback`
CDX extractor):

    pip install "library[deluxe]"

Torrent metadata commands (`torrents-add` and `torrents-dump`) require the
`libtorrent` Python bindings. They are included by `library[deluxe]` when using
Python 3.12 or 3.13; Python 3.14 wheels are not available yet, so use Python
3.13 for torrent support.

If the PyPI wheel is unavailable for your Python or platform, these system
packages provide the bindings:

* Debian/Ubuntu: `sudo apt install python3-libtorrent`
* Fedora: `sudo dnf install rb_libtorrent-python3`
* macOS/Homebrew: `brew install libtorrent-rasterbar`

The Debian, Fedora, and Homebrew packages are built for their system or
Homebrew Python and may not be importable from a separate uv virtualenv. There
is no official Scoop package for the Python bindings; on Windows, use Python
3.13 and `pip install "library[deluxe]"`.

</details>

<details><summary>Local media</summary>

### 1. Extract Metadata

For thirty terabytes of video the initial scan takes about four hours to complete.
After that, subsequent scans of the path (or any subpaths) are much quicker--only
new files will be read by `ffprobe`.

    library fsadd tv.db ./video/folder/

![termtosvg](./examples/extract.svg)

### 2. Watch / Listen from local files

    library watch tv.db                           # the default post-action is to do nothing
    library watch tv.db --post-action delete      # delete file after playing
    library listen finalists.db -k ask_delete     # ask whether to delete file after playing

To stop playing press Ctrl+C in either the terminal or mpv

</details>

<details><summary>Online media</summary>

### 1. Download Metadata

Download playlist and channel metadata. Break free of the YouTube algo~

    library tubeadd educational.db https://www.youtube.com/c/BranchEducation/videos

[![termtosvg](./examples/tubeadd.svg "library tubeadd example")](https://asciinema.org/a/BzplqNj9sCERH3A80GVvwsTTT)

And you can always add more later--even from different websites.

    library tubeadd maker.db https://vimeo.com/terburg

To prevent mistakes the default configuration is to download metadata for only
the most recent 20,000 videos per playlist/channel.

    library tubeadd maker.db --extractor-config playlistend=1000

Be aware that there are some YouTube Channels which have many items--for example
the TEDx channel has about 180,000 videos. Some channels even have upwards of
two million videos. More than you could likely watch in one sitting--maybe even one lifetime.
On a high-speed connection (>500 Mbps), it can take up to five hours to download
the metadata for 180,000 videos.

TIP! If you often copy and paste many URLs you can paste line-delimited text as arguments via a subshell. For example, in `fish` shell with [cb](https://github.com/niedzielski/cb):

    library tubeadd my.db (cb)

Or in BASH:

    library tubeadd my.db $(

[...截断...]

xclip -selection c)

#### 1a. Get new videos for saved playlists

Tubeupdate will go through the list of added playlists and fetch metadata for
any videos not previously seen.

    library tube-update tube.db

### 2. Watch / Listen from websites

    library watch maker.db

To stop playing press Ctrl+C in either the terminal or mpv

</details>

<details><summary>List all subcommands</summary>

    $ library
    library (v3.2.011; 102 subcommands)

    Create database subcommands:
    ╭─────────────────┬──────────────────────────────────────────╮
    │ fs-add          │ Add local media                          │
    ├─────────────────┼──────────────────────────────────────────┤
    │ tube-add        │ Add online video media (yt-dlp)          │
    ├─────────────────┼──────────────────────────────────────────┤
    │ web-add         │ Add open-directory media                 │
    ├─────────────────┼──────────────────────────────────────────┤
    │ gallery-add     │ Add online gallery media (gallery-dl)    │
    ├─────────────────┼──────────────────────────────────────────┤
    │ tabs-add        │ Create a tabs database; Add URLs         │
    ├─────────────────┼──────────────────────────────────────────┤
    │ links-add       │ Create a link-scraping database          │
    ├─────────────────┼──────────────────────────────────────────┤
    │ site-add        │ Auto-scrape website data to SQLite       │
    ├─────────────────┼──────────────────────────────────────────┤
    │ tables-add      │ Add table-like data to SQLite            │
    ├─────────────────┼──────────────────────────────────────────┤
    │ reddit-add      │ Create a reddit database; Add subreddits │
    ├─────────────────┼──────────────────────────────────────────┤
    │ hn-add          │ Create / Update a Hacker News database   │
    ├─────────────────┼──────────────────────────────────────────┤
    │ getty-add       │ Create / Update a Getty Museum database  │
    ├─────────────────┼──────────────────────────────────────────┤
    │ substack        │ Backup substack articles                 │
    ├─────────────────┼──────────────────────────────────────────┤
    │ tildes          │ Backup tildes comments and topics        │
    ├─────────────────┼──────────────────────────────────────────┤
    │ nicotine-import │ Import paths from nicotine+              │
    ├─────────────────┼──────────────────────────────────────────┤
    │ places-import   │ Import places of interest (POIs)         │
    ├─────────────────┼──────────────────────────────────────────┤
    │ row-add         │ Add arbitrary data to SQLite             │
    ├─────────────────┼──────────────────────────────────────────┤
    │ computers-add   │ Add computer info to SQLite              │
    ├─────────────────┼──────────────────────────────────────────┤
    │ torrents-add    │ Add torrent info to SQLite               │
    ╰─────────────────┴──────────────────────────────────────────╯

    Text subcommands:
    ╭──────────────────┬────────────────────────────────────────────────╮
    │ cluster-sort     │ Sort text and images by similarity             │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ regex-sort       │ Sort text by regex split and corpus comparison │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ extract-links    │ Extract inner links from lists of web links    │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ extract-text     │ Extract human text from lists of web links     │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ markdown-links   │ Extract titles from lists of web links         │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ expand-links     │ Expand search urls with query text             │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ nouns            │ Unstructured text -> compo