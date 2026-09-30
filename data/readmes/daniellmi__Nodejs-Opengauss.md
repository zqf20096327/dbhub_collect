# Node.js + OpenGauss Example

This project demonstrates how to connect a Node.js application to an [openGauss](https://opengauss.org/) database using the [`node-opengauss`](https://github.com/shiqimei/node-opengauss) client library.

Library owner: GitHub - shiqimei/node-opengauss: A simple OpenGauss client for Node.js based on node-postgres. https://lnkd.in/dKRNufSf

## 📚 About

[openGauss](https://opengauss.org/) is an open-source relational database developed by Huawei, based on PostgreSQL. It is designed for enterprise-grade reliability and performance.

The [`node-opengauss`](https://github.com/shiqimei/node-opengauss) library is a Node.js driver for openGauss, offering a simple and familiar API for connecting and querying the database.

## 🧩 Technologies

- **Node.js** (JavaScript runtime)
- **Express** (minimal web framework)
- **node-opengauss** (official Node.js client for openGauss)

## 🔗 Connecting to openGauss

This project uses the following connection configuration:

```js
const config = {
  host: 'localhost',
  port: 26000,
  username: 'omm',
  database: 'cattle',
  password: 'your_password'
};

client.connect(config);
