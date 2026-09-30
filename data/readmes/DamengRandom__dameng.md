# Dameng

A scroll-driven, cinematic CV/portfolio site for an AI agent engineer, rendered live in Three.js.
A fixed WebGL canvas driven by scroll, layered with generated cinematic stills and alpha-cutout
foreground art, built around an original "Deploy" theme: a night orchestration space of grid
terrain, node clusters, and light pulses.

See [`PROMPT.md`](PROMPT.md) for the full build brief.

## Run locally

There is no build step. From the repository root, run:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Then visit [http://127.0.0.1:4173/](http://127.0.0.1:4173/).

Any static file server works — Python is just the most likely to already be installed. For example:

```bash
npx serve .
```

## Project structure

```text
dameng/
├── index.html              # structure, CSS, scene code, and scroll choreography — single file
├── PROMPT.md               # build brief / reusable technique prompt for this site
├── vendor/
│   └── three.module.js     # vendored Three.js r169 (MIT), no npm install needed
├── assets/
│   ├── favicon.svg         # nav/favicon logomark
│   ├── generated/          # Leonardo-generated background plates (4)
│   └── foreground/         # Leonardo-generated alpha-cutout foreground props (6)
├── scripts/
│   └── cutout.py           # turns a subject-on-black render into an alpha-cutout webp
└── docs/superpowers/specs/ # design spec for the site
```

## Status

Design spec and first working pass are done — live scroll-driven scene, all 6 chapters, and
8 of 10 Leonardo shots generated and wired in. Remaining: 2 foreground props
(`circuit-fragment.webp`, `code-glyphs.webp`), a mobile nav menu, a real 390×844 responsive pass,
and swapping in real CV content in place of the placeholder copy.
