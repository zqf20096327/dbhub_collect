# Records API

The public endpoint at `/.netlify/functions/api` stores records in Netlify Database. No custom database credentials are required. Netlify applies the table migration during deploy.

- `GET` returns up to 100 records, newest first.
- `POST` accepts a JSON object with `Content-Type: application/json` (up to 16 KiB). It returns `201` and the stored record with `id`, `data`, and `createdAt`.

```sh
curl -X POST -H 'Content-Type: application/json' \
  -d '{"message":"Hello"}' https://<your-site>/.netlify/functions/api
```

This demo has no authentication. Only submit data intended to be public.
