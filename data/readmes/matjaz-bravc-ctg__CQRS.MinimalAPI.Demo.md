![](res/Title.jpg)

# CQRS Pattern (with Minimal API)
The Command and Query Responsibility Segregation (CQRS) it’s an architectural pattern where the main focus is to separate the way of reading and writing data. This pattern uses two separate models:

**Queries** - are used to read data from the database. Queries objects only return data and do not make any changes. Queries will only contain the methods for getting data. They are used to read the data in the database to return the DTOs to the client, which will be displayed in the user interface.

**Commands** - represent the intention of changing the state of an entity. They execute operations like Insert, Update, Delete. Commands objects alter state and do not return data. Commands represent a business operation and are always in the imperative tense, because they are always telling the application server to do something.

# Benefits of CQRS
Building your architecture using CQRS principles offers many advantages:

* **Separation of concerns**  
When the read and write sides are separate, the models become more maintainable and flexible. The read model is typically simpler, while the write model involves more complex business logic.

* **Independent scaling**  
With CQRS, read and write workloads can scale independently, resulting in fewer lock contentions.

* **Optimized data schemas**  
On the read side, a schema can be optimized for queries, and on the write side, a schema can be optimized for updates.

* **Security**  
It’s easier to ensure that only the right domain entities are performing writes on the data.

* **Simpler queries**  
Application queries can avoid complex joins by storing a materialized view in the read database.

# Implementation
This simple demo is based on the use of **Minimal API** pattern, using the **MediatR** library, **SQLite** database and **Entity Framework Core 10** as an ORM framework.
**Minimal API** is the simple way to build small microservices and HTTP APIs in ASP.NET Core. It hooks into ASP.NET Core's hosting and routing capabilities and allow you to build fully functioning APIs with just a few lines of code.  
 
**Note: this does not replace building APIs with MVC, if you are building complex APIs or prefer MVC, you can keep using it as you always have.**

## How a request flows
1. An **endpoint** (`Endpoints/Students/<Operation>/Endpoint.cs`) receives the HTTP request. Request bodies (`CreateStudentRequest`, `UpdateStudentRequest`) are validated from their data annotations by the built-in Minimal API validation (`AddValidation()`) before the endpoint runs; invalid requests get a `400` with the errors per field.
2. The endpoint sends a **command** or **query** (`Mediator/Commands`, `Mediator/Queries`) through MediatR's `ISender`.
3. Its **handler** (`Mediator/Handlers`) works with the EF Core `DataContext` directly:
   - **command handlers** change data through tracked `Student` entities (the write model);
   - **query handlers** read without change tracking and project straight into `StudentResponse` (the read model).
4. The endpoint returns a typed result (`200`, `404`, ...). Errors are returned as RFC 9457 problem details, never with exception details.

The SQLite database (`Data/Students.db`) is not part of the repository: it is created, migrated and seeded with five demo students when the application starts.

## Endpoints
| Method | Route | Result |
|--------|-------|--------|
| `GET` | `/student/get-all` | All students, ordered by name |
| `GET` | `/student/get-by-id?id=1` | The student, or `404` |
| `GET` | `/student/get-by-name?name=Alan%20Ford` | All students with that name (names are not unique), or `404` |
| `POST` | `/student/create` | The created student, or `400` with validation errors |
| `PUT` | `/student/update` | The updated student, `400` with validation errors, or `404` |
| `DELETE` | `/student/delete?id=1` | `200`, or `404` |
| `GET` | `/health` | `Healthy` when the database is reachable |

`/` redirects to the Swagger UI.

## Running
```bash
dotnet run --project src/CQRS.MinimalAPI.Demo
```
Then open http://localhost:5182.

## Testing
```bash
dotnet test --solution CQRS.MinimalAPI.Demo.sln
```
The tests (xUnit v3) run the real API in memory with `WebApplicationFactory`, each test class on its own temporary SQLite database. They cover every endpoint, validation, error responses, and check that the EF Core migrations match the model.

# Summary
At the end, we split the responsibility into **Command** and **Query**, and we use an **ORM** (Entity Framework Core) for the **Command** side. To improve the benefits, we can synchronize the data into a **NoSQL** database to be consumed from the read side and implement **Event Sourcing**.
**Event Sourcing** ensures that all changes to application state are stored as a sequence of events. Not just can we query these events, we can also use the event log to reconstruct past states, and as a foundation to automatically adjust the state to cope with retroactive changes. But this is another story.

Enjoy!

## Prerequisites
- [Visual Studio](https://visualstudio.microsoft.com/vs/) 2026 or greater (or any editor with the .NET SDK)
- [.NET SDK 10.0](https://dotnet.microsoft.com/download/dotnet/10.0)

## Tags & Technologies
- [.NET 10](https://github.com/dotnet/core/blob/main/release-notes/10.0)
- [SQLite](https://sqlite.org/index.html)
- [MediatR](https://github.com/jbogard/MediatR) 12.x (the last Apache-2.0 release line)
- [Entity Framework Core 10](https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-10.0/whatsnew)

## Licence
Licenced under [MIT](http://opensource.org/licenses/mit-license.php).
Contact me on [LinkedIn](https://si.linkedin.com/in/matjazbravc).
