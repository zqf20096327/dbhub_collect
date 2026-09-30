



基于 Nacos 3.1.1 官方版本，添加达梦数据库（DM）支持。

## 主要修改

- 添加达梦数据库插件 `nacos-dm-datasource-plugin-ext` 相关代码

## 编译

```bash
mvn -Prelease-nacos -Dmaven.test.skip=true -Dpmd.skip=true -Drat.skip=true -Dcheckstyle.skip=true clean install -U
```

