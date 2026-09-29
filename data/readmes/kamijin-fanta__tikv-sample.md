# TiKV Sample

## Requirement

- Docker
- Docker Compose

## Start Server

```bash
$ cd docker-compose
$ sudo docker-compose up -d
```

## View cluster logs

```bash
$ tail docker-compose/logs/pd0.log
```

## Run example codes

```bash
$ sudo docker exec -it tikv-sample_playground_1 bash

$ cd /source/examples/rawkv
$ go run .
```

## Use PD admin tool

```bash
$ sudo docker-compose exec pd0 /pd-ctl help
```
