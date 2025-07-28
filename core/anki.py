import platform
import subprocess  # nosec
import rich
import requests
import json
import shutil
from config import config


def _invoke(url: str, action: str, **params) -> dict:
    payload = {"action": action, "version": 6, "params": params}
    try:
        response = requests.post(url, json.dumps(payload), timeout=5)
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            if "model was not found" not in str(result["error"]):
                rich.print(
                    f"[bold red]AnkiConnect Error ({action}):[/bold red] {result['error']}"
                )
            return {}
        return result.get("result", {})
    except requests.exceptions.RequestException as e:
        rich.print(f"[bold red]AnkiConnect Request Failed:[/bold red] {e}")
        return {}


def get_windows_host_ip_from_wsl() -> str | None:
    if shutil.which("ip") is None:
        rich.print(
            "[bold yellow][WARN][/bold yellow] 'ip' executable not found in PATH."
        )
        return None
    try:
        output = subprocess.check_output(["ip", "route"], encoding="utf-8")  # nosec
        for line in output.splitlines():
            if line.startswith("default via "):
                return line.split()[2]
    except Exception as e:
        rich.print(
            f"[bold yellow][WARN][/bold yellow] Failed to get Windows host IP: {e}"
        )
    return None


def get_anki_connect_url() -> str:
    default_url = "http://localhost:8765"
    if platform.system() == "Linux":
        try:
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
            if "microsoft" in version_info or "wsl" in version_info:
                rich.print(
                    "-> WSL environment detected. Attempting to find Windows host IP..."
                )
                win_ip = get_windows_host_ip_from_wsl()
                if win_ip:
                    wsl_url = f"http://{win_ip}:8765"
                    rich.print(
                        f"   [green]Success![/green] Using WSL-friendly URL: [bold cyan]{wsl_url}[/bold cyan]"
                    )
                    return wsl_url
        except Exception as e:
            rich.print(
                f"[bold yellow][WARN][/bold yellow] Failed to detect WSL host: {e}"
            )
    return default_url


def test_anki_connection(url: str) -> bool:
    return _invoke(url, "version") != {}


def ensure_deck_exists(url: str):
    deck_name = config.get("anki", {}).get("deck_name", "LeetCode Mastery")
    if deck_name not in _invoke(url, "deckNames"):
        rich.print(f"   - Deck '{deck_name}' not found. Creating...")
        _invoke(url, "createDeck", deck=deck_name)


def add_or_update_notes(anki_url: str, problem_metadata: dict, cards: list):
    deck_name = config.get("anki", {}).get("deck_name")
    scarleet_id = f"{problem_metadata['frontend_id']}-{problem_metadata['slug']}"

    query = f"tag:#ScarleetID:{scarleet_id}"
    existing_ids = _invoke(anki_url, "findNotes", query=query)

    if existing_ids:
        rich.print(
            f"   - Found {len(existing_ids)} existing notes. Deleting and re-adding."
        )
        _invoke(anki_url, "deleteNotes", notes=existing_ids)

    notes_to_add = []

    list_tags = [tag.replace(" ", "_") for tag in problem_metadata.get("lists", [])]

    problem_tags = list_tags + [problem_metadata["slug"], f"#ScarleetID:{scarleet_id}"]

    for card in cards:
        note_type = (
            "Cloze"
            if "{{c1::" in card["front"] or "{{c1::" in card["back"]
            else "Basic"
        )

        front_content = card["front"].strip().replace("\n", "<br>")
        back_content = card["back"].strip().replace("\n", "<br>")

        fields = {}
        if note_type == "Cloze":
            fields["Text"] = f"{front_content}<br><hr>{back_content}"
        else:
            fields["Front"] = front_content
            fields["Back"] = back_content

        notes_to_add.append(
            {
                "deckName": deck_name,
                "modelName": note_type,
                "fields": fields,
                "tags": problem_tags,
            }
        )

    if notes_to_add:
        rich.print(f"   - Adding {len(notes_to_add)} new notes to Anki...")
        result = _invoke(anki_url, "addNotes", notes=notes_to_add)

        if result is None:
            rich.print(
                "[bold red]Error: Failed to add notes to Anki. No response from AnkiConnect.[/bold red]"
            )
            return

        errors = [err for err in result if not isinstance(err, int) and err is not None]
        if errors:
            rich.print("[bold red]Error adding some notes to Anki:[/bold red]")
            rich.print(f"   -> Details: {errors}")
