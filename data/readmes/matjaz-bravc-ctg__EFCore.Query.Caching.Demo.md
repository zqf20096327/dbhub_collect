![](res/Title.jpg)

# Boost EF Core performances using distributed cache

# EF Core

Entity Framework Core is a popular lightweight, open-source, cross-platform, object-relational mapping framework for .NET by Microsoft.
It enables you to work with relational data through domain objects. It is being widely used frequently in high transaction applications where performance and scalability are critical.
But in most high transaction scenarios the database quickly becomes a bottleneck. This is because unlike the application tier where you can add more application servers as you need to scale,
you cannot do the same with the database tier.

# A problem

Typically, we might write a memory cache which supports the calling method cache the entity in memory instead of querying it every time from the database.
But doing so requires a lot of additional work. We have to to manually handle the entity query event and clear the cache every time the entity has been changed or deleted.
This requires a lot of work and changes to our code.

# How can we cache each query and flush the cache every time we know it's updated?

With a second level cache for EF Core: the **[EF Core Second Level Cache Interceptor](https://github.com/VahidN/EFCoreSecondLevelCacheInterceptor)** caches the results of EF Core queries and removes the cached results of a table whenever `SaveChanges` changes that table.
It stores the results in a pluggable cache; this demo uses its **[StackExchange.Redis](https://stackexchange.github.io/StackExchange.Redis/)** provider, which stores them in **[Redis](https://redis.io/docs/about/)**.

# What if our app is running in multiple instances?

Database change by other instances may not apply to other instances and may cause many issues. How can we keep our app available for scale?
By using **[Redis](https://redis.io/docs/about/)** to store our cache! **[Redis](https://redis.io/docs/about/)** is an open source, in-memory data structure store, used as a database, cache and message broker.
It supports data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs,
geospatial indexes with radius queries and streams. **[Redis](https://redis.io/docs/about/)** has built-in replication, Lua scripting, LRU eviction, transactions and different levels of on-disk persistence,
and provides high availability via **[Redis Sentinel](https://redis.io/docs/management/sentinel/)** and automatic partitioning with **[Redis Cluster](https://redis.io/docs/management/scaling/)**.
All instances share the same Redis, so a change saved by one instance removes the cached results for all of them.

# Implementation

In **Program.cs** we register one Redis connection, add the second level cache with the Redis provider, and add its interceptor to the `DbContext`:

```csharp
// One Redis connection, shared by the query cache, the cache endpoints and the health check
builder.Services.AddSingleton<IConnectionMultiplexer>(_ =>
{
  ConfigurationOptions redisOptions = ConfigurationOptions.Parse(redisConnectionString);
  redisOptions.AbortOnConnectFail = false;
  return ConnectionMultiplexer.Connect(redisOptions);
});

// EF Core second level cache: caches the results of every query in Redis and removes
// the cached results of a table when SaveChanges changes it.
builder.Services.AddEFSecondLevelCache(options => options
  .UseStackExchangeRedisCacheProvider(services => services.GetRequiredService<IConnectionMultiplexer>(), queryCaching.ExpirationTimeout)
  .UseCacheKeyPrefix(queryCaching.KeyPrefix)
  // Puts every query in the cache, so calling Cacheable() is not necessary; NotCacheable() excludes a query
  .CacheAllQueries(CacheExpirationMode.Sliding, queryCaching.ExpirationTimeout));
// While Redis is down, queries go to the database instead of failing
builder.Services.AddResilientQueryCache();

builder.Services.AddDbContextPool<DataContext>((services, options) => options
  .UseMySQL(mySqlConnectionString, mySql => mySql.EnableRetryOnFailure(5, TimeSpan.FromSeconds(30), null))
  .AddInterceptors(services.GetRequiredService<SecondLevelCacheInterceptor>()));
```

The queries themselves contain no caching code:

```csharp
public async Task<IReadOnlyList<Network>> GetNetworksAsync(CancellationToken cancellationToken = default) =>
  await context.CityBikesNetworks
    .AsNoTracking()
    .Include(network => network.Location)
    .OrderBy(network => network.Name)
    .ToListAsync(cancellationToken);
```

Redis cache is updated when an entity is changed (insert, update, or delete) via a DbContext that uses this library.
**And you don't have to change any other code!**

**Warning: if the database is updated through a stored procedure, a trigger or another application, the cache becomes stale!**

## When Redis is down

`AddResilientQueryCache()` wraps the cache provider in a `ResilientCacheServiceProvider`:
- a failed cache read counts as a cache miss, so the query goes to the database;
- after a failure the cache is skipped for 30 seconds, so requests do not each wait for the Redis timeout;
- if a table changed while Redis was down, the whole query cache is cleared once Redis is back, so no stale result is served.

(The interceptor's own `UseDbCallsIfCachingProviderIsDown()` is not used: when a Redis read fails, it hands EF Core an empty result and the query fails.)

## Settings

| Setting | Default | |
|---------|---------|---|
| `ConnectionStrings:MySql` | `server=127.0.0.1;user=admin;password=admin;port=3306;database=CityBikes;` | MySQL database |
| `ConnectionStrings:Redis` | `localhost:6379,password=admin` | [StackExchange.Redis configuration](https://stackexchange.github.io/StackExchange.Redis/Configuration) |
| `QueryCaching:ExpirationTimeout` | `00:05:00` | Sliding expiration of cached query results |
| `QueryCaching:KeyPrefix` | `EF_` | Prefix of the Redis keys |
| `CityBikes:BaseUrl` | `https://api.citybik.es/v2/` | Source of the demo data |

They can be overridden with environment variables, for example `ConnectionStrings__Redis`.

## Endpoints

| Method | Route | |
|--------|-------|---|
| `GET` | `/api/v1/citybikes/getcitybikesnetworksasync` | All networks |
| `GET` | `/api/v1/citybikes/searchcitybikesnetworkasync?name=bike` | Networks whose name contains the text |
| `GET` | `/api/v1/rediscache/getrediskeys` | Redis keys of the cached queries |
| `DELETE` | `/api/v1/rediscache/deletecachedrediskeys` | Deletes them and returns how many were deleted |
| `GET` | `/health` | MySQL and Redis health |

At startup the application creates the database and, when it is empty, imports the bike-sharing networks from the [CityBikes API](https://api.citybik.es/v2/).

# Run the solution from Docker

To execute compose file, open Powershell, and navigate to the compose file in the solution's root folder.
Then execute the following command: **docker-compose up -d --build --remove-orphans** (with Podman: **podman compose up -d --build**). To check all running Containers use **docker ps**.

![](res/Docker.jpg)

Navigating to **[http://localhost:9400/swagger/index.html](http://localhost:9400/swagger/index.html)** opens Swagger UI with API v1 (you can open it from Docker container too).
![](res/Swagger.jpg)

By default cache expiration timeout is set to 5 minutes.

![](res/DockerLog.jpg)

# Run the application locally

Start only MySQL and Redis in containers, then run the application:

```bash
docker-compose up -d mysql redis_cache
```

```bash
dotnet run --project src/EFCore.Query.Caching.Demo
```

# Tests

```bash
dotnet test --solution EFCore.Query.Caching.Demo.sln
```

The tests (xUnit v3) need no containers: they run the application with `WebApplicationFactory` on SQLite instead of MySQL, with the in-memory cache provider instead of Redis and a stub instead of the CityBikes API.
They cover the import at startup, the endpoints, that a repeated query is served from the cache until `SaveChanges` changes the table, error responses, and the behaviour of the cache while Redis is down.

# Conclusion
The executed queries complete much faster since they are cached. With a small tweak to the code, we achieved a big performance boost!

Enjoy!

## Prerequisites
- [Visual Studio](https://visualstudio.microsoft.com/vs/) 2026 or greater (or any editor with the .NET SDK)
- [.NET SDK 10.0](https://dotnet.microsoft.com/download/dotnet/10.0)
- [Docker](https://www.docker.com/resources/what-container) or [Podman](https://podman.io/)

## Tags & Technologies
- [.NET 10](https://github.com/dotnet/core/blob/main/release-notes/10.0)
- [Docker](https://www.docker.com/resources/what-container)  
- [CityBikes API Documentation](https://api.citybik.es/v2/)
- [MySQL](https://www.mysql.com/) with [MySQL Connector/NET EF Core provider](https://dev.mysql.com/doc/connector-net/en/connector-net-entityframework-core.html)
- [EF Core Second Level Cache Interceptor](https://github.com/VahidN/EFCoreSecondLevelCacheInterceptor)
- [StackExchange.Redis](https://stackexchange.github.io/StackExchange.Redis/)

## Licence
Licenced under [MIT](http://opensource.org/licenses/mit-license.php).
Contact me on [LinkedIn](https://si.linkedin.com/in/matjazbravc).
