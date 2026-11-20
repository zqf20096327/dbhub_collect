# .NET Learning Journey


> A personal learning log for C#, ASP.NET Core, Entity Framework Core, SQL Server and backend fundamentals — with notes, runnable C# examples and DSA solutions.


[![GitHub stars](https://img.shields.io/github/stars/Daimx1214/dotnet-learning-journey)](https://github.com/Daimx1214/dotnet-learning-journey/stargazers)

[![GitHub forks](https://img.shields.io/github/forks/Daimx1214/dotnet-learning-journey)](https://github.com/Daimx1214/dotnet-learning-journey/network/members)

[![License: MIT](https://img.shields.io/github/license/Daimx1214/dotnet-learning-journey)](LICENSE)

[![.NET](https://img.shields.io/badge/.NET-512BD4?logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)


## About

Hi, I'm **Daim Ali**, a BS Computer Science student at **MNS University of Agriculture, Multan** (CGPA 3.88). I'm learning .NET development — C#, ASP.NET Core, Entity Framework Core and SQL Server — and sharing everything I learn in this repository so I can track my progress, help others learning the same stack and build in public.


I also practice competitive programming — 200+ problems solved on LeetCode and CodeChef.


- 🌐 Portfolio: <https://daim-portfolio-wine.vercel.app>
- 💼 LinkedIn: <https://www.linkedin.com/in/daimx1214>
- 📅 Repository started: 2026-10-28. Current focus: ASP.NET Core backend fundamentals.


## What's inside

- **`notes/`** — 213 learning notes across C#, ASP.NET Core, EF Core, SQL Server and data structures & algorithms. Each note is a short, focused write-up of one concept.

- **`examples/`** — Runnable C# code: two pointers, sliding window, binary search, recursion, sorting, LINQ queries, dynamic programming, LINQ deferred execution, graph traversal (BFS/DFS), heaps (with PriorityQueue), stacks/queues (with a balanced-brackets checker), tries (with insert, search and prefix search) and greedy algorithms (activity selection, coin change and fractional knapsack) and monotonic stacks (next greater element and largest rectangle in a histogram) and Bellman-Ford shortest paths (with negative weights and cycle detection) and segment trees with lazy propagation (range adds and range sums). Drop a file into a console project (or a C# script runner) and run it.

- Topics are organized by area: `notes/csharp/`, `notes/aspnet/`, `notes/efcore/`, `notes/sql/` and `notes/dsa/`.


## Topics covered

### C#

Language fundamentals and OOP, value vs reference types, records, tuples, pattern matching, generics, interfaces, delegates and events, extension methods, async/await, yield iterators, nullable reference types, exception handling, string interpolation and LINQ basics. SOLID principles, design patterns (Singleton, Factory, Strategy, Repository, Observer, Decorator), Docker for .NET apps and unit testing with xUnit and Moq. CQRS with MediatR, clean architecture, Dapper, Span and Memory, and System.Threading.Channels. Source generators and async streams (IAsyncEnumerable). Cancellation tokens, primary constructors, reflection basics and garbage collection. Immutable collections, custom attributes, parallel programming with Parallel and PLINQ, and System.Text.Json serialization. Expression trees, operator overloading and benchmarking with BenchmarkDotNet. Collection expressions (C# 12) and unsafe code with pointers. TimeProvider abstraction for testable time, frozen collections (FrozenDictionary and FrozenSet), keyed services (.NET 8) and advanced LINQ operators (Chunk, DistinctBy, MaxBy). IEnumerable vs IQueryable, Task vs ValueTask, ConfigureAwait, enums and flags, and DateOnly/TimeOnly. System.IO.Pipelines for high-performance parsing, generic math with INumber<T>, ArrayPool memory pooling, IAsyncDisposable, lazy initialization, thread synchronization primitives, ref returns and ref locals, dynamic and ExpandoObject, Func/Action/Predicate, Index and Range operators, and required and init-only members.

### ASP.NET Core

Web APIs, routing, controllers, dependency injection, middleware, model binding, validation, configuration, logging and minimal APIs. JWT authentication and refresh tokens, authorization policies and claims, SignalR, gRPC, the Options pattern, background services, API versioning, rate limiting, Serilog structured logging, Swagger/OpenAPI, Redis distributed caching, HttpClientFactory and output caching. Problem Details (RFC 7807) error responses. Endpoint filters, distributed caching with IDistributedCache and Blazor basics. ASP.NET Core Identity, GraphQL basics, raw WebSockets, Quartz.NET scheduling and response compression. Razor Pages, MVC controllers, localization and globalization, the Data Protection API and security headers. OpenTelemetry observability and antiforgery tokens. API key authentication, feature flags with Microsoft.FeatureManagement and HTTP resilience with Polly (retry, circuit breaker, timeout). HybridCache, cookie authentication, YARP reverse proxy and external login providers (Google/GitHub). Hosting models and Kestrel, server-sent events and gRPC streaming.

### Entity Framework Core

DbContext and models, CRUD operations and migrations. Change tracking, loading strategies, relationships and performance (AsNoTracking, projections, compiled queries, split queries), raw SQL queries, value converters, global query filters and optimistic concurrency tokens. Owned entity types, soft delete, shadow properties and interceptors. Data seeding with HasData. Inheritance mapping (TPH, TPT, TPC), bulk operations with ExecuteUpdate and ExecuteDelete, and temporal tables for point-in-time history. JSON columns for owned types. Split queries and async query patterns.

### SQL Server

Joins, indexes, transactions, stored procedures, CTEs and window functions. GROUP BY and HAVING, views, database normalization, execution plans, index deep dives, locking and isolation levels, and query optimization. Temp tables vs table variables, the MERGE statement, PIVOT and UNPIVOT, and deadlocks. Triggers for auditing and enforcing rules. Table partitioning for large tables. Set operations (UNION, INTERSECT, EXCEPT), correlated subqueries, columnstore indexes and row-level security. Parameter sniffing, filtered indexes and full-text search. Recursive CTEs and dynamic SQL.

### Data structures & algorithms

Two pointers, sliding window, binary search, hashmaps, linked lists, stacks and queues, recursion and binary trees — with runnable C# examples in `examples/`. Plus graphs and heaps, with sorting and dynamic programming examples. Also dynamic programming basics, greedy algorithms, tries and segment trees. Also binary search trees, union-find, topological sort and Dijkstra's shortest path. Also backtracking, AVL trees, B-trees, the knapsack problem and KMP string matching. Also red-black trees, Bloom filters, the LRU cache, bit manipulation and prefix sums — with a runnable trie example. Also minimum spanning trees (Kruskal and Prim), A* search and advanced dynamic programming (LCS, edit distance, LIS) — with a runnable greedy-algorithms example. Also Floyd–Warshall all-pairs shortest paths, monotonic stacks, Fenwick trees and Rabin–Karp string matching — with a runnable monotonic-stack example. Also Bellman-Ford shortest paths — with a runnable example — longest common subsequence, the coin change problem, merge intervals and trapping rain water. Segment tree lazy propagation and binary search on the answer.


## Learning roadmap

- Deepen ASP.NET Core — model binding, validation and building complete Web APIs.
- Deepen EF Core — relationships, migrations and querying.
- Keep up DSA practice with new C# examples.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add a note or an example.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
