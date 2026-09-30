## Use Prisma engine for OceanBase

- Configure env variables.

```bash
export PRISMA_ENGINES_MIRROR=https://oceanbase-prisma-builds.s3.ap-southeast-1.amazonaws.com
export BINARY_DOWNLOAD_VERSION=a4a148a29524ee902a798290fb0db1884aea1d99
```

- Install dependencies including `Prisma` and corresponding engine.

```bash
pnpm i
```

## Database URL

- Add params `?prefer_socket=false&a=.psdb.cloud` into `DATABASE_URL`.
  - `prefer_socket=false`: https://github.com/prisma/prisma/issues/24010
  - `a=.psdb.cloud`: https://github.com/prisma/prisma/issues/18508

```bash
# .env
DATABASE_URL="{OCEANBASE_URL}?prefer_socket=false&a=.psdb.cloud"
```