# Apps built for Tidbyt Pixel Display

Programming language: [Starlark](https://github.com/google/starlark-go/)  
Building apps using Pixlet: [Instructions](https://github.com/tidbyt/pixlet)

## Apps

### Hello World

#### Canonical 'Hello World' example, spruced up with animation

- Displays centered text
- Include animation on 3 frames of pixelart

### Latte

#### Simple app that displays an animation 

- Displays centered animation 

### Stoic Quote

#### Displays a random quote for the day

- Includes random number generator (seeded with time of day)
- Accesses random element in list of strings to display


## Useful commands / tools during development

#### Pushing and testing a program locally:  
`cat example.star |   pixlet serve /dev/stdin`

#### Creating Pixel Art
https://www.pixilart.com/draw 

#### Converting image to base64
https://base64.guru/converter/encode/image
