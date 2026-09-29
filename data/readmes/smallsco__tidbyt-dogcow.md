# tidbyt-dogcow
Clarus the Dogcow for your Tidbyt!

### Requirements
 - A [Tidbyt](https://tidbyt.com/)!
 - A copy of [Pixlet](https://tidbyt.dev/docs/build/installing-pixlet)

### What does it look like?
![tidbyt-dogcow](https://github.com/smallsco/tidbyt-dogcow/assets/1906551/894fa81f-1f87-4b2c-8e2a-3daaa801145f)



### Try it in your browser
```
pixlet serve dogcow/dogcow.star
```

### Install to your Tidbyt
Replace `[your-tidbyt-id]` in the command below with the internal ID of your Tidbyt. You can get this ID by running `pixlet devices`.

```
pixlet render dogcow/dogcow.star
pixlet push [your-tidbyt-id] dogcow/dogcow.webp -i dogcow
rm dogcow/dogcow.webp
```
