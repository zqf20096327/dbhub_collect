# Tidbyt Apps

Use [pixlet](https://github.com/tidbyt/pixlet) to build apps for [Tidbyt](https://tidbyt.com/) using [Starlark](https://github.com/bazelbuild/starlark).


## Getting started

* Install the [VSCode `vscode-starlark` extension](https://marketplace.visualstudio.com/items?itemName=phgn.vscode-starlark).
* Install the [iOS app](https://tidbyt.com/app).


### Reference

* https://github.com/tidbyt/pixlet/blob/main/docs/
* https://github.com/bazelbuild/starlark


## Development

The `pixlet` executable is included in the project, so you can develop with:

```bash
$ bin/pixlet serve --watch src/example.star
```

Then visit http://localhost:8080/


### `fuzzy_clock_data.star`

This Starlark file for a clock is generated from `fuzzy_clock_data.star.erb` by running:

```bash
ruby bin/fuzzy_clock_data.rb
```

It interpolates the `DATA` dict in the file so that it can use Ruby to fetch and format data in ways that Starlark cannot. It also uses a local file cache with a TTL for each value to prevent hitting APIs too often.


## Buliding Pixlet for Raspberry Pi

Assuming `go` and `npm` are installed:

```bash
cd ~/pixlet
npm install && npm run build && PATH=$PATH:/usr/local/go/bin GOPATH=$HOME/golang make build
cp pixlet ~/tidbyt-apps/bin/pixlet_linux_arm32
```

https://github.com/drudge/homebridge-tidbyt/wiki#how-do-you-install-pixlet-on-the-raspberry-pi
https://github.com/tidbyt/pixlet/issues/700


## Pushing to Tidbyt

Include a `.env` file in the root of the project that includes:

```bash
TIDBYT_DEVICE_ID=the-device-id
TIDBYT_TOKEN=1lkjdf09jasdlfkj23094lslkdfj0.9234nf
```

Those values can be found in the Tidbyt mobile app.

Then to push to the device:

```bash
$ bin/push src/example.star
```
