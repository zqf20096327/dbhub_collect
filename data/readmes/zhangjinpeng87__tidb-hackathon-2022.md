# tidb-hackathon-2022

随着 TiDB 的使用越来越广，一家公司内部的不同业务使用 TiDB 是很常见的现象，但是这些公司面临一个成本和运维问题，就是每个业务单独使用一套 TiDB Cluster，机器成本和运维成本比较高，因为 TiDB Cluster 的生产系统起步配置一般为 3 PD 3 TiKV 2 TiDB。如果直接让多个业务使用一套 TiDB Cluster，如何保证某些关键业务的性能成为挑战。所以本次 Hackathon 我们想在多业务/用户共享一套 TiDB Cluster 这块获得一些突破，以达到：

- TiDB Cloud 上多个用户共享 TiDB Cluster，使 TiDB Cloud 具备提供 Shared TiDB Cluster Tier 的能力，降低 TiDB Cloud 生产系统的入门门槛
- 同一家企业内部，多个业务共享一套 TiDB Cluster，保证一些关键业务的响应时间，降低整体运维成本和机器成本
