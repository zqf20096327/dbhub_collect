# tidbyte-client

Client for [tidbyte](https://github.com/flikmsg/tidbyte)

### Usage

```javascript
const TidbyteClient = require('tidbyte-client')

// You can optionally pass in a tidbyte server URL.
// Otherwise, it will use the public lookup.flik.im
const client = new TidbyteClient(/* url */)

client.lookup('https://www.google.com')
    .then(console.log)
    .catch(a => console.error(a))

async function example() {
    try {
        console.log(await client.lookup('https://apple.com'))
    } catch (e) {
        console.error('It failed!')
        console.error(e)
    }
}
```

### TODO

* Proxy streaming from server