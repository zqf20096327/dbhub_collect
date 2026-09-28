# Express + GraphQL + TypeORM Example

## Frameworks

- **Express**
- **Express GraphQL**
- **GraphQL**
- **TypeORM**

## Setup

- TypeScript
- Mysql
- Docker

### UP

```
docker-compose up

http://localhost:3000/graphiql

```

## Query

Save Author

```
mutation {
  saveAuthor(firstName:"Mateus", lastName: "Constanzo") {
    id,
    name,
    firstName,
    lastName,
  }
}
```

Get all Author

```
{
  authors {
    id,
    name,
    firstName,
    # lastName
  }
}
```