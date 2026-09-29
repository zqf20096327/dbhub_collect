# java-tidbcloud-sdk-v1

[中文](/README-zh.md) | English

> **Note:**
>
> This repo based on [c4pt0r/go-tidbcloud-sdk-v1](https://github.com/c4pt0r/go-tidbcloud-sdk-v1).

Unofficial Java wrapper for [TiDB Cloud OpenAPI v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta)

Most generated code are from offical OpenAPI specification(Swagger 2.0, JSON): https://download.pingcap.org/tidbcloud-oas.json

Codegen:

```bash
wget -nc https://oss.sonatype.org/content/repositories/releases/io/swagger/swagger-codegen-cli/2.2.1/swagger-codegen-cli-2.2.1.jar

java -jar swagger-codegen-cli-2.2.1.jar generate \
    -i https://download.pingcap.org/tidbcloud-oas.json \
    -l java \
    --group-id com.github.icemap \
    --artifact-version 0.0.1 \
    --git-user-id Icemap \
    --model-package com.github.icemap.model \
    --api-package com.github.icemap.api \
    --invoker-package com.github.icemap.invoker
```

You can generate other program language follow the [documentation](https://swagger.io/docs/open-source-tools/swagger-codegen/) from swagger codegen.

## Usage

1. Register TiDB Cloud (free & easy): https://tidb.cloud
2. Create an API Key, follow the document here: https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started
3. See [example/main.go](https://github.com/c4pt0r/go-tidbcloud-sdk-v1/blob/master/example/main.go) for more detail usage

Enjoy it! 😉
