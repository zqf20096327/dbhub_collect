# pg-opengauss

<span class="badge-npmversion"><a href="https://npmjs.org/package/pg-opengauss" title="View this project on NPM"><img src="https://img.shields.io/npm/v/pg-opengauss.svg" alt="NPM version" /></a></span>
<span class="badge-npmdownloads"><a href="https://npmjs.org/package/pg-opengauss" title="View this project on NPM"><img src="https://img.shields.io/npm/dm/pg-opengauss.svg" alt="NPM downloads" /></a></span>

This is a fork of [node-postgres](https://github.com/brianc/node-postgres) adapted for [openguass](https://gitee.com/opengauss), and upgraded to the latest [node-postgres](https://github.com/brianc/node-postgres) based on [openGauss-connector-nodejs](https://gitee.com/opengauss/openGauss-connector-nodejs)

## Monorepo

This repo is a monorepo which contains the core [pg-opengauss](https://github.com/whyour/pg-opengauss/tree/master/packages/pg-opengauss) module as well as a handful of related modules.

- [pg-opengauss](https://github.com/whyour/pg-opengauss/tree/master/packages/pg-opengauss)
- [pg-opengauss-protocol](https://github.com/whyour/pg-opengauss/tree/master/packages/pg-opengauss-protocol)

## Documentation

Each package in this repo should have its own readme more focused on how to develop/contribute. For overall documentation on the project and the related modules managed by this repo please see:

### :star: [Documentation](https://node-postgres.com) :star:

The source repo for the documentation is available for contribution [here](https://github.com/brianc/node-postgres/tree/master/docs).

### Setting up for local development

1. Clone the repo
2. Ensure you have installed libpq-dev in your system.
3. From your workspace root run `yarn` and then `yarn lerna bootstrap`
4. Ensure you have a PostgreSQL instance running with SSL enabled and an empty database for tests
5. Ensure you have the proper environment variables configured for connecting to the instance
6. Run `yarn test` to run all the tests
