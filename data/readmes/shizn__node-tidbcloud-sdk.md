# node-tidbcloud-sdk-v1-beta

Unofficial Node.js management plane SDK for [TiDB Cloud OpenAPI v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta)

The majority of the codes are auto-genenrated by [openapi-generator](https://openapi-generator.tech/docs/generators/typescript-node)

```bash
 openapi-generator-cli generate -i tidbcloud-oas.json -g typescript-node -o node-tidbcloud-sdk/  --additional-properties=npmName=tidbcloud-sdk
```
# Get started

1. [Create your project and cluster on TiDB Cloud for free.](https://tidb.cloud)
2. Create your API Key by following the [steps here](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started). 
3. Check `client.ts` file. Store your API Key into env var, restore npm packages and run `client.ts`.


