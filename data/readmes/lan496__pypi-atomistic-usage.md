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

## Using the figures

Every figure has a Share button that gives a link to that figure alone
(`#panel=<name>`, keeping the filters in use; add `&theme=light` for light
colours) and an `<iframe>` code to embed it in another web page. A "Latest"
link follows the monthly refresh; a "Fixed" link (`#snapshot=<date>`) keeps the
data of one refresh for a year, from the copies in `docs/snapshots/`; older
copies are deleted at each refresh and their links show the latest data. Figures
also download as PNG, SVG and CSV.

For example, "The field over time" alone, as a PNG of the 2026-11-20 data that
links to the live figure:

[![The field over time: PyPI downloads per day of each category of atomistic Python packages since 2016](docs/field-over-time.png)](https://lan496.github.io/pypi-atomistic-usage/#panel=era)

and embedded in a web page (GitHub does not render iframes, hence the image
above):

```html
<iframe src="https://lan496.github.io/pypi-atomistic-usage/#panel=era&theme=light"
        title="The field over time" width="100%" height="520" style="border: 0" loading="lazy"></iframe>
```

## License

The figures and the compiled data (`docs/data.js` and what the dashboard
draws from it) are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse them freely,
also commercially, with credit to "Atomistic PyPI usage" and a link to the
dashboard. They aggregate
[PyPI's download statistics](https://docs.pypi.org/api/bigquery/), themselves
CC BY 4.0.

The code is MIT; see [LICENSE](LICENSE).
