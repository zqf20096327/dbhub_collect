# Tidbits
Random compilation of web tips

# Javascript
## Promises
Can only **await** in For of/ For in/ For/ While loops but not higher order array functions/ loops that use a callback  
  * Array.map will return an array of pending promises in this situation.  
  * Will require a Promise.all(promisesArray) to resolve all the promises.  

# CSS

  * CSS animations are not automatically GPU accelerated (defaults to browsers rendering     engine) - Using transform : translateZ(0) or translate3d will force GPU accelaration
  * Radial gradients can be used to prevent the sharp color changes (element|border)
