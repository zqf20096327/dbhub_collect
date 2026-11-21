# django-pg-sse

[![Tests](https://img.shields.io/github/actions/workflow/status/oliverandrich/django-pg-sse/test.yml?branch=main)](https://github.com/oliverandrich/django-pg-sse/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/django-pg-sse.svg)](https://pypi.org/project/django-pg-sse/)
[![Docs](https://readthedocs.org/projects/django-pg-sse/badge/?version=latest)](https://django-pg-sse.readthedocs.io/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/pypi/l/django-pg-sse)](https://github.com/oliverandrich/django-pg-sse/blob/main/LICENSE)
[![Django versions](https://img.shields.io/pypi/frameworkversions/django/django-pg-sse)](https://pypi.org/project/django-pg-sse/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-pg-sse)](https://pypi.org/project/django-pg-sse/)
[![Downloads](https://static.pepy.tech/badge/django-pg-sse)](https://pepy.tech/project/django-pg-sse)
[![Downloads/month](https://static.pepy.tech/badge/django-pg-sse/month)](https://pepy.tech/project/django-pg-sse)

Documentation: <https://django-pg-sse.readthedocs.io/>, with the
[settings](https://django-pg-sse.readthedocs.io/en/latest/settings.html), a
[deployment guide](https://django-pg-sse.readthedocs.io/en/latest/deployment.html),
[presence](https://django-pg-sse.readthedocs.io/en/latest/presence.html) and an
[API reference](https://django-pg-sse.readthedocs.io/en/latest/api.html).

Server-sent events for Django over PostgreSQL `LISTEN`/`NOTIFY`. Push HTML from any process to the
open browsers of a topic, with replay after a reconnect. No Redis, no message broker.

Built for [htmx 4](https://four.htmx.org) and its `hx-sse` extension, but any SSE client works.

[django-pg-sse-demo](https://github.com/oliverandrich/django-pg-sse-demo) is a small chat built on django-pg-sse, htmx 4 and daisyUI.

## Requirements

- Python 3.12 or newer, Django 5.2 or newer
- PostgreSQL and psycopg 3.3.9 or newer
- Middleware that sets `request.user`, such as `AuthenticationMiddleware`; the check `pg_sse.W001` warns without it.
  A session is optional: without one, `close_streams(session=...)` reaches no stream.
- An ASGI server such as granian, uvicorn or daphne. `runserver` speaks WSGI and cannot stream an
  async response.

## Installation

```shell
uv add django-pg-sse
```

```python
INSTALLED_APPS = [
    # ...
    "django_pg_sse",
]
```

```python
# urls.py
urlpatterns = [
    # ...
    path("events/", include("django_pg_sse.urls")),
]
```

Run `manage.py migrate` to create the event table.

## Usage

Send HTML to a topic. The event goes out when the current transaction commits; a rollback sends
nothing. A topic has at most 200 characters and an event name at most 100; `broadcast()` raises
`ValueError` for longer ones.

```python
from django_pg_sse import broadcast

html = '<ul id="news" hx-swap-oob="beforeend"><li id="news-7">Hi</li></ul>'
broadcast("public:news", html)
```

A page opens one stream for all its topics:

```html
<ul id="news"></ul>
<div hx-sse:connect="{% url 'pg_sse:stream' %}?topic=public:news{% if user.is_authenticated %}&topic=user:{{ user.pk }}{% endif %}"></div>
```

The default policy opens `public:` topics to everyone and `user:<pk>` to that user.
Other kinds, such as `room:`, need a policy of their own; see [Who may read a topic](#who-may-read-a-topic).

htmx swaps each message. Elements with `hx-swap-oob` or `<hx-partial>` update the page anywhere.
A stream sends no event twice; a reconnect resumes after the browser's `Last-Event-ID`.
A page can still show an element before its stream delivers the same event.
The hub's catch-up after a lost `LISTEN` connection is one such case.
htmx 4 appends with `beforeend` without comparing ids.
A target that skips an existing element prevents the second copy:

```html
<ul hx-swap-oob='beforeend target:"#news:not(:has(> #news-7))"'><li id="news-7">Hi</li></ul>
```

### From async code

`broadcast()`, `broadcast_json()` and `close_streams()` register with `transaction.on_commit()`.
Django allows that only in sync code; async code gets `SynchronousOnlyOperation`.
Async code awaits `abroadcast()`, `abroadcast_json()` and `aclose_streams()` instead.

```python
from django_pg_sse import abroadcast


async def post_message(request, room_pk):
    message = await Message.objects.acreate(room_id=room_pk, text=request.POST["text"])
    await abroadcast(f"room:{room_pk}", render_to_string("chat.html#message", {"message": message}))
```

### JSON for client code

`broadcast_json()` sends a value as JSON, encoded with `DjangoJSONEncoder`. It needs an event name.

```python
from django_pg_sse import broadcast_json

broadcast_json(f"room:{room.pk}", {"online": 12}, event="presence")
```

htmx dispatches a named event as a DOM event on the element with `hx-sse:connect`. The event
bubbles, and `event.detail.data` holds the text. `broadcast()` refuses the event names `closed`
and `hx:release`, which end or release the stream.

```js
document.body.addEventListener("presence", (event) => {
  const { online } = JSON.parse(event.detail.data);
});
```

Without htmx, `EventSource.addEventListener("presence", ...)` receives the same event.

## Who may read a topic

`PG_SSE["CAN_SUBSCRIBE"]` names a function `(request, topic) -> bool`. The default opens
`public:` topics to everyone and `user:<pk>` to that user, and closes every other kind.
Topics starting with `_` are reserved for the package, such as the topics `close_streams()` writes to.
The view answers a request for them with a 403, before it calls `CAN_SUBSCRIBE`.
`broadcast()` raises `ValueError` for them.

```python
PG_SSE = {"CAN_SUBSCRIBE": "myproject.events.can_subscribe"}
```

```python
from django_pg_sse.permissions import can_subscribe as default


def can_subscribe(request, topic):
    kind, _, key = topic.partition(":")
    if kind == "room":
        return request.user.is_authenticated and Membership.objects.filter(room=key, user=request.user).exists()
    return default(request, topic)
```

A refused topic gets a 403 without a body. htmx does not retry it.
htmx 4 swaps error responses into the target, by default the element with `hx-sse:connect`.
The empty body clears that element, so keep it empty, as in the example above.
With `DEBUG` on, django-htmx replaces the whole page with the body of a 400, 403, 404 or 500.
A refused stream then leaves a blank page, and only the browser console shows the 403.

The check runs when a stream opens. After taking access away, call `close_streams()`:

```python
from django_pg_sse import close_streams

close_streams(user=user)  # every stream of the user
close_streams(session=request.session)  # the streams of one session
```

Each stream receives an event named `closed` and ends. htmx reconnects, and the check runs again.
Add `hx-sse:close="closed"` to a stream element that should stop instead. Logging out closes the
streams of that session, so other tabs lose the user's topics.

## Replay

Every event is stored. A reconnecting browser sends `Last-Event-ID` and receives what it missed.
Event ids are signed with `SECRET_KEY` for the user, the session and the topics of the stream.
An unsigned id, or one signed for another stream, replays nothing; the stream starts with live events.
A `close_streams()` for the owner after the id also skips the replay.
The events from the time without access then stay unread.
Run `manage.py prune_stream_events` regularly, for example hourly; it deletes events older than
`PG_SSE["RETENTION_HOURS"]` (default 24).

Some events are snapshots that replace the previous one, such as an online list.
`latest` gives them a key, and a replay skips a snapshot when a newer one has the same topic and key:

```python
broadcast("room:1", online_html, latest="online")
```

An open stream receives every snapshot as it is sent.
The hub's catch-up after a lost `LISTEN` connection is a replay and skips replaced snapshots too.
Events without `latest` are replayed in full.

htmx's `hx-sse` closes the stream of a hidden tab and reconnects when the tab is visible again.
The replay then delivers what the tab missed, in order.
A tab hidden for longer than the retention misses the events pruned meanwhile.
More than 500 missed events end the stream after one batch, and the next reconnect fetches the next batch.
`hx-config='{"sse": {"pauseOnBackground": false}}'` on the stream element keeps a hidden tab's stream open.

## Signals

`django_pg_sse.signals` sends `stream_opened` when a stream's subscription is in place.
It sends `stream_closed` when that stream ends, also after a disconnect during `stream_opened`.
A process that is killed sends no `stream_closed`.
Both signals pass `sender=StreamInfo` and a `stream` argument, a `StreamInfo` with these fields:

- `id`: a new random id for each connection
- `user_pk`: the user's primary key as a string, or `None` for an anonymous stream
- `session`: the SHA-256 digest of the session key, or `None` for an anonymous stream
- `topics`: the topics of the stream
- `request`: the request that opened the stream; read its session and user in sync code

```python
from django.dispatch import receiver
from django_pg_sse.signals import stream_opened


@receiver(stream_opened)
def count_stream(sender, stream, **kwargs):
    metrics.increment("sse.streams", tags={"user": stream.user_pk is not None})
```

The stream waits for its receivers, so keep them short.
A receiver that raises is logged to `django.dispatch`, and the stream goes on.

## Presence

The optional app `django_pg_sse.presence` tracks who has a topic open, such as the members of a chat room.
`present(topic)` lists the readers, and the `presence_changed` signal reports joins, leaves and new meta.
A reader with several tabs counts once, and a reconnect within 5 seconds changes nothing.
See [Presence](https://django-pg-sse.readthedocs.io/en/latest/presence.html).

## Database connections

The [deployment guide](https://django-pg-sse.readthedocs.io/en/latest/deployment.html) covers sizing,
timeouts, proxies and shutdown in more detail.

The hub's connections use the alias in `PG_SSE["DATABASE"]` (default `"default"`), outside Django's connection pool.
Each ASGI worker holds one for LISTEN, one for live delivery and a pool for opening streams.
`PG_SSE["STREAM_CONNECTIONS"]` (default 4) caps that pool.
A worker therefore holds up to 2 + `STREAM_CONNECTIONS` connections.

- They take its host, port, user, password and the libpq `OPTIONS`, such as `sslmode`, `service`,
  `passfile`, `application_name` and `prepare_threshold`.
- They apply `OPTIONS["assume_role"]` with `SET ROLE`.
- `pool`, `isolation_level` and `server_side_binding` do not apply. The hub runs in autocommit.
- LISTEN needs a session. A PgBouncer in transaction mode cannot carry it.
  With such a PgBouncer, give the hub an alias that reaches PostgreSQL directly.
  The alias must reach the same database as `default`, which `broadcast()` writes to.
- They add libpq defaults for `connect_timeout`, keepalives and `tcp_user_timeout`.
  [Settings](https://django-pg-sse.readthedocs.io/en/latest/settings.html#databases) lists them;
  a key in `OPTIONS` replaces its default.

Turn on Django's connection pool, `OPTIONS: {"pool": True}`, for `default` and the hub's alias.
Under ASGI, Django reuses connections only through a pool.
django-pg-sse closes the receivers' connections after each signal; without a pool, the next one connects anew.
`manage.py check --deploy` warns with `pg_sse.W002` for `default` and `pg_sse.W003` for the hub's alias.
Behind a PgBouncer in transaction mode, which pools `default` itself, silence `pg_sse.W002`.

## How it works

- `broadcast()` writes the event after the commit, in a short transaction that holds an advisory
  lock. Event ids therefore become visible in order, which keeps the replay exact.
- `NOTIFY` carries only the id and the topic, so the 8000-byte payload limit does not apply.
- The number of connections per ASGI worker does not grow with the number of open streams.
  Open streams hold no connection from Django's pool.
- A listener that loses its connection reconnects and loads the events it missed from the table.
- After 30 seconds without a NOTIFY, the listener sends `SELECT 1` and waits up to 10 seconds.
  Without an answer, it reconnects; psycopg can add up to 10 seconds while it cancels the query.
  This replaces a half-open LISTEN connection, such as after a failover, within about a minute.
- A query on the other connections gives up after `PG_SSE["QUERY_TIMEOUT"]` (default 30) seconds.
  psycopg can add up to 10 seconds while it cancels the query.
  If the server does not answer, the query runs once more on a new connection, with the same limits.
- A query on a connection that a database restart ended runs once more on a new connection.
- The view opts out of `ATOMIC_REQUESTS`, which Django does not allow for async views.
- `close_streams()` stores an event on a close topic of the user or the session.
  Only a process with a stream of that owner acts on it, and it needs no query.
- A close topic holds a SHA-256 digest of the user's primary key or the session key.

## Compared to django-eventstream

[django-eventstream](https://github.com/fanout/django-eventstream) also serves server-sent events
from Django. It shares no code or API with this package. This comparison refers to its release 5.3.4.

django-pg-sse supports PostgreSQL only and ASGI only. In return it needs no other service.

| | django-pg-sse | django-eventstream |
|---|---|---|
| Delivery across processes | PostgreSQL `LISTEN`/`NOTIFY` | Redis pub/sub or a GRIP proxy such as Pushpin; otherwise the sending process only |
| Sending | After the transaction commits; a rollback sends nothing | At once, without `on_commit` |
| Storage | Every event | Optional, per channel |
| Event ids | One sequence, in commit order across all topics | One counter per channel |
| `Last-Event-ID` | Signed for the user, the session and the topics | Chosen by the client |
| Stream lifecycle | `stream_opened` and `stream_closed` signals | None |
| Revoking access | `close_streams()` for a user or a session, in every process | `channel_permission_changed()` for a user and a channel, in the calling process and at a GRIP proxy |
| Payload | HTML for htmx, JSON for client code, or any text | JSON by default, or any text |
| Servers | ASGI | ASGI, or WSGI behind a GRIP proxy |

django-eventstream with Pushpin or Fanout holds the open connections outside Django.
That scales to more concurrent connections than an ASGI worker holds.
Without such a proxy, both packages hold each open stream in an ASGI worker.

django-pg-sse serialises `broadcast()` through an advisory lock, so the events per second have a
lower ceiling than with Redis.

## License

MIT
