import typer
from typing_extensions import Annotated
import rich
import json
import re
from scarleet.core import anki, slm
from scarleet.commands.docgen_cmd import find_problem_dir

app = typer.Typer(help="Generates and syncs Anki flashcards for a problem.")


def extract_readme_sections(readme_text: str) -> dict:
    sections = {"intuition": "", "approach": ""}
    try:
        intuition_match = re.search(
            r"## Intuition\n(.*?)\n## Approach", readme_text, re.DOTALL
        )
        if intuition_match:
            sections["intuition"] = intuition_match.group(1).strip()

        approach_match = re.search(
            r"## Approach\n(.*?)\n## Complexity", readme_text, re.DOTALL
        )
        if approach_match:
            sections["approach"] = approach_match.group(1).strip()
    except Exception as e:
        import rich

        rich.print(
            f"[bold yellow][WARN][/bold yellow] Exception in extract_sections_from_readme: {e}"
        )
    return sections


@app.callback(invoke_without_command=True)
def flashcards(
    problem_slug: Annotated[str, typer.Argument(help="The URL slug of the problem.")]
):
    rich.print(
        f"-> Generating flashcards for: [bold magenta]{problem_slug}[/bold magenta]"
    )
    problem_dir = find_problem_dir(problem_slug)
    if not problem_dir:
        rich.print(
            f"[bold red]Error:[/bold red] Directory for slug '{problem_slug}' not found."
        )
        raise typer.Exit(code=1)

    readme_path = problem_dir / "README.md"
    if not readme_path.exists():
        rich.print(
            "[bold red]Error:[/bold red] `README.md` not found. Run `docgen` first."
        )
        raise typer.Exit(code=1)

    readme_text = readme_path.read_text()
    solution_code = (problem_dir / "solution.py").read_text()
    with open(problem_dir / "metadata.json", "r") as f:
        metadata = json.load(f)

    readme_sections = extract_readme_sections(readme_text)

    from scarleet.core import slm as slm_provider

    env = slm_provider.get_openai_env()
    backend = "local SLM"
    if env["api_key"] and env["api_base"] and env["model"]:
        backend = "Azure OpenAI" if env["is_azure"] else "OpenAI"
    rich.print(
        f"-> Generating flashcard content with [bold cyan]{backend}[/bold cyan]..."
    )

    # Determine if problem is in NeetCode150 or Blind75
    extra_lists = {}
    if "neetcode150" in metadata.get("lists", []):
        extra_lists["neetcode150"] = True
    if "blind75" in metadata.get("lists", []):
        extra_lists["blind75"] = True

    flashcard_data = slm.generate_flashcard_content(
        problem_id=metadata.get("frontend_id") or metadata.get("id") or "",
        title=metadata["title"],
        intuition=readme_sections["intuition"],
        approach=readme_sections["approach"],
        code=solution_code,
        metadata=metadata,
        extra_lists=extra_lists,
    )

    if not flashcard_data or "cards" not in flashcard_data:
        rich.print(
            "[bold red]Error:[/bold red] Failed to get valid flashcard data from SLM."
        )
        raise typer.Exit(code=1)

    cards_to_add = flashcard_data["cards"]

    # --- Flashcard variety validation ---
    cloze_count = sum("{{c1::" in c["front"] for c in cards_to_add)
    qna_count = sum(
        c["front"].strip().endswith("?") and "{{c1::" not in c["front"]
        for c in cards_to_add
    )
    edge_case_count = sum(
        "edge case" in c["front"].lower() or "edge case" in c["back"].lower()
        for c in cards_to_add
    )
    fill_blank_count = sum(
        "fill in the blank" in c["front"].lower() or "___" in c["front"]
        for c in cards_to_add
    )
    answer_count = sum("answer:" in c["back"].lower() for c in cards_to_add)
    if cloze_count < 2:
        rich.print(
            "[bold yellow][WARN][/bold yellow] Less than 2 cloze deletion cards generated."
        )
    if qna_count < 2:
        rich.print("[bold yellow][WARN][/bold yellow] Less than 2 Q&A cards generated.")
    if edge_case_count < 1:
        rich.print("[bold yellow][WARN][/bold yellow] No edge case card detected.")
    if fill_blank_count < 1:
        rich.print(
            "[bold yellow][INFO][/bold yellow] No fill-in-the-blank card detected."
        )
    if answer_count < 1:
        rich.print(
            "[bold yellow][INFO][/bold yellow] No explicit answer card detected."
        )

    rich.print(f"   [green]Success![/green] Generated {len(cards_to_add)} flashcards.")

    anki_url = anki.get_anki_connect_url()
    if not anki.test_anki_connection(anki_url):
        rich.print(
            f"[bold red]Error:[/bold red] Could not connect to AnkiConnect at {anki_url}."
        )
        raise typer.Exit(code=1)

    rich.print("-> Syncing with Anki...")
    anki.ensure_deck_exists(anki_url)
    anki.add_or_update_notes(
        anki_url=anki_url, problem_metadata=metadata, cards=cards_to_add
    )
    rich.print("\n[bold green]✅ Flashcard sync complete![/bold green]")
