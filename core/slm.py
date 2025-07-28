import requests
import rich
import json
from config import config


def _call_slm(prompt: str) -> dict | None:
    slm_config = config.get("slm", {})
    api_url, model = slm_config.get("endpoint"), slm_config.get("model")
    if not api_url or not model:
        rich.print("[bold red]Error:[/bold red] SLM config missing in scarleet.toml.")
        return None
    try:
        response = requests.post(
            api_url,
            json={"model": model, "prompt": prompt, "format": "json", "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return json.loads(response.json().get("response", "{}"))
    except requests.RequestException as e:
        rich.print(f"[bold red]API Request to SLM Failed:[/bold red] {e}")
    except json.JSONDecodeError:
        rich.print(f"[bold red]SLM JSON Decode Error:[/bold red] {response.text}")
    return None


def generate_readme_content(**kwargs) -> dict | None:
    prompt = config.get("slm", {}).get("docgen_prompt_template", "").format(**kwargs)
    return _call_slm(prompt)


def generate_flashcard_content(**kwargs) -> dict | None:
    prompt = config.get("slm", {}).get("flashcard_prompt_template", "").format(**kwargs)
    return _call_slm(prompt)
