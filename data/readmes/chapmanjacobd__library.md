# library (media toolkit)

A wise philosopher once told me: "the future is [autotainment](https://www.youtube.com/watch?v=F9sZFrsjPp0)".

Manage and curate large media libraries. An index for your archive.
Primary usage is local filesystem but also supports some virtual constructs like
tracking online video playlists (eg. YouTube subscriptions) and scheduling browser tabs.

<img align="right" width="300" height="600" src="https://raw.githubusercontent.com/chapmanjacobd/library/main/.github/examples/art.avif" />

[![Downloads](https://static.pepy.tech/badge/library)](https://pepy.tech/project/library)

## Install

Linux recommended but [Windows setup instructions](./Windows.md) available.

    pip install library

Should also work on Mac OS.

### External dependencies

Required: `ffmpeg`

Some features work better with: `mpv`, `fd-find`, `fish`

## Getting started

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

    library tubeadd my.db $(xclip -selection c)

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
    library (v3.2.007; 102 subcommands)

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
    │ tabs-add        │ 

[...截断...]

Create a tabs database; Add URLs         │
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
    │ nouns            │ Unstructured text -> compound nouns (stdin)    │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ dates            │ Unstructured text -> dates                     │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ times            │ Unstructured text -> times                     │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ timestamps       │ Unstructured text -> timestamps                │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ json-keys-rename │ Rename JSON keys by substring match            │
    ├──────────────────┼────────────────────────────────────────────────┤
    │ combinations     │ Enumerate possible combinations                │
    ╰──────────────────┴────────────────────────────────────────────────╯

    Folder subcommands:
    ╭─────────────────┬─────────────────────────────────────────────────────────────────────╮
    │ merge-mv        │ Move files and merge folders in BSD/rsync style, rename if possible │
    ├─────────────────┼───────────────────────────────────────