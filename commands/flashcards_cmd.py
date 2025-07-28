import typer
from typing_extensions import Annotated
import rich
import json
import re
from core import anki, slm
from commands.docgen_cmd import find_problem_dir

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

    rich.print("-> Generating flashcard content with local SLM...")
    flashcard_data = slm.generate_flashcard_content(
        title=metadata["title"],
        intuition=readme_sections["intuition"],
        approach=readme_sections["approach"],
        code=solution_code,
    )

    if not flashcard_data or "cards" not in flashcard_data:
        rich.print(
            "[bold red]Error:[/bold red] Failed to get valid flashcard data from SLM."
        )
        raise typer.Exit(code=1)

    cards_to_add = flashcard_data["cards"]
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
