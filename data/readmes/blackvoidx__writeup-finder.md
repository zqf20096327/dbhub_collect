# Writeup Finder

[![Go Version](https://img.shields.io/badge/go-1.17%20%7C%201.18%20%7C%201.19%20%7C%201.20-blue)](https://golang.org/dl/)
[![GitHub Issues](https://img.shields.io/github/issues/blackvoidx/writeup-finder)](https://github.com/blackvoidx/writeup-finder/issues)
[![GitHub Stars](https://img.shields.io/github/stars/blackvoidx/writeup-finder)](https://github.com/blackvoidx/writeup-finder/stargazers)
[![GitHub License](https://img.shields.io/github/license/blackvoidx/writeup-finder)](https://github.com/blackvoidx/writeup-finder/blob/master/LICENSE)

<p>
     <a href="https://skillicons.dev"> 
      <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/GoLang.svg" width="48" title="Go">
      <img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Github-Dark.svg" width="48" title="github">
     </a>
     
</p>

Join our Writeup Hacking supergroup for curated hacking writeups and resources!

📜🔍 https://t.me/writeup_hacking

Writeup Finder is a tool designed to automatically find and save recent writeups from specified URLs. It supports saving the found writeups in a PostgreSQL database, and sending them directly to a Telegram.

```
Writeup-finder is a tool to search for writeups and manage article data, including sending notifications.

Usage:
  writeup-finder [flags]
  writeup-finder [command]

Available Commands:
  completion  Generate autocompletion script
  help        Help about any command

Flags:
      --database       Save new articles in the database
      --help           Show help
      --proxy string   Proxy URL to use for sending Telegram messages
      --telegram       Send new articles to Telegram

Use "writeup-finder [command] --help" for more information about a command.

```


## Features

- Fetch recent writeups from multiple URLs.
- Save writeups to a PostgreSQL database.
- Optionally send notifications of new writeups to a Telegram.
- It filters topics based on the title and sends them to the corresponding topic in the Telegram group.

```
── .env 
├── .env.example 
├── .github/ 
│   └── workflows/ 
│       └── writeup-finder-runner.yml 
├── .gitignore 
├── CHANGELOG.md 
├── README.md 
├── command/ 
│   ├── action.go 
│   ├── command.go 
│   ├── completion.go 
│   └── flags.go 
├── data/ 
│   ├── Youtube_channel.md 
│   ├── keywords.json 
│   └── url.txt 
├── db/ 
│   └── db.go 
├── global/ 
│   └── global.go 
├── go.mod 
├── go.sum 
├── handler/ 
│   ├── handler.go 
│   ├── medium.go 
│   ├── utils.go 
│   └── youtube.go 
├── main.go 
├── run_writeUp-finder.sh 
├── telegram/ 
│   ├── message.go 
│   ├── proxy.go 
│   ├── request.go 
│   └── telegram.go 
├── utils/ 
│   ├── env.go 
│   ├── filters.go 
│   ├── http.go 
│   ├── rss.go 
│   └── utils.go 
└── writeup-finder 
```

## Requirements

- Go 1.16+
- PostgreSQL

## Setup

1. Clone the repository.
2. Install dependencies using `go mod tidy`.
3. Create a `.env` file with the `.env.example` file.
4. Update the `url.txt` file with the URLs you want to monitor.
5. Run the tool with the desired flags.
6. Run `go build -o writeup-finder`

## Usage

| Command                                                                   | Description                                      |
| ------------------------------------------------------------------------- | ------------------------------------------------ |
| `writeup-finder --database`                                               | Save new articles to PostgreSQL database         |
| `writeup-finder [--database] --telegram`                                  | Send new writeups to Telegram                    |
| `writeup-finder [--database] --telegram --proxy=PROTOCOL://HOSTNAME:PORT` | Send new writeups to Telegram with proxy support |

## Flags:
- `--database`       Save new articles in the database
- `--help`           Show help
- `--proxy string`   Proxy URL to use for sending Telegram messages
- `--telegram`       Send new articles to Telegram

Use `writeup-finder [command] --help` for more information about a command.

You can use `CRON` to run script every *hours, *days, or etc.

#### Example for run script every 3 hour

More read: [How to Automate Tasks with cron Jobs in Linux](https://www.freecodecamp.org/news/cron-jobs-in-linux/)

```bash
    0 */3 * * * cd /path/to/your/script && /usr/local/go/bin/writeup-finder -d -t
```
