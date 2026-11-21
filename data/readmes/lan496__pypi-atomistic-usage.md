# Atomistic PyPI usage

How much are the Python packages of atomistic simulation and atomistic machine
learning used? This dashboard shows the PyPI downloads of about 200 of them:

- a curated list of structure, symmetry, phonon, workflow and
  machine-learning-potential packages,
- every PyPI package of
  [best-of-atomistic-machine-learning](https://github.com/JuDFTteam/best-of-atomistic-machine-learning),
- the simulation engines of [atomistic.software](https://atomistic.software)
  that install from PyPI,
- the most-downloaded packages that depend on any of the above.

**Dashboard: <https://lan496.github.io/pypi-atomistic-usage/>**

It shows daily downloads over the last 180 days and monthly downloads back to
2016, by platform, as a line chart, a bar chart race and a sortable table. The
table also estimates how much of each package's downloads come from CI runs and
from bulk rebuilds of one pinned environment, since download counts measure
installs, not people.

## How it works

`fetch_stats.py` queries [ClickPy](https://clickpy.clickhouse.com), ClickHouse's
public copy of the PyPI download logs and metadata, and PyPI's JSON API, and
writes `docs/data.js`. `docs/index.html` reads it and draws everything in the
browser; it opens straight from disk. A GitHub Actions job refreshes the data
on the 2nd of every month and publishes `docs/` to GitHub Pages.

## Contributing

Missing a package? See [CONTRIBUTING.md](CONTRIBUTING.md); adding one is a
one-line change.

## Credits

The project is inspired by [atomistic.software](https://atomistic.software),
which tracks the citations of atomistic simulation engines. The queries follow
the materialized views of [ClickPy](https://github.com/ClickHouse/clickpy)
(Apache-2.0).

## License

MIT; see [LICENSE](LICENSE).
