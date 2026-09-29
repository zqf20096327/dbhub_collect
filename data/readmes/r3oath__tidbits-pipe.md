# Pipe
A tiny collection of JS functions to facilitate piping, composition and basic currying.

## Install
Using you favourite package manager:

`yarn add @tidbits/pipe`

or

`npm i @tidbits/pipe`

## Usage

Via import's
`import { compose, pipe, args } from '@tidbits/pipe';`

Via require
`const { compose, pipe, args } = require('@tidbits/pipe');`

## Functions
### `pipe(initialValue, fns)`
- *initialValue* (any): The initial value passed to the first function in the pipeline.
- *fns* (Array): An array of functions to chain together.

Returns the result of initialValue being passed down the chain of provided functions.

### `compose(fns)`
- *fns* (Array): An array of functions to chain together.

Returns a new function with 1 parameter, which can be called anywhere.

### `args(fn, ...)`
- *fn* (Function): A function to curry.
- *...* (Any): Any number of additional arguments to supply to *fn* after the first argument when called.

Returns a new function expecting 1 parameter, which can be called anywhere.

## Examples
### Pipe
```js
import { pipe } from '@tidbits/pipe';

const uppercase = str => str.toUpperCase();
const exclaim = str => `${str}!`;

pipe('functional', [
  uppercase,
  exclaim,
  console.log,
]);

// FUNCTIONAL!
```

### Composition
```js
import { compose } from '@tidbits/pipe';

const uppercase = str => str.toUpperCase();
const exclaim = str => `${str}!`;

const shout = compose([
  uppercase,
  exclaim,
]);

console.log(shout('functional'));

// FUNCTIONAL!
```

### Additional Arguments
```js
import { compose, pipe, args } from '@tidbits/pipe';

const uppercase = str => str.toUpperCase();
const exclaim = str => `${str}!`;
const repeat = (str, times = 1) => str.repeat(times);

const shout = compose([
  uppercase,
  exclaim,
]);

pipe('functional', [
  shout,
  args(repeat, 3),
  console.log,
]);

// FUNCTIONAL!FUNCTIONAL!FUNCTIONAL!
```
