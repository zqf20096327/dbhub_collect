# su3-tidb-playground
Try to use TiDB https://tidbcloud.com

# Setup

## References

- TiDB official guide: https://docs.pingcap.com/ja/tidb/stable/tiup-playground/
- Zenn: https://zenn.dev/koiping/articles/01f62e77d047e6

## 0: Add alias

```zsh
vi ~/.zshrc
```

Add the followings

```zsh
alias mysql='/opt/homebrew/opt/mysql-client/bin/mysql'
```

## 1: Install TiUP

```zsh
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

## 2: Add PD config file

Add [this content](https://github.com/tikv/pd/blob/release-8.1/conf/config.toml) into the new file

```zsh
mkdir ~/config
touch ~/config/pd.toml
vi ~/config/pd.toml
```

```zsh
tiup playground --pd.config ~/config/pd.toml
```

## 3: Boot tiup

### Command

```zsh
tiup playground
```

### Logs

```zsh
su3-tidb-playground % tiup playground
Checking updates for component playground... 
A new version of playground is available:  -> v1.16.2

    To update this component:   tiup update playground
    To update all components:   tiup update --all

The component `playground` version  is not installed; downloading from repository.
download https://tiup-mirrors.pingcap.com/playground-v1.16

...
...
...

3-darwin-arm64.tar.gz 88.73 MiB / 88.73 MiB 100.00% 4.21 MiB/s
Start tiflash instance: v8.5.3
Waiting for tiflash instances ready
- TiFlash: 127.0.0.1:3930 ... Done

🎉 TiDB Playground Cluster is started, enjoy!

Connect TiDB:    mysql --comments --host 127.0.0.1 --port 4000 -u root
TiDB Dashboard:  http://127.0.0.1:2379/dashboard
Grafana:         http://127.0.0.1:3000

```

## 4: Connect mysql

```zsh
mysql --comments --host 127.0.0.1 --port 4000 -u root
```
