# random-tidbit

A tiny browser renderer for shuffled bits of text without repeats.

Give it quotes, facts, jokes, reminders, or any other tidbits.

It displays a different tidbit on each reload or navigation. Each tidbit is shown once before reshuffling and the sequence persists across page reloads and navigation (when `localStorage` is available). Without `localStorage`, the renderer still works, but tidbits may repeat.

You can bring your own tidbits or start with the included collection of quotes.

- Works with any short text content
- Includes public domain quotes as a ready-to-use example
- Persistent, non-repeating shuffle when `localStorage` is available
- Minimal built-in styles
- Zero dependencies

## Installation

```sh
npm install random-tidbit
```

## Usage

```html
<div id="tidbit"></div>
```

```ts
import { renderRandomTidbit } from "random-tidbit";

renderRandomTidbit({
  target: "#tidbit",
  tidbits: [
    { text: 'The Big Bang occurred about 13.8 billion years ago' },
    { text: 'Planet Earth formed about 4.54 billion years ago' },
    { text: 'Homo sapiens appeared on Earth about 300,000 years ago' },
    { text: 'A sock disappeared in the washing machine sometime last Tuesday' }
  ]
});
```

## Quote collection

Quotes are included as one example of tidbits:

```ts
import { quotes } from "random-tidbit/quotes";
import { renderRandomTidbit } from "random-tidbit";

renderRandomTidbit({
  target: "#tidbit",
  tidbits: quotes
});
```

Each quote uses the same generic tidbit shape:

```ts
{
  text: "I dwell in possibility",
  attribution: "Emily Dickinson"
}
```

## Usage in Astro

This package works well with static site generators such as Astro: the page remains static while a small client-side script displays a different tidbit on each navigation or reload.

```astro
<div id="tidbit"></div>

<script>
  import { renderRandomTidbit } from "random-tidbit";
  import tidbits from "../assets/data/tidbits.json";

  renderRandomTidbit({
    target: "#tidbit",
    tidbits
  });
</script>
```

## API

### `renderRandomTidbit(options)`

Renders the next tidbit in the shuffled sequence.

| Option             | Type                    | Default  | Description                                       |
| ------------------ | ----------------------- | -------- | ------------------------------------------------- |
| `target`           | `string \| HTMLElement` | required | CSS selector or element that receives the tidbit. |
| `tidbits`          | `Tidbit[]`              | required | Tidbits to shuffle and render.                    |
| `useDefaultStyles` | `boolean`               | `true`   | Whether to inject the built-in stylesheet.        |

Returns the current tidbit and two controls:

```ts
{
  tidbit: Tidbit;
  renderNext: () => Tidbit;
  destroy: () => void;
}
```

- `renderNext()` renders and returns the next tidbit.
- `destroy()` clears the target.

### `Tidbit`

```ts
import type { Tidbit } from "random-tidbit";

type Tidbit = {
  text: string;
  attribution?: string;
};
```

Text and attribution values are trimmed. Entries without text are ignored. The renderer throws if no valid tidbits remain.

### `quotes`

An exported `Tidbit[]` containing the example quote collection. Pass it explicitly as `tidbits` when you want to use it.

## Persistence

When available, `localStorage` stores only sequence indexes.

Each distinct normalized tidbit list receives its own storage key, so different lists do not interfere with one another. Across reshuffles, at least half the collection, rounded down, is rendered between appearances of the same tidbit. If `localStorage` is unavailable or inaccessible, rendering continues without persistence and tidbits may repeat.

## Styling

Tidbits render as neutral `<p>` elements. Attributions render as `<span>` elements. Disable the built-in styles when using your own CSS:

```ts
renderRandomTidbit({
  target: "#tidbit",
  tidbits,
  useDefaultStyles: false
});
```

Generated classes:

```txt
random-tidbit
random-tidbit__text
random-tidbit__attribution
```

### Preventing layout shifts

Reserve space for the target in CSS that loads with your page:

```css
#tidbit {
  min-block-size: 3lh;
}

@media (max-width: 40rem) {
  #tidbit {
    min-block-size: 5lh;
  }
}
```

## Browser support

This package is ESM-only and requires a browser environment. `localStorage` is recommended for persistent, non-repeating sequences but is not required.

## License

[MIT](./LICENSE)
