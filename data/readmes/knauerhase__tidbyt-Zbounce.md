# Zbounce

A pixel-art cat face (named for Zora) bouncing around a [Tidbyt](https://tidbyt.com) 64x32 display like an old
screensaver. Written in Starlark for Pixlet.

She takes a winding route from wall to wall at a different angle each time (ten legs, about 17 s at normal speed) and the loop is seamless. The cat is a 21x14 sprite defined as rows of
text (`CAT`) in `zbounce.star`, with its colors in `CAT_COLORS`.

## Run it

    pixlet serve zbounce.star                  # preview at http://localhost:8080
    pixlet render zbounce.star -o zbounce.webp
    pixlet push --background --installation-id Zbounce <device-id> zbounce.webp

## Options

| key | values | default |
|-----|--------|---------|
| `speed` | `slow`, `normal`, `fast` | `normal` |
