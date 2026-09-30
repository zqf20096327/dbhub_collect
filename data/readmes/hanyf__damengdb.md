# damengdb linux/arm64 docker image

Arm64 version damengdb v8 can be running on your docker environment, for developing purpose.

[Docker Hub Page](https://hub.docker.com/r/hanyf/damengdb)

USAGE:

```shell
docker run -d -p 5236:5236 --restart=always --name damengdb -v ./data/damengdb:/dmdata/data hanyf/damengdb:v1.0
```
