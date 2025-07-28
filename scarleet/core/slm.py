import os
import openai
import rich
import json
from scarleet.config import config
from dotenv import load_dotenv

load_dotenv()


def _call_slm(prompt: str) -> dict | None:
    slm_config = config.get("slm", {})
    api_url, model = slm_config.get("endpoint"), slm_config.get("model")
    if not api_url or not model:
        rich.print("[bold red]Error:[/bold red] SLM config missing in scarleet.toml.")
        return None
    try:
        import requests

        rich.print("[yellow]Using local SLM endpoint for generation...[/yellow]")
        response = requests.post(
            api_url,
            json={"model": model, "prompt": prompt, "format": "json", "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return json.loads(response.json().get("response", "{}"))
    except Exception as e:
        rich.print(f"[bold red]Local SLM API request failed:[/bold red] {e}")
    return None


def get_openai_env():
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_API_KEY")
    api_base = os.getenv("OPENAI_API_URL") or os.getenv("AZURE_API_BASE")
    model = os.getenv("OPENAI_MODEL") or os.getenv("AZURE_DEPLOYMENT_NAME") or "gpt-4o"
    api_version = os.getenv("OPENAI_API_VERSION") or os.getenv("AZURE_API_VERSION")
    is_azure = bool(os.getenv("AZURE_API_KEY") or os.getenv("AZURE_API_BASE"))
    return {
        "api_key": api_key,
        "api_base": api_base,
        "model": model,
        "api_version": api_version,
        "is_azure": is_azure,
    }


def call_openai_chat_api(prompt: str, env: dict) -> str | None:
    try:
        response_format = {"type": "json_object"}
        if env["is_azure"]:
            rich.print("[yellow]Using Azure OpenAI for generation...[/yellow]")
            client = openai.AzureOpenAI(
                api_key=env["api_key"],
                api_version=env["api_version"],
                azure_endpoint=env["api_base"],
            )
            response = client.chat.completions.create(
                model=env["model"],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for LeetCode and spaced repetition flashcards.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2048,
                temperature=0.7,
                response_format=response_format,
            )
        else:
            rich.print("[yellow]Using OpenAI for generation...[/yellow]")
            client = openai.OpenAI(
                api_key=env["api_key"],
                base_url=env["api_base"] if env["api_base"] else None,
            )
            response = client.chat.completions.create(
                model=env["model"],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant for LeetCode and spaced repetition flashcards.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2048,
                temperature=0.7,
                response_format=response_format,
            )
        return response.choices[0].message.content
    except Exception as e:
        rich.print(
            f"[bold red]OpenAI/Azure Chat API failed:[/bold red] {e}\n[bold yellow]Falling back to local SLM...[/bold yellow]"
        )
        return None


def generate_readme_content(**kwargs) -> dict | None:
    prompt = config.get("slm", {}).get("docgen_prompt_template", "").format(**kwargs)
    env = get_openai_env()
    if env["api_key"] and env["api_base"] and env["model"]:
        result = call_openai_chat_api(prompt, env)
        if result:
            try:
                return json.loads(result)
            except Exception as e:
                rich.print(
                    f"[bold red]Failed to parse OpenAI/Azure response:[/bold red] {e}\n[bold yellow]Falling back to local SLM...[/bold yellow]"
                )
    return _call_slm(prompt)


def normalize_cloze(text):
    # Replace all {{cN::...}} with {{c1::...}} for Anki compatibility
    import re

    return re.sub(r"\{\{c\d+::", "{{c1::", text)


def filter_tags(metadata, extra_lists=None):
    tags = set()
    # Add tags from metadata (e.g., topic_tags, difficulty, etc.)
    for key in ("tags", "topic_tags", "difficulty", "category"):
        val = metadata.get(key)
        if isinstance(val, str):
            tags.update(val.lower().replace(",", " ").split())
        elif isinstance(val, list):
            tags.update([str(v).lower() for v in val])
    # Add NeetCode150/Blind75 if in extra_lists
    if extra_lists:
        if extra_lists.get("neetcode150"):
            tags.add("NeetCode150")
        if extra_lists.get("blind75"):
            tags.add("Blind75")
    return " ".join(sorted(tags))


def enforce_card_variety(cards):
    # Ensure at least 2 cloze, 2 Q&A, 1 edge case, 1 fill-in-the-blank, 1 explanation
    cloze = [c for c in cards if c.get("card_type") == "cloze"]
    qna = [
        c
        for c in cards
        if c.get("card_type") == "basic" and c["front"].strip().endswith("?")
    ]
    edge = [
        c
        for c in cards
        if "edge case" in c["front"].lower() or "edge case" in c["back"].lower()
    ]
    fill = [
        c
        for c in cards
        if "___" in c["front"] or "fill in the blank" in c["front"].lower()
    ]
    explain = [
        c
        for c in cards
        if c["front"].lower().startswith("explain")
        or c["front"].lower().startswith("describe")
    ]
    return (
        len(cloze) >= 2
        and len(qna) >= 2
        and len(edge) >= 1
        and len(fill) >= 1
        and len(explain) >= 1
    )


def postprocess_flashcards(flashcard_data, metadata, extra_lists=None):
    # Normalize cloze, set tags, and enforce card variety
    cards = flashcard_data.get("cards", [])
    for c in cards:
        # Normalize cloze deletions
        if c.get("card_type") == "cloze" or ("{{c" in c["front"]):
            c["front"] = normalize_cloze(c["front"])
            c["back"] = ""  # For Anki cloze, back is empty
            c["card_type"] = "cloze"
        # Fill-in-the-blank: basic card, blank in front, answer in back
        elif "___" in c["front"]:
            c["card_type"] = "basic"
            # leave front and back as is
        # Explanation cards: treat as basic unless they use cloze
        elif c["front"].lower().startswith("explain") or c["front"].lower().startswith(
            "describe"
        ):
            c["card_type"] = "basic"
        else:
            c["card_type"] = "basic"
        # Set tags from metadata and lists
        c["tags"] = filter_tags(metadata, extra_lists)
    if not enforce_card_variety(cards):
        rich.print(
            "[bold yellow][WARN][/bold yellow] Not all required card types are present in the generated flashcards."
        )
    return flashcard_data


def generate_flashcard_content(**kwargs) -> dict | None:
    prompt = config.get("slm", {}).get("flashcard_prompt_template", "").format(**kwargs)
    env = get_openai_env()
    metadata = kwargs.get("metadata", {})
    extra_lists = kwargs.get("extra_lists", {})
    if env["api_key"] and env["api_base"] and env["model"]:
        result = call_openai_chat_api(prompt, env)
        if result:
            try:
                # If result is a response object, get .content
                if hasattr(result, "content"):
                    result = result.content
                # If result is a string, parse as JSON
                import json

                flashcard_data = json.loads(result)
                return postprocess_flashcards(flashcard_data, metadata, extra_lists)
            except Exception as e:
                rich.print(
                    f"[bold red]Failed to parse OpenAI/Azure response:[/bold red] {e}\n[bold yellow]Falling back to local SLM...[/bold yellow]"
                )
    # Fallback to SLM
    flashcard_data = _call_slm(prompt)
    if flashcard_data:
        return postprocess_flashcards(flashcard_data, metadata, extra_lists)
    return None
