# Tidbyt - ACiD Packs

This repo installs 4 random pieces of ACiD BBS ANSI art (of 99) onto your Tidbyt. These scroll
veritically and run for 15 seconds.

This work was sourced from http://artscene.textfiles.com/acid/ARTPACKS/ between 1992 and 1996.

# Setup

OSX:
```
brew install
```

Linux: visit [pixlet releases](https://github.com/tidbyt/pixlet/releases) and grab the latest for
your platform:
```
pushd /tmp
wget https://github.com/tidbyt/pixlet/releases/download/v0.25.1/pixlet_0.25.1_linux_amd64.tar.gz
tar zxvf pixlet_0.25.1_linux_amd64.tar.gz
sudo mv pixlet /usr/local/bin/
popd
```

If you have a browser installed you can run
```
pixlet login
```
for auth. If this is a headless server, just grab your API token via the App in Settings -> General
-> Get API key.

# Usage

It's recommend you cron this roughly every 5 or 10 minutes. I've had a number of issue with the Tidbyt
crashing when images were pushed too frequently.

```
./push-gifs <device id> [api token]
```

The api token is only required if you couldn't run pixlet login.

You can gather both of these from the App in Settings -> General -> Get API Key. The API key is
brutally long. I'm sorry.

## Cron Example

```
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
*/10 * * * * /home/mkent/tidbyt-acid/push-gifs amicably-natty-cat-centipede-149 <giant token> >>/home/mkent/tidbyt-acid/push.log 2>&1
```
