# Habitat package: pd-server

## Description

[PD](https://github.com/pingcap/pd) is the Consul of [TiDB](https://github.com/pingcap/tidb) (which is really just [etcd](https://github.com/coreos/etcd) under the covers with some fliar).

This package attempts to automate the running of a PD Cluster.

## Usage

Refer to parent project [Habitat TiDB Documentation](https://github.com/qubitrenegade/habitat-tidb-server) for full usage instructions.


[Docker Hub](https://hub.docker.com/r/qbrd/pd/)

```
# run this x3
docker run qbrd/pd --peer 172.17.0.3 --peer 172.17.0.5 --topology leader
```

Seems to work in limited testing.


```
$ curl http://172.17.0.4:2379/v2/members 2>/dev/null | jq    
{
  "members": [
    {
      "id": "1af57124460c9172",
      "name": "0226d8f47626",
      "peerURLs": [
        "http://172.17.0.5:2380"
      ],
      "clientURLs": [
        "http://172.17.0.5:2379"
      ]
    },
    {
      "id": "660aa483274d103a",
      "name": "d292cd6ad4a3",
      "peerURLs": [
        "http://172.17.0.3:2380"
      ],
      "clientURLs": [
        "http://172.17.0.3:2379"
      ]
    },
    {
      "id": "ad0233873e2a0054",
      "name": "65c7aa293f48",
      "peerURLs": [
        "http://172.17.0.4:2380"
      ],
      "clientURLs": [
        "http://172.17.0.4:2379"
      ]
    }
  ]
}
```

Welcome any feedback...
