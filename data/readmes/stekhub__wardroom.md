<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/wardroom-header-dark.svg">
    <img src="assets/logo/wardroom-header-light.svg" alt="Wardroom" width="624">
  </picture>
  <h2 align="center">Newsgroups deserve a modern home.</h2>
</div>

Newsgroups are among the oldest places for discussion on the internet, and they are still alive: open, decentralized and owned by no single company. But the software for reading them is fading. Many newsreaders are no longer maintained, and few feel at home on today's web.

Wardroom is built to keep newsgroups alive. It is a free, open-source, self-hosted newsreader with a modern reading experience: threads shown as conversations, a clean interface in your browser, and decades of discussions within reach. It runs as a single Docker container.

Wardroom works with any server that speaks NNTP, the newsgroup protocol. That can be a Usenet provider, or a standalone news server that is not part of Usenet, such as one run by a project, a company or yourself.

Wardroom is made for text discussions. It does not download binaries or attachments.

### Digital archaeology

Newsgroups hold decades of conversation. Pick any date and read a group as it was back then: the first debates about a new language, forgotten announcements, threads that shaped a community. Wardroom finds the right place on the server in seconds, without downloading everything in between, so a discussion from twenty years ago is as close as today's.

### Find the groups that are still alive

A server can offer tens of thousands of groups, and many of them went quiet long ago. Sort the groups by activity, and Wardroom shows how many articles each one gets per day. The lively ones come first, so you see at a glance where people still talk.

### And everything else you need

- **Threaded discussions:** articles are grouped into threads and shown as a conversation.
- **Subscriptions:** search the groups your server offers, subscribe to the ones you like and see unread counts.
- **Posting:** start new threads and reply to articles.
- **Local cache:** synchronized articles are stored locally, so reading is fast.
- **Ignoring:** hide authors and threads you do not want to see.
- **Simple to run:** one container, one data directory, one owner account, one NNTP server.

<p align="center">
  <img src="docs/images/discover-groups.png" width="800" alt="The discover view: the groups of the server, sorted by activity">
</p>

<p align="center">
  <img src="docs/images/discussion.png" width="800" alt="A discussion opened as a conversation">
</p>

## Quick install

You need Docker with Docker Compose and access to an NNTP server. The image runs on amd64 and arm64, for example on a Raspberry Pi 3, 4 or 5 with a 64-bit operating system.

1. Create a directory for Wardroom and save this file in it as `compose.yaml`:

   ```yaml
   services:
     wardroom:
       image: ghcr.io/stekhub/wardroom:latest
       restart: unless-stopped
       ports:
         - "8119:8119"
       environment:
         - PUID=1000
         - PGID=1000
         - TZ=Etc/UTC
       volumes:
         - ./config:/config
   ```

2. Start Wardroom:

   ```bash
   docker compose up -d
   ```

3. Open `http://localhost:8119` in your browser.

On the first start, a wizard asks for two things: a username and password for your Wardroom account, and the connection details of your NNTP server. After that, Wardroom shows the groups your server offers.

### Settings in the Compose file

| Setting | Meaning |
|---|---|
| `PUID`, `PGID` | User and group ID that Wardroom runs as. Files in `config` belong to this user. |
| `TZ` | Time zone of the container, for example `Europe/Vienna`. |
| `ports` | Wardroom listens on port 8119. To use another port on the host, change the left number, for example `"9000:8119"`. |
| `./config:/config` | The data directory. It holds the database, the encryption key and automatic backups. |

## Documentation

The [user guide](docs/user-guide.md) covers everything beyond the quick install:

- [Backups and updates](docs/user-guide.md#backups-and-updates)
- [Troubleshooting](docs/user-guide.md#troubleshooting): forgotten password, lost key file, more detail in the log
- [Advanced: keeping the encryption key outside the data directory](docs/user-guide.md#advanced-keeping-the-encryption-key-outside-the-data-directory)
- [Building from source](docs/user-guide.md#building-from-source)

For people who want to work on Wardroom:

- [Contribution guidelines](CONTRIBUTING.md): how to report problems and send changes.
- [AI guidelines](docs/ai-guidelines.md): Wardroom is built with the help of an AI coding assistant. This document explains how, and which rules keep humans in control.
