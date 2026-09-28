# postgres-logging
Postgresql docker container which logs queries to stdout.

This project extends from the regular postgres images.

## Running

Run the development postgres container by executing the following command. This will use the latest postgres version.

```bash
docker run -p 127.0.0.1:5432:5432 --name postgres-logging timms/postgres-logging
```

You might want to run a specific version for your project's needs by defining a tag. The versions defined below are available as docker tags.

```bash
docker run -p 127.0.0.1:5432:5432 --name postgres-logging timms/postgres-logging:14.4
```

*note: In case you run docker-machine, bind to 0.0.0.0 instead of localhost*

## Versions
Note that versions are available as branches.


The following versions are available:

* 15.1
* 15.0
* 14.4
* 14.0
* 13.4
* 12.0
* 11.5
* 11.1
* 11.0
* 10.6
* 10.5
* 10.4
* 10.3
* 10.2
* 10.1
* 10.0
* 9.6
* 9.5
* 9.4
* 9.3
* 9.2
* 9.1
