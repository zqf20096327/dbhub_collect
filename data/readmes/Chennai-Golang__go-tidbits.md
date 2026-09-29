Go Tidbits
----------

Some go language surprises and goodies.

  * init()

> $ go run main.go

  * go:generate magic comments

> $ go generate

  Eg: [Gorm postgres dialect][GormPostgres] which imports [lib/pq][libPQ]


[GormPostgres]: https://github.com/jinzhu/gorm/blob/master/dialects/postgres/postgres.go#L7
[libPQ]: https://github.com/lib/pq/blob/d34b9ff171c21ad295489235aec8b6626023cd04/conn.go#L48
