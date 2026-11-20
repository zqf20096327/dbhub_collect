# Collie: DCB event sourcing for Go

<p align="center">
  <img src="docs/collie.webp" width="375" alt="A border collie with a Go bandana herds sheep through a gate while a gopher ticks them off on a clipboard">
</p>

A Go implementation of [Dynamic Consistency Boundaries](https://dcb.events/) (DCB) event sourcing, including a Postgres event store implementation.

Classic event sourcing fixes its consistency boundaries at design time: one aggregate, one stream, and a rule that spans two aggregates needs a saga. With DCB there are no more aggregates and no more streams. There is one global log of events, every event carries tags, and every decision names the events it depends on with a query. An append is refused when a matching event arrived after the decision read the log.

That is also where the name "Collie" comes from: instead of fixed fences that keep sheep together, a border collie decides dynamically which sheep to round up.

⚠ This is my own experimental implementation of the DCB spec.  
It's currently running stable on one of my own projects (20 million events in the store, increasing every day). But I keep on improving on the interface and the design. I hope to inspire people with this project, and I hope people will start using it, however, which means that sometimes I might break the interfaces to make it even better 😉.

## Install

```sh
go get github.com/DenBeke/collie
```

## A complete example

A username can be claimed once. This program runs as it stands:

```go
package main

import (
	"context"
	"fmt"

	"github.com/DenBeke/collie"
	"github.com/DenBeke/collie/memory"
)

// An event is a struct. Its dcb tag says what the event is a fact about.
type UserSignedUp struct {
	Username string `json:"username" dcb:"tag:username"`
}

// usernameTaken folds the signups for one username into a bool.
func usernameTaken(username string) collie.DefaultProjection[bool] {
	return collie.DefaultProjection[bool]{
		Query: collie.QueryItem{Tags: collie.NewTags("username", username)},
		Handlers: map[string]collie.HandleFunc[bool]{
			"UserSignedUp": func(bool, collie.SequencedEvent) (bool, error) { return true, nil },
		},
	}
}

func signUp(ctx context.Context, store collie.Store, username string) error {
	// 1. Read the events this decision depends on.
	taken := usernameTaken(username)
	condition, err := collie.BuildDecisionModel(ctx, store, &taken)
	if err != nil {
		return err
	}

	// 2. Decide.
	if taken.State {
		return fmt.Errorf("username %q is already taken", username)
	}

	// 3. Append, on the condition that no such event arrived since step 1.
	event, err := collie.NewEventFrom("UserSignedUp", UserSignedUp{Username: username})
	if err != nil {
		return err
	}
	return store.Append(ctx, []collie.Event{event}, condition)
}

func main() {
	ctx := context.Background()
	store := memory.New()

	fmt.Println(signUp(ctx, store, "alice")) // <nil>
	fmt.Println(signUp(ctx, store, "alice")) // username "alice" is already taken
}
```

If two requests claim `alice` at the same moment, both pass step 2, one append succeeds, and the other fails with `ErrAppendConditionViolated`. When the loser tries again, it reads the winner's event and is refused in step 2.

## How it works

![A decision reads the events matching its query, folds them into a state, decides, and appends on the condition that no matching event was added since. On a conflict it retries.](docs/how-it-works.svg)

**Events and tags.** An event has a type, a payload and tags. A tag is a key and a value, such as `username=alice`, and names one thing the event is a fact about. An event can carry several tags, and the same key could have multiple values. `NewEventFrom` takes the tags from `dcb:"tag:<key>"` struct fields. `NewEvent` takes them as an argument. Read a payload back with `collie.EventData[UserSignedUp](event)`.

**Queries.** A `QueryItem` matches events that have one of its `Types` and carry all of its `Tags`. A `Query` is a list of items and matches an event that matches any of them.

**Projections.** A projection is a query and a fold: the events to read, and a handler per event type that turns the current state and one event into the next state. `DefaultProjection[S]` is the ready-made one you can use.

**Decision model and append condition.** `BuildDecisionModel` reads the events for one or more projections in one pass. It returns an `AppendCondition`: the projections' queries, and the position in the log they were read up to. `Append` with that condition fails with `ErrAppendConditionViolated` when an event matching those queries was appended after that position. The consistency boundary is therefore what the decision read, and nothing more. A decision that reads the stock of a product and the credit of a customer is guarded on both, and two decisions that read different things never conflict.

**The log.** Every event in the log has a sequence number. A reader that has read up to a position has seen every matching event at or before it, so a single `uint64` says how far a projection or a condition has come.

`Store` is the event store interface: `Read` and `Append`. The `memory` and `postgres` packages implement it.

## Commands

The `command` package wraps the loop above, including the retry. A command declares its projections and decides from their state:

```go
type SignUp struct {
	Username string `json:"username"`

	taken collie.DefaultProjection[bool]
}

func (c *SignUp) Projections(context.Context) ([]collie.Projection, error) {
	c.taken = usernameTaken(c.Username)
	return []collie.Projection{&c.taken}, nil
}

func (c *SignUp) Decide(context.Context) ([]collie.Event, error) {
	if c.taken.State {
		return nil, fmt.Errorf("username %q is already taken", c.Username)
	}
	event, err := collie.NewEventFrom("UserSignedUp", UserSignedUp{Username: c.Username})
	if err != nil {
		return nil, err
	}
	return []collie.Event{event}, nil
}

err := command.Execute(ctx, store, &SignUp{Username: "alice"}, command.WithMaxAttempts(3))
```

- `Execute` builds the decision model, calls `Decide` and appends with the condition. On a conflict it starts again with a fresh copy of the command. Retrying is opt-in through `WithMaxAttempts`.
- `Projections` and `Decide` run once per attempt, so they must have no side effects. I/O, clocks and generated ids belong in the optional `Prepare` method, which runs once.
- An error from `Decide` is a business refusal: `errors.Is(err, command.ErrCommandRejected)`.
- `command.Registry` dispatches commands by name from a JSON payload, for an HTTP handler or a queue consumer.

## The read side

Reads use projections too, but keep them between requests. A `CheckpointProjection` remembers how far it has read, and `UpdateProjection` applies only the events after that. There are no subscriptions: a read catches its projection up, then answers.

Two general-purpose projections are provided:

| Projection | State | Use it for |
|---|---|---|
| `snapshot.Projection[S]` | One folded value, stored with its position | A total or a counter, and decisions over a long history: `BuildDecisionModel` resumes from the snapshot instead of replaying |
| `postgres.KeyedProjection[V]`, `memory.KeyedProjection[V]` | One value per key | Read endpoints: get one by key, or list with filters, sorting and paging |

```go
// The handler has two methods. Key: which value an event belongs to. Apply: fold it in.
profiles := memory.NewKeyedProjection[UserProfile](
	collie.QueryItem{Types: []string{"UserSignedUp", "UserEmailChanged"}},
	userProfileHandler{},
)

err := collie.UpdateProjection(ctx, store, profiles) // catch up, then serve

entry, found, err := profiles.Get(ctx, "user-123")
page, err := profiles.List(ctx, keyedprojection.ListQuery{
	Where: []keyedprojection.FieldEquals{{Field: "status", Value: "active"}},
	Order: []keyedprojection.SortKey{{Field: "name"}},
	Limit: 20,
})
```

A keyed projection is safe to share between requests. A `snapshot.Projection` is not: create one per request, or guard it with a mutex. More in [`snapshot`](snapshot/README.md) and [`keyedprojection`](keyedprojection/README.md).

### Writing your own

The two above are a starting point. A read model with a shape of its own, such as tables with real columns and joins, a search index or a report, is better written by hand. Any type with these four methods is a `CheckpointProjection`, and `UpdateProjection` drives it like the provided ones:

```go
EventQuery() collie.QueryItem                               // which events to read
Apply(ctx context.Context, e collie.SequencedEvent) error   // fold one event in
After() uint64                                                  // the position read up to
Checkpoint(ctx context.Context, upTo uint64) error              // record the new position
```

`Checkpoint` runs once, after a complete catch-up. A crash before it means the same events are applied again, so make `Apply` idempotent or store the position in the same transaction as the state.

## PostgreSQL

The basic implementation to use is the Postgres store. It's stateless and guarantees consistency between multiple instances.

```go
db, err := gorm.Open(postgres.Open(dsn)) // "gorm.io/driver/postgres"
store := pgstore.New(db)                 // pgstore is "github.com/DenBeke/collie/postgres"
defer store.Close()
err = store.Migrate()                    // creates the tables
```

To guarantee the consistency without losing performance, there are a couple of things to be aware of when using the Postgres implementation:

- **An event is readable a few milliseconds after `Append` returns**, not at once. A second decision on the same boundary inside that window fails with `ErrAppendConditionViolated` and succeeds on a retry. But I suspect eventual consistency is nothing new for people working with event sourcing...
- **Every item in an append condition needs at least a type and a tag**, or `Append` returns `ErrUnkeyableCondition`. The memory store applies the same rule, so a test catches it.

`pgstore.WithGlobalLock()` lifts both limitations, at the price of appends running one at a time and thus being a lot slower. See [`postgres/README.md`](postgres/README.md).

## Optional packages

`collie.NewMiddlewareStore` wraps any `Store` with functions that change events on their way in and out. Envelope, encryption and attachments are built on it. These packages are younger than the core and more likely to change.

| Package | What it does |
|---|---|
| [`reactor`](reactor/README.md) | Handlers that watch the log and answer an event with a side effect or with commands. Delivery is at least once. Run it in one process only. |
| [`envelope`](envelope/README.md) | Stamps every event with who caused it and what it followed from, taken from the context. |
| [`encryption`](encryption/README.md) | Encrypts personal fields with a key per data subject. Deleting the key forgets the subject (crypto-shredding, for GDPR). |
| [`attachments`](attachments/README.md) | Stores large fields in a blob store and puts them back on read. |

## Further reading

- [Dynamic Consistency Boundaries (DCB) for Event Sourcing](https://denbeke.be/blog/software/dynamic-consistency-boundaries-dcb-for-event-sourcing/): why aggregates fall short, and the design of this store's interface.
- [Can DCB event sourcing be fast and flexible? A Postgres benchmark](https://denbeke.be/blog/software/can-dcb-event-sourcing-be-fast-and-flexible-a-postgres-benchmark/): four ways to append, measured.
- [The DCB specification](https://dcb.events/specification/). One difference: the specification's tags are plain strings, and here a tag is a key and a value.
- [State-dependent external work](docs/state-dependent-external-work.md): calling an external system whose input depends on state.
- In Dutch, without code, on the Tandem Studio blog: [event sourcing](https://tandemstudio.be/blog/wat-is-event-sourcing-en-wanneer-loont-het-voor-een-kmo), [DCB](https://tandemstudio.be/blog/wat-is-dynamic-consistency-boundary-event-sourcing), [projections](https://tandemstudio.be/blog/wat-is-een-projectie-event-sourcing) and [the benchmark](https://tandemstudio.be/blog/dcb-event-sourcing-benchmark).
