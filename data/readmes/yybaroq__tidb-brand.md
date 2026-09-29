# tidb-brand — a Claude skill

A self-contained Claude skill that gives Claude (Code, Cowork, Agent SDK, claude.ai) the TiDB / PingCAP brand system: colors, typography, logo rules, the Cornerstone graphic system, and a curated library of ready-to-use SVG assets.

When this skill is installed, Claude automatically reads it before producing any TiDB-branded content — slides, docs, social posts, web artifacts, banner ads, etc. — so the output stays on-brand without you spelling out the rules each time.

## What's in here

```
tidb-brand/
├── SKILL.md                ← the skill manifest Claude reads
├── preview.html            ← visual index of every asset (open in a browser)
├── README.md               ← this file
├── assets/
│   ├── logos/              6 brand-approved logo lockups (PNG)
│   ├── cornerstones/       single solid 3D cubes, every brand hue, two orientations
│   ├── cornerstones-grid/  cube + dashed isometric scaffold (scalability visuals)
│   ├── matrices/           multi-cube cornerstone matrices for hero moments
│   ├── lattices/           dark + red hero towers / stacks
│   ├── scaffolds/          outline grids and large isometric backdrops
│   ├── banners/            pre-composed banner backgrounds
│   ├── cta-blocks/         1440 × 574 CTA backgrounds in every brand color
│   ├── textures/           diagonal stripe patterns
│   └── overview/           full brand-sheet poster + raster exports + photo
└── references/
    ├── colors.md           full color spec with print equivalents
    ├── cornerstone.md      deep dive on Cornerstone construction
    ├── layouts.md          composition templates
    ├── logo-usage.md       logo do/don't gallery
    └── typography.md       type system details
```

74 visual assets in total.

## Install

### As a Claude Code / Cowork skill

Drop the `tidb-brand/` folder into your skills directory:

- **macOS / Linux:** `~/.claude/skills/tidb-brand/`
- **Cowork plugin (per-org):** include it under your plugin's `skills/` folder.

Claude auto-discovers any folder containing a `SKILL.md` and treats its YAML frontmatter as the trigger description.

### As a standalone reference

You don't need Claude to use this — open `preview.html` in any browser and you get a clickable thumbnail index of every asset.

## Usage

Once installed, just talk to Claude normally:

> "Make a 1080×1080 LinkedIn post announcing TiDB Cloud's new region. Use the violet Cornerstone."

Claude will read `SKILL.md`, pick `assets/cornerstones/cornerstone-violet-A.svg` (or a matrix variant), apply the right colors and typography, and produce on-brand output.

## License / attribution

Brand assets © PingCAP. Distribute internally or to TiDB partners; do not redistribute publicly without permission.

## Maintenance

To add or update assets:
1. Drop the new file into the matching `assets/<category>/` folder.
2. Add a row to the relevant table in `SKILL.md` so Claude can find it.
3. Add the file to `preview.html` (the `groups` object near the bottom of `<script>`).
