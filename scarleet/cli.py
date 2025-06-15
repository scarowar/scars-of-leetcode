import typer
from scarleet.commands import new_cmd, docgen_cmd, flashcards_cmd, status_cmd, setup_cmd

app = typer.Typer(
    name="scarleet",
    help="A CLI tool to streamline your LeetCode practice and learning workflow.",
)

app.add_typer(setup_cmd.app, name="setup")
app.add_typer(new_cmd.app, name="new")
app.add_typer(docgen_cmd.app, name="docgen")
app.add_typer(flashcards_cmd.app, name="flashcards")
app.add_typer(status_cmd.app, name="status")

if __name__ == "__main__":
    app()
