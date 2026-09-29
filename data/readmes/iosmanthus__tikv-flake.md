# Nix Flake for TiKV

TiKV project has plenty of build methods including Dockerfile, Makefile, ... which will increase the maintenance cost of maintainers. So I create this repository to wrap the TiKV project with nix flake. If you want to load the shell derivation while `cd` to this repository, check [nix-direnv](https://github.com/nix-community/nix-direnv).

## Usage
```sh
nix develop
cd tikv
# Happy coding
```