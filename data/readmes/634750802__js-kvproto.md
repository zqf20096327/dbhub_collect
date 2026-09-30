# kvproto

Compiled [TiKV](https://tikv.org) protobuf lib, generated from [pingcap/kvproto](https://github.com/pingcap/kvproto) by [protobufjs](https://github.com/protobufjs/protobuf.js).

## Installation

```shell
npm i js-kvproto
```

## Usage

See [protobufjs](https://github.com/protobufjs/protobuf.js)

### gRPC

```javascript
const grpc = require('grpc')
const { pdpb } = require('js-kvproto')

const Client = grpc.makeGenericClientConstructor({})
const client = new Client(
  '127.0.0.1:2379',
  grpc.credentials.createInsecure()
)

const rpcImpl = prefix => (method, requestData, callback) => {
  client.makeUnaryRequest(
    `/${prefix}/${method.name}`,
    arg => arg,
    arg => arg,
    requestData,
    null,
    null,
    callback
  )
}

const pd = pdpb.PD.create(rpcImpl('pdpb.PD'), false, false)

async function main () {
  const members = await pd.getMembers({})

  console.log(members)
}

main().then()
```
