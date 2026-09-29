# tikv-etcd-shim

I am trying to make an adaptor which implements etcd v3 API, and use TiKV as the backend.

The basic idea is using TiCDC for the watch API.

## TODOs

- [ ] testing utils for A/B testing, the one is etcd, the other one is this shim
- [ ] implement txn KVServer
- [ ] implement watch API
