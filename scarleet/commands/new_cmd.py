import typer
from typing_extensions import Annotated
import rich
import json
import datetime

from scarleet.config import PROJECT_ROOT
from scarleet.core import leetcode_api

app = typer.Typer(help="Sets up a new problem directory.")


def _load_problem_lists():
    lists_dir = PROJECT_ROOT / ".scarleet" / "lists"
    problem_lists = {}
    if not lists_dir.exists():
        rich.print(
            "[bold yellow]Warning:[/bold yellow] '.scarleet/lists' directory not found. Cannot tag problems."
        )
        return problem_lists

    for list_file in lists_dir.glob("*.json"):
        try:
            with open(list_file, "r") as f:
                list_name = list_file.stem
                problem_lists[list_name] = set(json.load(f))
        except (json.JSONDecodeError, IOError) as e:
            rich.print(f"[bold red]Error loading {list_file}:[/bold red] {e}")
    return problem_lists


def _get_list_tags_for_slug(slug, problem_lists):
    tags = []
    list_name_map = {"blind75": "Blind 75", "neetcode150": "NeetCode 150"}
    for list_name, slugs_set in problem_lists.items():
        if slug in slugs_set:
            tags.append(list_name_map.get(list_name, list_name))
    return tags


@app.callback(invoke_without_command=True)
def new(
    problem_slug: Annotated[
        str, typer.Argument(help="The URL slug of the problem (e.g., 'two-sum').")
    ]
):
    rich.print(
        f"-> Setting up new problem: [bold magenta]{problem_slug}[/bold magenta]"
    )

    problem_lists = _load_problem_lists()

    rich.print("-> Fetching problem details from LeetCode API...")
    problem_data = leetcode_api.get_problem_details(problem_slug)

    if not problem_data:
        rich.print(
            f"[bold red]Error:[/bold red] Could not fetch data for slug '{problem_slug}'. Please check the slug and try again."
        )
        raise typer.Exit(code=1)

    rich.print(
        f"   [green]Success![/green] Found problem: [bold]{problem_data['title']}[/bold] ({problem_data['difficulty']})"
    )

    problem_id = problem_data.get("frontend_id", "0")
    folder_name = f"{problem_id}-{problem_slug}"
    problem_dir = PROJECT_ROOT / "problems" / folder_name

    if problem_dir.exists():
        rich.print(
            f"[bold yellow]Warning:[/bold yellow] Directory '{problem_dir}' already exists. Aborting."
        )
        raise typer.Exit()

    rich.print(f"-> Creating directory and files at [cyan]{problem_dir}[/cyan]")
    problem_dir.mkdir(parents=True, exist_ok=True)

    metadata_path = problem_dir / "metadata.json"
    list_tags = _get_list_tags_for_slug(problem_slug, problem_lists)
    if list_tags:
        rich.print(f"   -> Tagging with: [bold cyan]{', '.join(list_tags)}[/bold cyan]")

    metadata_content = {
        "title": problem_data["title"],
        "slug": problem_slug,
        "frontend_id": problem_id,
        "url": f"https://leetcode.com/problems/{problem_slug}/",
        "difficulty": problem_data["difficulty"],
        "tags": problem_data["tags"],
        "lists": list_tags,
        "status": "new",
        "solution_stats": None,
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata_content, f, indent=2)
    rich.print("   - Created [green]metadata.json[/green]")

    code_snippet = problem_data.get("code_snippet", "class Solution:\n    pass\n")

    solution_path = problem_dir / "solution.py"
    with open(solution_path, "w") as f:
        f.write("#!/usr/bin/env python\n\n")
        f.write(f"# LeetCode Problem: {problem_data['title']}\n")
        f.write(f"# URL: {metadata_content['url']}\n\n")
        f.write("from typing import *\n\n")
        f.write(code_snippet)
    rich.print("   - Created [green]solution.py[/green] with wildcard type hints")

    test_path = problem_dir / "test_cases.py"
    with open(test_path, "w") as f:
        f.write("import unittest\n")
        f.write("from solution import Solution\n\n")
        f.write("class TestSolution(unittest.TestCase):\n")
        f.write("    def setUp(self):\n")
        f.write("        self.solution = Solution()\n\n")
        f.write("    def test_example_1(self):\n")
        f.write("        # Example from LeetCode problem description\n")
        f.write(
            "        # self.assertEqual(self.solution.your_method_name(params), expected_output)\n"
        )
        f.write("        pass\n\n")
        f.write("    # Add more test cases for edge cases and other scenarios\n\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    unittest.main()\n")
    rich.print("   - Created simplified [green]test_cases.py[/green]")

    rich.print("\n[bold green]✅ Setup complete! Happy coding![/bold green]")
    rich.print(f"Navigate to the directory: [bold cyan]cd '{problem_dir}'[/bold cyan]")
