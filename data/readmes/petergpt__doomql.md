# DOOMQL

### `SELECT * FROM HELL`

**A playable first-person shooter whose framebuffer is a SQL query.**

DOOMQL started with a deliberately unreasonable question: what if SQLite were
the game engine, not merely the place where a game stores data?

The result is a small, original Doom-like game in which SQL owns movement,
collision, enemies, combat, progression and every RGB pixel on screen. There is
no SVG, browser, Canvas or game engine, and the playable runtime contains no
Python graphics code.

![DOOMQL running in a real terminal](docs/images/gameplay-terminal.png)

## How does SQL become a picture?

For each frame, SQL reads the player and map tables and produces one row per
pixel:

```text
x    y    red    green    blue
40   20   232    240      248
41   20    30     35       45
```

A second SQL view turns those RGB rows into coloured `▀` terminal blocks. The
Python host does no drawing: it supplies raw keys, time and terminal size to
SQLite, then prints the completed query result unchanged.

```text
player + map tables
        ↓
SQL simulation and raycasting
        ↓
frame_pixels(x, y, r, g, b)
        ↓
render_frame(y, coloured scanline)
        ↓
terminal
```

The complete visible frame is returned by one query:

```sql
SELECT scanline FROM render_frame ORDER BY y;
```

## Play

You need:

- macOS, Linux or another Unix-like environment; Windows users can use WSL
- Python 3.11 or newer
- SQLite 3.45 or newer with mathematical functions enabled
- A terminal with 24-bit colour and Unicode `▀` support
- At least 80 columns × 33 rows recommended

There are no third-party Python dependencies. From the repository root, run:

```bash
make run
```

The game follows the live terminal size. Enlarge the window for more
SQL-rendered pixels, or increase the terminal font size to make each pixel
physically larger.

### Controls

| Keys | Action |
|---|---|
| `W` / `S` | Move forward / backward |
| `A` / `D` | Strafe left / right |
| `J` / `L` or arrow keys | Turn left / right |
| Space | Fire |
| `E` | Use the index gate |
| `P` | Pause |
| `R` | Restart after death or victory |
| `Ctrl-C` | Exit |

### Objective

1. Find the cyan-and-gold **INDEX TOKEN**.
2. Return to the amber gate and press `E`.
3. Defeat the red **DEADLOCK**.
4. Reach the cyan commit portal.

Along the way you will meet ORPHAN enemies, ranged LOCK WAITERS, health tuples
and ammo pages.

## Watch the real SQL while you play

This is the best way to demonstrate the project. Open two terminals in the
repository root.

In the first terminal, start the game:

```bash
make run
```

In the second terminal, start the read-only SQL audit:

```bash
make inspect
```

![DOOMQL game beside its live SQL audit](docs/images/game-and-sql-audit.png)

The left terminal is the game. The right terminal reads the same live database
and shows:

- The tick and resolution of the frame actually displayed
- `SAME COMMIT=YES` when the game state and displayed frame match
- The exact render query that completed
- Real before/after values for movement, firing, damage and state changes
- The exact responsible SQL from the source the game executed

This is not a replay, a second simulation or an animated approximation. The
inspector opens SQLite with `PRAGMA query_only=ON`; it cannot change the game.
There is no pretend instruction pointer or moving highlight. Audit events are
written inside the same transaction as the gameplay change and roll back with
it.

Use `j` / `k` or Space / `b` to scroll the SQL and `q` to exit the inspector.

## What is really implemented in SQL?

| SQL owns | Python only transports |
|---|---|
| Key bindings and input interpretation | Raw terminal key bytes |
| Player movement and collision | A monotonic timestamp |
| Enemy AI, combat and progression | Terminal columns and rows |
| Doors, pickups, death and victory | Fixed SQL execution requests |
| DDA raycasting and wall projection | Completed SQL scanlines to stdout |
| Sprite scaling, depth and occlusion | Terminal mode setup and restoration |
| Weapon, crosshair, effects and HUD | Nothing game-specific |
| Every final RGB value and ANSI colour code | |

The host deliberately contains no key map, coordinates, game constants,
colours, rendering calculations or game-state decisions. Tests enforce this
boundary.

## Project layout

```text
doomql/
├── sql/          game state, simulation, AI and renderer
├── host/         minimal SQLite and terminal transport
├── tools/        live audit, source browser and preview utilities
├── tests/        gameplay, rendering, determinism and purity tests
├── docs/         technical specification and images
├── .github/      CI and contributor-facing files
├── Makefile
├── LICENSE
└── README.md
```

The two most important files are:

- [`sql/tick.sql`](sql/tick.sql): input, movement, AI, combat and progression
- [`sql/003_render.sql`](sql/003_render.sql): raycasting, pixels and ANSI output

For the full design and purity contract, read
[`docs/SPEC.md`](docs/SPEC.md).

## Useful commands

| Command | Purpose |
|---|---|
| `make run` | Play using the persistent `.doomql/doomql.sqlite` database |
| `make inspect` | Show the live transactional SQL audit |
| `make reset` | Reset the game and print its first frame |
| `make demo` | Print one SQL-generated frame |
| `make benchmark` | Measure SQL tick and render performance |
| `make verify` | Run all tests and command-line smoke checks |
| `make clean-db` | Delete only the generated local game database |

Optional deeper diagnostics are available through `make inspect-source` and
`make inspect-overview`.

## Verification

```bash
make verify
```

The 36-test suite checks gameplay, collision, progression, deterministic replay,
frame dimensions, RGB ranges, ANSI decoding, read-only inspection, transaction
rollback, exact runtime-source identity and the absence of game logic from the
Python host. It also includes a strict local renderer-latency gate.

GitHub Actions runs the hardware-independent checks on macOS and Linux with
supported Python versions. The wall-clock latency assertion stays local because
shared virtual-runner timing is not a meaningful performance baseline.

## Scope and trust

- DOOMQL is an original Doom-like raycaster, not a Doom port. It contains no
  Doom code, WAD data, maps, art, audio or logos, and is not affiliated with or
  endorsed by id Software or its publishers.
- The terminal performs the final physical drawing. SQL calculates every RGB
  value and emits every terminal colour instruction; Python writes those bytes
  unchanged.
- Treat custom databases as trusted input. A modified database can replace the
  stored runtime SQL and inject terminal text, so do not open untrusted files
  with `--db`.
- Floating-point trigonometry can differ slightly across SQLite and math-library
  builds, so deterministic replay is promised only within the same environment.

## Contributing, security and licence

Contributions are welcome when they preserve the SQL-owned simulation and
rendering boundary. Read the [contribution guide](.github/CONTRIBUTING.md) and
[security policy](.github/SECURITY.md) before opening a pull request or report.

DOOMQL is released under the [MIT License](LICENSE).
