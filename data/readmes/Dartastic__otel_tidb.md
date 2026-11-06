# otel_tidb

Dartastic OpenTelemetry bridge for TiDB (distributed HTAP SQL).

Wraps each call in a CLIENT-kind span with vendor-specific attributes following OpenTelemetry semantic conventions where applicable.

```dart
import 'package:otel_tidb/otel_tidb.dart';

await tracedTidb<void>(
  operation: 'someOp',
  invoke: () async {
    final r = await client.someOp();
    return TidbCallResult(value: r, result: TidbResult(statusCode: 200));
  },
);
```

Suppress instrumentation within a block:

```dart
await runWithoutTidbInstrumentationAsync(() async {
  await client.someInternalSync();
});
```
