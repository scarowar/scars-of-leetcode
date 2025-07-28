import tomli
from pathlib import Path
import sys
import rich

PROJECT_ROOT = Path.cwd()
CONFIG_FILE_PATH = PROJECT_ROOT / "scarleet.toml"


def load_config():
    if not CONFIG_FILE_PATH.exists():
        rich.print(
            f"[bold red]Error:[/bold red] Configuration file not found at [cyan]{CONFIG_FILE_PATH}[/cyan]."
        )
        sys.exit(1)
    try:
        with open(CONFIG_FILE_PATH, "rb") as f:
            return tomli.load(f)
    except tomli.TOMLDecodeError as e:
        rich.print(f"[bold red]Error parsing {CONFIG_FILE_PATH}:[/bold red] {e}")
        sys.exit(1)


config = load_config()
