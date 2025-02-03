from rich import print
LIGHT_BLUE = "#7EBAE4"
LIGHT_RED = "#e47e7e"
LIGHT_YELLOW = "#e4d97e"
LIGHT_GREEN = "#7ee48e"
LIGHT_PURPLE = "#bd7ee4"
DARK_BLUE = "#5277C3"
NIXOS_LOGO = ""
COLORED_LOGO = f"[{DARK_BLUE}]{NIXOS_LOGO}[/]"

def banner():
    print(f"[{LIGHT_GREEN}] nixos-wizard[/] [{LIGHT_PURPLE}]v0.1.0[/]")

def info(msg: str, *args, **kwargs):
    print(f"[{LIGHT_BLUE}] [/]" + msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    print(f"[{LIGHT_RED}]󱗗 [/]" + msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs):
    print(f"[{LIGHT_YELLOW}] [/]" + msg, *args, **kwargs)

def success(msg: str, *args, **kwargs):
    print(f"[{LIGHT_GREEN}]󰗠 [/]{msg}", *args, **kwargs)

def yesno(msg: str, *args, **kwargs) -> bool:
    print(f"[{LIGHT_PURPLE}]󰜴 [/]{msg} \\[{LIGHT_GREEN}]Yy[/]/[{LIGHT_RED}]Nn[/]]", end=" ", *args, **kwargs)
    return input().lower().strip() in ["Y", "y"]

def exception(msg: str, exception: Exception, *args, **kwargs):
    print(f"[{LIGHT_RED}] [/]{msg}: {exception}", *args, **kwargs)
