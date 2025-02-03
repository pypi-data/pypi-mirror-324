# nixos-wizard

## Installation


```bash
python3 -m pip install nixos-wizard

# create config file
mkdir -p ~/.config/nixos-wizard
# filepath to your nix config
echo "dotfiles: ~/dotnix" > ~/.config/nixos-wizard/config.yaml
```

## Usage


```bash
nixos-wizard-rebuild    # rebuilds nix config (+ switch)
nixos-wizard-cleanup    # clean up nix store
nixos-wizard-update     # update nixpkgs
```

