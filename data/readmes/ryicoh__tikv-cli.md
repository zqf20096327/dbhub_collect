# tikv-cli

## Usage

### Set

```bash
tikv-cli --pd-endpoints=http://127.0.0.1:2379 set dog/1 saluki
tikv-cli --pd-endpoints=http://127.0.0.1:2379 set dog/2 borzoi
```

### Get

```bash
tikv-cli --pd-endpoints=http://127.0.0.1:2379 get '' ''
key:  dog/1
value:  saluki
key:  dog/2
value:  borzoi
len:  2
```

### Delete

```bash
tikv-cli --pd-endpoints=http://127.0.0.1:2379 del dog/1
```
