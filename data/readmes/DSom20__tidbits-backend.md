# Tidbits-backend

This is the backend repo for the Tidbits project

The frontend can be found at https://github.com/DSom20/tidbits-frontend

## How to Start Locally
1. Clone repo and `cd` into it
2. `npm install`
3. `npm start`

## Testing
1. `npm test`

## Technologies
Node, Express, Jest, Supertest

### Notes:
Stores an array of strings

Provides two endpoints:
* GET /tidbits --> get the strings, returns as { tidbits: [/strings/])
* POST /tidbits --> expects request body of { tidbit: /string/ }, prepends string to stored array, returns { tidbit: /string/ } on success
