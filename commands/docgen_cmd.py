import typer
from typing_extensions import Annotated
import rich
from pathlib import Path
import json
import datetime
from config import PROJECT_ROOT
from core import slm as slm_provider
from core import leetcode_api

app = typer.Typer(help="Generates documentation for a solved problem.")


def find_problem_dir(slug: str) -> Path | None:
    problems_root = PROJECT_ROOT / "problems"
    if not problems_root.exists():
        return None
    for item in problems_root.iterdir():
        if item.is_dir() and item.name.endswith(f"-{slug}"):
            return item
    return None


@app.callback(invoke_without_command=True)
def docgen(
    problem_slug: Annotated[str, typer.Argument(help="The URL slug of the problem.")]
):
    rich.print(f"-> Generating docs for: [bold magenta]{problem_slug}[/bold magenta]")
    problem_dir = find_problem_dir(problem_slug)
    if not problem_dir:
        rich.print(
            f"[bold red]Error:[/bold red] Directory for slug '{problem_slug}' not found."
        )
        raise typer.Exit(code=1)

    solution_path = problem_dir / "solution.py"
    metadata_path = problem_dir / "metadata.json"
    if not all([solution_path.exists(), metadata_path.exists()]):
        rich.print(f"[bold red]Error:[/bold red] Missing files in {problem_dir}")
        raise typer.Exit(code=1)

    solution_code = solution_path.read_text()
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    problem_details = leetcode_api.get_problem_details(problem_slug)
    problem_description = problem_details.get("description", "Not available.")

    readme_content = slm_provider.generate_readme_content(
        title=metadata["title"],
        url=metadata["url"],
        difficulty=metadata["difficulty"],
        description=problem_description,
        code=solution_code,
    )

    if not readme_content:
        rich.print("[bold red]Failed to generate README content from SLM.[/bold red]")
        raise typer.Exit(code=1)

    notes_raw = readme_content.get("notes", [])
    if isinstance(notes_raw, list):
        notes_text = "\n".join(notes_raw)
    else:
        notes_text = str(notes_raw)

    readme_path = problem_dir / "README.md"
    full_readme_text = (
        f"# Problem {metadata['frontend_id']}: {metadata['title']}\n\n"
        f"## Link\n- [{metadata['title']}]({metadata['url']})\n\n"
        f"## Intuition\n{readme_content.get('intuition', 'N/A')}\n\n"
        f"## Approach\n{readme_content.get('approach', 'N/A')}\n\n"
        f"## Complexity\n"
        f"- Time: `{readme_content.get('complexity_time', 'N/A')}`\n"
        f"- Space: `{readme_content.get('complexity_space', 'N/A')}`\n\n"
        f"## Notes\n{notes_text}"
    )

    readme_path.write_text(full_readme_text)
    rich.print("   - Created/Updated [green]README.md[/green]")

    metadata.update(
        {
            "status": "documented",
            "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
        }
    )
    metadata.pop("solution_stats", None)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    rich.print("   - Updated status in [green]metadata.json[/green]")
    rich.print("\n[bold green]✅ Docgen complete![/bold green]")
