# @johnpc Tidbyt app

This is an app for [Tidbyt](https://tidbyt.com/) for my personal use.

## Setting up

First, install `pixlet`.

On Mac

```bash
brew install tidbyt/tidbyt/pixlet
```

On Linux

```bash
# Download the archive.
curl -LO https://github.com/tidbyt/pixlet/releases/download/v0.22.4/pixlet_0.22.4_linux_amd64.tar.gz

# Unpack the archive.
tar -xvf pixlet_0.22.4_linux_amd64.tar.gz

# Ensure the binary is executable.
chmod +x ./pixlet

# Move the binary into your path.
sudo mv pixlet /usr/local/bin/pixlet
```

Then, connect to your Tidbyt:

```bash
# login to your Tidbyt account
pixlet login

# get your Tidbyt device id
export DEVICE_ID=$(pixlet devices | cut -d ' ' -f1)
```

## Building the app (.webp)

```bash
pixlet render hello_world.star
export DEVICE_ID=$(pixlet devices | cut -d ' ' -f1)
pixlet push $DEVICE_ID hello_world.webp
```

## Building for [Inklink](https://getinklink.net)

Inklink is another project I've worked on to show information of interest at a glance. See https://github.com/johnpc/ink-link

You can view your Inklink widget on Tidbyt using:

```bash
export INKLINK_DEVICE_CODE={YOUR_DEVICE_CODE_HERE}
sh ./inklink.sh
```
