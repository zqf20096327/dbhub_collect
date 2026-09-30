# tikv_toml2json

## Solution 1
Convert rocksdb tikv toml config into toplingdb json config.

toml2json for tikv:
    
1. toml.hpp is from https://github.com/marzer/tomlplusplus
2. Change toml.hpp for replace char '-' to '_' in json key
3. toml2json.cc for convert tikv toml into sideplugin json
4. repo.ImportAutoFile("tikv-toml.json") then
5. repo.ImportAutoFile("tikv-other.json")

config in 4 & 5 will be merged, conf item in 5 will override
which in 4.

There some conf items are not compatible between TiKV and
ToplingDB sideplugin, such as time durations, which are like
"10m", "10ms", ...

## Solution 2

TiKV can also use toml to build DBOptions and CFOptions, then:
```c++
// Build DBOptions and CFOptions by TiKV's toml
std::shared_ptr<DBOptions> dbo = ...;
std::shared_ptr<CFOptions> default_cfo = ...;
std::shared_ptr<CFOptions> lock_cfo = ...;
std::shared_ptr<CFOptions> write_cfo = ...;

repo.Put('dbo', dbo);
repo.Put('default', default_cfo);
repo.Put('lock', lock_cfo);
repo.Put('default', default_cfo);

// Import ToplingDB sideplugin conf, conf items in TiKV's toml
// will be replaced by which in sideplugin.json
repo.ImportAutoFile("sideplugin.json");
```

This solution is perfect.
