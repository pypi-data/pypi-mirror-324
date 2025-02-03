from argparse import ArgumentParser
from .log import info, success, error, warning, yesno, banner
from .exec import nix_exec
from .settings import get_option

def _prepare_rebuild():
    dotfiles = get_option("dotfiles")
    # check that no changes have been made
    diff: str = nix_exec(f"cd {dotfiles}; git status --porcelain", capture=True, packages=["git"])
    if diff.strip():
        # if changes have been made, ask wether to add and commit them
        warning("Changes have been made to the configuration. Commit them before rebuilding.")
        if yesno("Add and commit changes?"):
            nix_exec(f"cd {dotfiles}; git add .", packages=["git"])
            commit_message = nix_exec(f"cd {dotfiles}; nixos-rebuild list-generations | grep current", capture=True)
            info(f"Committing changes with message: {commit_message}")
            nix_exec(f"cd {dotfiles}; git commit -m '{commit_message}'", packages=["git"])
            success("Changes committed.")
        else:
            return

def rebuild():
    banner()
    dotfiles = get_option("dotfiles")
    info("Rebuilding NixOS configuration...")
    _prepare_rebuild()
    # rebuild the configuration
    rebuild_cmd = f"cd {dotfiles}; sudo /usr/bin/env bash -p -c 'nixos-rebuild switch --flake .# --log-format internal-json -v |& nom --json'"
    rebuild_packages = ["nix-output-monitor"]
    info("Rebuilding configuration...")
    nix_exec(rebuild_cmd, packages=rebuild_packages)
    success("Configuration rebuilt.")

def cleanup():
    banner()
    info("Cleaning up NixOS store... (deleting older than 3d)")
    nix_exec("sudo /usr/bin/env bash -p -c 'nix-collect-garbage --delete-older-than 3d --log-format internal-json -v |& nom --json'")
    success("NixOS store cleaned up.")

def update():
    banner()
    dotfiles = get_option("dotfiles")
    info("Updating NixOS...")
    nix_exec(f"cd {dotfiles}; sudo /usr/bin/env bash -p -c 'nix flake update --flake .# --log-format internal-json -v |& nom --json'")
    success("NixOS updated.")
