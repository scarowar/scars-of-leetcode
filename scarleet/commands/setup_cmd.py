import typer
import rich
import shutil
import subprocess  # nosec
import requests
import platform
from scarleet.config import CONFIG_FILE_PATH

app = typer.Typer(help="Initializes Scarleet and sets up dependencies like Ollama.")

DEFAULT_CONFIG_CONTENT = """
# Scarleet Configuration File

[user]
author = "Your Name"

[leetcode]
api_url = "https://leetcode.com/graphql"

[slm]
endpoint = "http://localhost:11434/api/generate"
# Changed to a more lightweight model suitable for CPU-only machines with 16GB RAM.
# gemma:2b is a capable ~3GB model from Google.
model = "gemma:2b"

# Prompt for generating the README content
docgen_prompt_template = \"\"\"
You are an expert programmer analyzing a LeetCode solution. Based on the provided problem description and Python code, generate a concise explanation. My solution was faster than {time_percentile}% of submissions and used less memory than {space_percentile}% of submissions. Return your response as a single, clean JSON object with the keys "intuition", "approach", and "notes". Do not include any other text.

**Problem:** {title} ({difficulty})
**Description:**
---
{description}
---
**My Solution:**
---
```python
{code}
```
---
\"\"\"

# Prompt for generating Anki flashcards
flashcard_prompt_template = \"\"\"
You are an expert programmer creating spaced repetition flashcards from a LeetCode solution.
Based on the provided solution code and explanations, generate 5-7 high-quality flashcards.
Return a single, clean JSON object with a "cards" key, which is an array of objects.
Each card object must have "front" and "back" keys.
For cloze deletions, use the format `{{c1::text to hide}}`.

**Context:**
- **Problem:** {title}
- **My Explanation:**
  - **Intuition:** {intuition}
  - **Approach:** {approach}
- **My Solution Code:**
  ```python
  {code}
  ```
\"\"\"

[anki]
deck_name = "LeetCode Mastery"
note_type = {
    "name": "Scarleet Basic",
    "fields": ["ProblemTitle", "ProblemURL", "Question", "Answer", "ScarleetID", "Tags"],
    "card_templates": [
        {
            "Name": "Card 1",
            "Front": "{{Question}}",
            "Back": "{{FrontSide}}\\\\n\\\\n<hr id=answer>\\\\n\\\\n{{Answer}}\\\\n\\\\n<br><br>\\\\n<div style='font-size:12px; color:grey;'>{{ProblemTitle}} ({{Tags}})</div>"
        }
    ]
}
"""


def _check_ollama_installed():
    return shutil.which("ollama") is not None


def _check_ollama_running():
    try:
        requests.get("http://localhost:11434", timeout=3)
        return True
    except requests.RequestException:
        return False


def _pull_slm_model(model_name: str):
    rich.print(
        f"-> Attempting to pull the recommended SLM: [bold cyan]{model_name}[/bold cyan]..."
    )
    rich.print("   This may take some time depending on your internet connection.")

    if shutil.which("ollama") is None:
        rich.print("[bold red]Error:[/bold red] 'ollama' executable not found in PATH.")
        return
    try:
        process = subprocess.Popen(  # nosec
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        for line in iter(process.stdout.readline, ""):
            rich.print(f"   [dim]{line.strip()}[/dim]")
        process.wait()
        if process.returncode == 0:
            rich.print(f"   [green]Success![/green] Model '{model_name}' is ready.")
        else:
            rich.print(
                f"[bold red]Error:[/bold red] Failed to pull model. Please try `ollama pull {model_name}` manually."
            )
    except FileNotFoundError:
        rich.print("[bold red]Error:[/bold red] 'ollama' command not found.")
    except Exception as e:
        rich.print(
            f"[bold red]An error occurred while pulling the model:[/bold red] {e}"
        )


@app.callback(invoke_without_command=True)
def setup():
    rich.print("[bold]🚀 Starting Scarleet Setup[/bold]")

    if not CONFIG_FILE_PATH.exists():
        rich.print(
            "-> Configuration file not found. Creating a default `scarleet.toml`..."
        )
        with open(CONFIG_FILE_PATH, "w") as f:
            f.write(DEFAULT_CONFIG_CONTENT)
        rich.print("   [green]Success![/green] `scarleet.toml` created.")

    rich.print("-> Checking for Ollama installation...")
    if not _check_ollama_installed():
        rich.print("\n[bold red]Error: Ollama is not installed.[/bold red]")
        rich.print(
            "Scarleet uses Ollama to run local language models for documentation and flashcard generation."
        )
        rich.print(
            "Please install it from [link=https://ollama.com]https://ollama.com[/link] and run this command again."
        )
        raise typer.Exit(code=1)
    rich.print("✅ [green]Ollama is installed.[/green]")

    rich.print("-> Checking if Ollama service is running...")
    if not _check_ollama_running():
        rich.print("\n[bold red]Error: Ollama is not running.[/bold red]")
        rich.print("Please start the Ollama application and run this command again.")
        if platform.system() == "Darwin":
            rich.print("   (On macOS, find it in your Applications folder.)")
        elif platform.system() == "Windows":
            rich.print("   (On Windows, check your system tray or Start Menu.)")
        elif platform.system() == "Linux":
            rich.print("   (On Linux, you may need to run `systemctl start ollama`.)")
        raise typer.Exit(code=1)
    rich.print("✅ [green]Ollama service is running.[/green]")

    from scarleet.config import config as loaded_config

    model_to_pull = loaded_config.get("slm", {}).get("model", "gemma:2b")
    _pull_slm_model(model_to_pull)

    rich.print(
        "\n[bold green]🎉 Scarleet setup is complete! You're ready to start solving.[/bold green]"
    )
