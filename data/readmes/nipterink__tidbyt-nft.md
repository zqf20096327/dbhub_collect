# tidbyt-nft
Ethereum and NFT Widgets for the Tidbyt

These widgets are built on top of the [Pixlet SDK](https://github.com/tidbyt/pixlet/) using Starlark scripts to display Ethereum and NFT data (from OpenSea) on the [Tidbyt](https://tidbyt.com/). Instructions for how to run locally and deploy to the Tidbyt can be found on the [Pixlet Readme](https://github.com/tidbyt/pixlet/#readme).

### [EthGasTracker](EthGasTracker.star)
Ethereum Price and Gas data is powered by https://etherchain.org/ to display the current price in USD and the cost of gas in GWei
![gastracker](https://user-images.githubusercontent.com/55990898/152473621-e280eb23-d340-4714-990f-0dacdbed07bf.png)

### [OSCollectionStats](OSCollectionStats.star)
OpenSea Collection data is powered by their [API](https://docs.opensea.io/reference/api-overview) to show a the image and current floor price of a random collection from a predefined list.
![collection](https://user-images.githubusercontent.com/55990898/152473909-9252c21c-8f6e-4f36-a1f3-ebbdd0ef829b.png)
