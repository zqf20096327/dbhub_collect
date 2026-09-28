
# oceanbase-cubejs-driver

## Usage

* cube.js

```code
// Cube.js configuration options: https://cube.dev/docs/config
const {OceanBaseQuery,OceanBaseDriver} = require("oceanbase-cubejs-driver")
module.exports = {
    dialectFactory: (dataSource) => {
        // need config  datasource  for multitenant env
        return OceanBaseQuery
    },
    dbType: ({ dataSource } = {}) => {
        return "oceanbase"
    },
    driverFactory: ({ dataSource } = {}) => {
        return new OceanBaseDriver({
            host: xxxxxx,
            port:xxxx,
            database: xxxx,
            user:xxx,
            password: xxxx
        })
    }
};
```