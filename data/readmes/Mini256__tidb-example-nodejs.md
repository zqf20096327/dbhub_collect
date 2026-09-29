# TiDB Examples for Node.js Developers (👷Work in progress)

This repository is a set of TiDB sample code for Node.js developers, which is written in TypeScript and JavaScript.

Due to TiDB's MySQL compatibility, most of the examples are also applicable and valuable to the developers who using MySQL and MariaDB databases.

## Getting started

### Development environment

If you are developing locally, you need to clone the repository to your local machine and please install the following tools:

- [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)
- Node.js >= 16.x

Alternatively, you can use the cloud-native development environment GitHub Codespaces or GitPod to open the sample code repository, where the above tools are already installed in advance. 

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/pingcap-inc/tidb-example-nodejs)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/pingcap-inc/tidb-example-nodejs)

### Create a TiDB cluster

You can use TiDB Cloud to [create a free serverless TiDB cluster](https://tidbcloud.com/free-trial?utm_source=github&utm_medium=referral&utm_campaign=developer-sample-code), which is convenient for you to develop and test applications.

### Checkout the sample code

In this code repository, the sample code will be organized and divided into directories according to the type of ORM or Driver. 

There is a README.md file in each directory, which will introduce how to run the sample code.

## Examples

### Driver / ORM

For Driver, we recommend using mysql2 for development.

| Name                                                             | Category        | Examples                           |
|------------------------------------------------------------------|-----------------|------------------------------------|
| [mysqljs/mysql](https://github.com/mysqljs/mysql)                | `Driver`        | [➡️ Examples (WIP)](./node_mysql)  |
| [mysql2](https://github.com/sidorares/node-mysql2) (Recommended) | `Driver`        | [➡️ Examples (WIP)](./node_mysql2) |
| [knex/knex](https://github.com/knex/knex)                        | `Query Builder` | TODO                               |                                
| [TypeORM](https://github.com/typeorm/typeorm)                    | `ORM`           | TODO                               |
| [Prisma](https://github.com/prisma/prisma)                       | `ORM`           | TODO                               |
| [Sequelize](https://github.com/sequelize/sequelize)              | `ORM`           | TODO                               |

### Advanced Topics

- Integration with Vercel Serverless Functions (TODO)
- Developing with the TiDB Cloud Data API in a Node.js application (TODO)
- Use TiDB Cloud API to manage clusters (TODO)
- Using Template literals to simplify 

## Support

If you encounter problems related to TiDB during development, you can get help in the following ways:

- [TiDB Forum](https://ask.pingcap.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/tidb) (Please add the `tidb` tag to the question)

Regarding the possible problems with the contents of this repository or the sample code, you can get help in the following ways:

- [GitHub Issue](https://github.com/pingcap-inc/tidb-example-nodejs/issues/new)

## Contributing

TBD

## License

[Apache 2.0 License](./LICENSE)