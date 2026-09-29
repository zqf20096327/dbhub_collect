
## tidbits.nix

Nix and NixOS in the beginning can be
- a little hard to wrap one's head around
- there are a few missing tidbits out of the box 

Here I collect a few tidbits to nibble on.

---

Start with [examples/nixos-iso](./examples/nixos-iso/) to see how you can configure a flake based configuration.

To use this with your flake, add:

`inputs.tidbits.url = "github:wav/tidbits.nix/main"`

Then import the module 

`inputs.tidbits.nixosModules.default`

---

Here are a few little good to knows to have a play with in this repository:

`❯ nix eval .#assertions`

`❯ nix build .#snapdrop`

`❯ nix repl .`

```shell
Welcome to Nix 2.18.1. Type :? for help.

Loading installable 'git+file:///home/.../src/github.com/wav/tidbits.nix#'...
Added N variables.
nix-repl> nixosConfigurations.nixos-iso.config.tidbits.display-scaling.cursor-size
24
     
```

`❯ nix build .#nixosConfigurations.nixos-iso.config.system.build.toplevel`

`❯ nix build .#nixosConfigurations.nixos-iso.config.system.build.isoImage`