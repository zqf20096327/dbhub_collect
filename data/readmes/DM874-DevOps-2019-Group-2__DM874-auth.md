# DM874-auth
## Description
This service is a standalone service that generates JWT tokens, signed with a secret.

These JWT tokens are "proof" of an authenticated action, and can be used anywhere when they have been generated with the right secret.

## Interface
This service has 3 routes:
* register: { username: string, password: string } -> { $type: Success | Error, payload: string }
* login: { username: string, password: string } -> { $type: Success | Error, payload: string }
* users: -> [[userId: int, username: string]]

These routes can be called at any time and the service is completely stateless as it is basically a proxy for the JWT secret and database.

## Configuration
The service is configurable though the configmap in kubernetes (also supplied in the repository). The service also more fine-tunely configurable though the `application.conf` file in HOCON format (typesafe config).
