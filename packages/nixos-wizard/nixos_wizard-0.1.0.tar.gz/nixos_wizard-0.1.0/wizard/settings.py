from pathlib import Path
import yaml

HOME_DIR = Path.home()
CONFIG_DIR = HOME_DIR / ".config/" / "nixos-wizard"
CONFIG_PATH = CONFIG_DIR / "config.yaml"

# default settings
DEFAULTS = {
    "dotfiles": HOME_DIR / "dotfiles",
}

def _load_config(config_path: Path) -> dict:
    """
    Load the configuration file.
    """
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
        for key, value in DEFAULTS.items():
            if key not in data:
                data[key] = value
    return data

data = _load_config(CONFIG_PATH)
def get_option(key: str) -> str:
    """
    Get a value from the configuration.
    """
    return data[key]
