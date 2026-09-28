# Open Tractor Data

An open dataset of tractor brands, models, shows, and museums — freely available for developers, researchers, and agriculture enthusiasts.

**Browse the full interactive database:** [tractordata.site](https://tractordata.site)

---

## What's Inside

| Dataset | Records | Format |
|---------|---------|--------|
| [Tractor Brands](data/brands.json) | 334 brands | JSON, CSV |
| [Tractor Shows](data/shows.json) | 13 events | JSON |
| [Tractor Museums](data/museums.json) | 14 museums | JSON |
| [Brand Pages](brands/) | 334 files | Markdown |
| [Shows by State](shows/) | 16 states/regions | Markdown |

## Data Structure

### `data/brands.json`
```json
{
  "tractor_brand": "John Deere",
  "brand_key": "john_deere",
  "tractor_type": "farm",
  "tractor_count": "1011",
  "power_range": "10-631 hp",
  "years_range": "1918-2025",
  "brand_website": "https://www.deere.com",
  "tractordata_url": "https://tractordata.site/en/brands/john_deere"
}
```

### `data/brands.csv`
Same data in CSV format — ready for Excel, pandas, R, etc. Includes `tractordata_url` column linking to full specs.

### `brands/farm/` and `brands/lawn/`
One Markdown file per brand with overview and a link to full model specs on [tractordata.site](https://tractordata.site).

### `shows/`
Tractor shows and museums organized by US state / region.

## Quick Start

```python
import json

brands = json.load(open('data/brands.json'))
farm_brands = [b for b in brands if b['tractor_type'] == 'farm']
print(f"{len(farm_brands)} farm tractor brands")
```

```python
import pandas as pd

df = pd.read_csv('data/brands.csv')
print(df.groupby('type')['model_count'].sum())
```

## Full Specifications & Model Data

This repository contains summary-level data. For complete model specifications (engine, dimensions, hydraulics, transmission), visit:

**[tractordata.site](https://tractordata.site)** — 16,000+ tractor models with full specs

## License

Licensed under [CC BY 4.0](LICENSE). Free to use and adapt for any purpose, including commercial, with attribution:

> Source: [TractorData.site](https://tractordata.site) — The Open Tractor Database

## Contributing

Found missing data or an error? Open an issue or submit a PR.
