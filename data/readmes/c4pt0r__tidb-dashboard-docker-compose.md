# tidb-dashboard-docker-compose
Docker-compose scripts for TiDB dashboard components (prometheus, grafana, pushgateway)

It will export pushgateway on port 9091

Usage:

1. docker-compose up -d


2. Specify pushgateway addr in the configuration of TiKV/TiDB/PD

```
[metric]
# prometheus client push interval, set "0s" to disable prometheus.
interval = "15s"
# prometheus pushgateway address, leaves it empty will disable prometheus.
address = "localhost:9091"
```


* Metrics data will store outside the container, default path: ./data
* Pushgateway addr is localhost:9091, Grafana dashboard endpoint is localhost:3000, feel free to change it in docker-compose file.
