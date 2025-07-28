import typer
from typing_extensions import Annotated
import rich
from rich.table import Table
import json
from scarleet.config import PROJECT_ROOT

app = typer.Typer(help="Displays a summary table of all problems.")


def _gather_problem_data() -> list[dict]:
    problems_root = PROJECT_ROOT / "problems"
    if not problems_root.exists():
        return []

    all_problems = []
    for problem_dir in sorted(problems_root.iterdir()):
        if not problem_dir.is_dir():
            continue

        metadata_path = problem_dir / "metadata.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    data = json.load(f)
                    data["frontend_id"] = int(data.get("frontend_id", 0))
                    all_problems.append(data)
            except (json.JSONDecodeError, ValueError):
                rich.print(
                    f"[bold yellow]Warning:[/bold yellow] Could not parse metadata for {problem_dir.name}"
                )

    all_problems.sort(key=lambda p: p.get("frontend_id", 0))
    return all_problems


def _generate_markdown_table(problems: list[dict]) -> str:
    header = "| # | Title | Status | Difficulty | Tags |\n"
    separator = "|---|---|---|---|---|\n"
    body = ""
    for p in problems:
        tags = ", ".join(p.get("lists", []))
        body += f"| {p.get('frontend_id', '')} | [{p.get('title', '')}]({p.get('url', '')}) | {p.get('status', '')} | {p.get('difficulty', '')} | {tags} |\n"

    return f"# LeetCode Progress\n\n{header}{separator}{body}"


@app.callback(invoke_without_command=True)
def status(
    update_readme: Annotated[
        bool,
        typer.Option(
            "--update-readme",
            "-u",
            help="Update the root problems/README.md with the status table.",
        ),
    ] = False
):
    problems = _gather_problem_data()
    if not problems:
        rich.print(
            "[yellow]No problems found. Use 'scarleet new <slug>' to add one.[/yellow]"
        )
        raise typer.Exit()

    table = Table(title="Scarleet Problem Status")
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Difficulty", style="yellow")
    table.add_column("Tags", style="blue")

    difficulty_colors = {"Easy": "green", "Medium": "yellow", "Hard": "red"}
    status_colors = {"new": "yellow", "documented": "green", "archived": "dim"}

    for p in problems:
        difficulty = p.get("difficulty", "N/A")
        status = p.get("status", "N/A")

        diff_style = difficulty_colors.get(difficulty, "white")
        status_style = status_colors.get(status, "white")

        tags = ", ".join(p.get("lists", []))

        table.add_row(
            str(p.get("frontend_id", "")),
            f"[{p.get('title', '')}]({p.get('url', '')})",
            f"[{status_style}]{status}[/{status_style}]",
            f"[{diff_style}]{difficulty}[/{diff_style}]",
            tags,
        )

    rich.print(table)

    if update_readme:
        rich.print("\n-> Updating root `problems/README.md`...")
        readme_path = PROJECT_ROOT / "problems" / "README.md"
        markdown_content = _generate_markdown_table(problems)
        readme_path.write_text(markdown_content)
        rich.print("   [green]Success![/green] README file updated.")
