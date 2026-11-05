# dokku postgres [![Build Status](https://img.shields.io/github/actions/workflow/status/dokku/dokku-postgres/ci.yml?branch=master&style=flat-square "Build Status")](https://github.com/dokku/dokku-postgres/actions/workflows/ci.yml?query=branch%3Amaster) [![IRC Network](https://img.shields.io/badge/irc-libera-blue.svg?style=flat-square "IRC Libera")](https://webchat.libera.chat/?channels=dokku)

Official postgres plugin for dokku. Currently defaults to installing [postgres 18.6](https://hub.docker.com/_/postgres/).

## Requirements

- dokku 0.35.x+
- docker 1.8.x

## Installation

```shell
# on 0.35.x+
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git --name postgres
```

## Commands

```
postgres:app-links [<app>]                         # list all Postgres service links for a given app
postgres:backup <service> <bucket-name> [--id <id>] [-u|--use-iam] [--all-databases] # create a backup of the Postgres service to an existing s3 bucket
postgres:backup-auth <service> <aws-access-key-id> <aws-secret-access-key> <aws-default-region> <aws-signature-version> <endpoint-url> [--id <id>] # set up authentication for backups on the Postgres service
postgres:backup-deauth <service> [--id <id>]       # remove backup authentication for the Postgres service
postgres:backup-logs <service> [-t|--tail [<tail-num>]] # print the most recent output of the scheduled backups of the service
postgres:backup-schedule <service> <schedule> <bucket-name> [--id <id>] [-u|--use-iam] # schedule a backup of the Postgres service
postgres:backup-schedule-cat <service> [--id <id>] # cat the crontab line of a scheduled backup for the service
postgres:backup-set-encryption <service> <passphrase> [--id <id>] # set encryption for all future backups of Postgres service
postgres:backup-set-public-key-encryption <service> <public-key-id> [--id <id>] # set GPG Public Key encryption for all future backups of Postgres service
postgres:backup-unschedule <service> [--id <id>|--all] # unschedule the backup of the Postgres service
postgres:backup-unset-encryption <service> [--id <id>] # unset encryption for future backups of the Postgres service
postgres:backup-unset-public-key-encryption <service> [--id <id>] # unset GPG Public Key encryption for future backups of the Postgres service
postgres:certificate <service>                     # print the certificate the Postgres service encrypts connections with
postgres:clone <service> <new-service> [--clone-flags...] # create container <new-name> then copy data from <name> into <new-name>
postgres:connect <service> [--database <database>] [--user <user>] # connect to the service via the postgres connection tool
postgres:create <service> [--create-flags...]      # create a Postgres service
postgres:create-database <service> <database>      # create a database in the Postgres service
postgres:create-user <service> <user> [<password>] # create a user in the Postgres service
postgres:destroy <service> [-f|--force]            # delete the Postgres service/data/container if there are no links left
postgres:destroy-database <service> <database> [-f|--force] # destroy a database created in the Postgres service
postgres:destroy-user <service> <user> [-f|--force] # destroy a user created in the Postgres service
postgres:enter <service>                           # enter or run a command in a running Postgres service container
postgres:exists <service>                          # check if the Postgres service exists
postgres:export <service> [-f|--file <path>] [--force] [--all-databases] [--database <database>] [-- <export-args...>] # export a dump of the Postgres service database
postgres:expose <service> <ports...>               # expose a Postgres service on custom host:port if provided (random port on the 0.0.0.0 interface if otherwise unspecified)
postgres:import <service> [-f|--file <path>] [--all-databases] [--database <database>] [-- <import-args...>] # import a dump into the Postgres service database
postgres:info 

[...截断...]

[<service>] [--info-flags...]        # print the service information
postgres:label <service> <key=value>...            # add docker labels to the service container
postgres:link <service> [<app>] [--link-flags...]  # link the Postgres service to the app
postgres:link-migrate <service> [<app>]            # move apps linked to the Postgres service off the deprecated docker link and onto a network
postgres:linked <service> [<app>]                  # check if the Postgres service is linked to an app
postgres:links <service>                           # list all apps linked to the Postgres service
postgres:list                                      # list all Postgres services
postgres:logs <service> [-t|--tail [<tail-num>]]   # print the most recent log(s) for this service
postgres:mount [--replace] <service> <source:container-dir[:options]>... # mount a host path or docker volume into the service container
postgres:pause <service>                           # pause a running Postgres service
postgres:promote <service> [<app>]                 # promote service <service> as DATABASE_URL in <app>
postgres:reexpose <service>                        # reexpose a Postgres service, applying its expose settings
postgres:reset <service> [-f|--force] [--database <database>] # delete all data in the Postgres service, keeping the service and its links
postgres:restart <service>                         # graceful shutdown and restart of the Postgres service container
postgres:set <service> <key> [<value>] [--id <id>] # set or clear a property for a service
postgres:set-user-password <service> <user> [<password>] [-n|--no-restart] # change the password of a user created in the Postgres service
postgres:start <service>                           # start a previously stopped Postgres service
postgres:stop <service>                            # stop a running Postgres service
postgres:unexpose <service>                        # unexpose a previously exposed Postgres service
postgres:unlabel [--all] <service> [<key>...]      # remove one or all docker labels from the service container
postgres:unlink <service> [<app>] [-n|--no-restart] # unlink the Postgres service from the app
postgres:unmount [--all] <service> [<source:container-dir>...] # remove one or all mounts from the service container
postgres:upgrade <service> [--upgrade-flags...]    # upgrade service <service> to the specified versions
postgres:upgrade-cleanup <service>                 # remove the data an upgrade across a major version kept aside
```

## Usage

Help for any commands can be displayed by specifying the command as an argument to postgres:help. Plugin help output in conjunction with any files in the `docs/` folder is used to generate the plugin documentation. Please consult the `postgres:help` command for any undocumented commands.

### Basic Usage

### create a Postgres service

```shell
# usage
dokku postgres:create <service> [--create-flags...]
```

flags:

- `--backend <string>`: the execution backend to create the service with, docker or compose (default: docker)
- `-c|--config-options <string>`: extra arguments for the process the service container runs, not docker flags; use mount for mounts
- `-C|--custom-env <string>`: semi-colon delimited environment variables to start the service with
- `--definition <string>`: the definition to run the service on, instead of the one its image and version resolve to
- `-i|--image <string>`: the image name to start the service with
- `-I|--image-version <string>`: the image version to start the service with
- `-N|--initial-network <string>`: the initial network to attach the service to
- `--label <stringArray>`: a docker label to put on the service container, as <key>=<value>, repeatable
- `--log-driver <string>`: the docker logging driver to run the service container with (default: the daemon's own)
- `--log-opt <strings>`: a comma-separated list of key=value docker log options for the service container
- `-m|--memory <int>`: contain