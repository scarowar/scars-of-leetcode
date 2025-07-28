# Scars of LeetCode

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/scarowar/scars-of-leetcode)
[![pre-commit](https://github.com/scarowar/scars-of-leetcode/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/scarowar/scars-of-leetcode/actions/workflows/pre-commit.yml)
[![CodeQL](https://github.com/scarowar/scars-of-leetcode/actions/workflows/codeql.yml/badge.svg)](https://github.com/scarowar/scars-of-leetcode/actions/workflows/codeql.yml)
[![Dependabot Status](https://img.shields.io/badge/dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/scarowar/scars-of-leetcode/pulls?q=is%3Apr+label%3Adependencies)

**Every Accepted was paid in blood, sweat, and runtime errors.**

> **Note:** This repository is a work in progress. Expect ongoing improvements and refinements!

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Installation](#installation)
* [The Workflow: A Quick Start](#the-workflow-a-quick-start)
* [Command Usage](#command-usage)
* [Configuration](#configuration)
* [File & Folder Structure](#file--folder-structure)
* [Contributing & Support](#contributing--support)
* [License](#license)
* [OpenAI API Usage (Optional)](#openai-api-usage-optional)

## Overview

**Scars of LeetCode** is a repository powered by **Scarleet**, a command-line tool designed to automate and streamline the entire workflow for mastering LeetCode problems. It helps you:

* Organize solutions in a structured way.
* Automatically generate high-quality documentation for solved problems.
* Create evidence-based, spaced-repetition flashcards for deep learning.
* Track your progress with a dynamic summary table.
* Seamlessly integrate with Anki for efficient review.

This project is for anyone who wants to build a deep, recallable understanding of algorithms and data structures through a powerful, automated system.

## Features

* **CLI-Driven Workflow**: Manage your entire practice from the command line.
* **Automated Scaffolding**: Instantly create a structured directory for any LeetCode problem.
* **AI-Powered Documentation**: Use a local language model to automatically generate high-quality READMEs explaining your solution's intuition, approach, and complexity.
* **Automated Flashcard Generation**: Turn your solutions into effective Anki flashcards (both Q&A and Cloze deletion) with a single command.
* **Intelligent Anki Integration**: Automatically detects your environment (including WSL) to connect to Anki and sync cards without manual configuration.
* **Progress Tracking**: Generate a summary table of your progress at any time.

## Installation

**Prerequisites:**

* Python 3.8+
* [Ollama](https://ollama.com/) for running the local language model.
* [Anki](https://apps.ankiweb.net/) desktop application with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed.

**Setup Steps:**

1.  Clone the repository:
    ```sh
    git clone [https://github.com/scarowar/scars-of-leetcode.git](https://github.com/scarowar/scars-of-leetcode.git)
    cd scars-of-leetcode
    ```
2.  Install the required Python packages:
    ```sh
    pip install "typer[all]" rich toml requests
    ```
3.  Run the interactive setup command. This will create your configuration file, check for Ollama, and download the recommended language model.
    ```sh
    python main.py setup
    ```

## Installation (Local CLI)

You can install all dependencies with either:

```sh
pip install -r requirements.txt
```

or, if you prefer PEP 621/modern Python packaging:

```sh
pip install .
```

Both methods will install all required packages for Scarleet.

See [INSTALL.md](INSTALL.md) for more details.

## The Workflow: A Quick Start

The entire process is designed to be simple and flow naturally with your practice.

1.  **Create a New Problem:**
    ```sh
    scarleet new <problem-slug>
    # Example: scarleet new two-sum
    ```
2.  **Solve It:** Navigate to the new `problems/[id]-[slug]` directory and write your solution in `solution.py`.
3.  **Generate Docs:** After your solution is accepted on LeetCode, let Scarleet document it for you.
    ```sh
    scarleet docgen <problem-slug>
    ```
4.  **Create Flashcards:** Turn your documented solution into study material.
    ```sh
    scarleet flashcards <problem-slug>
    ```
5.  **Track Your Progress:** View a summary of all your solved problems and update the master `README.md`.
    ```sh
    scarleet status --update-readme
    ```

## Command Usage

* **`setup`**: Initializes the project. Should be run once.
* **`new <slug>`**: Scaffolds a new problem directory.
* **`docgen <slug>`**: Generates a `README.md` for a problem using your solution and the local SLM.
* **`flashcards <slug>`**: Generates Anki flashcards from your `README.md` and solution.
* **`status`**: Displays a summary table of all problems. Use the `--update-readme` or `-u` flag to write this table to `problems/README.md`.

## Configuration

All configuration is managed in the `scarleet.toml` file, which is created by the `setup` command. Here you can change:

* The language model used (e.g., from `gemma:2b` to another Ollama model).
* The prompts used for generating documentation and flashcards.
* The name of your Anki deck.

## File & Folder Structure

```
.
├── scarleet.toml        # Global configuration for the tool
├── main.py              # The CLI entrypoint
├── commands/            # Logic for each CLI command
├── core/                # Core logic for Anki, SLM, and LeetCode API
├── problems/
│   ├── ...              # One folder per problem, each with solution and docs
│   └── README.md        # Auto-generated progress summary
└── .scarleet/
    └── lists/
        ├── blind75.json         # Blind 75 list
        └── neetcode150.json     # NeetCode 150 list
```


## OpenAI or Azure OpenAI Usage (Optional)

Scarleet can use either OpenAI or Azure OpenAI models (like GPT-4, GPT-3.5, etc.) for generating flashcards and documentation. To enable this, set the following environment variables in a `.env` file (which should NOT be committed to version control):

### For OpenAI:
```
OPENAI_API_KEY=sk-...your-key...
OPENAI_API_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o
OPENAI_API_VERSION=2024-06-01
```

### For Azure OpenAI:
```
AZURE_API_KEY=your-azure-key
AZURE_API_BASE=https://your-resource.openai.azure.com
AZURE_DEPLOYMENT_NAME=your-deployment
AZURE_API_VERSION=2024-06-01
```

- Scarleet will auto-detect which provider to use based on your `.env`.
- If neither is set, Scarleet will use your local SLM endpoint as a fallback.
- Install dependencies for .env support:
  ```sh
  pip install python-dotenv
  ```
- The `openai` Python package is required (see `requirements.txt`).

**Never commit your `.env` file or API keys to version control.**

---

## Contributing & Support

Contributions, suggestions, and improvements are welcome! Please open an issue or PR. By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

**Happy grinding — and may your scars become your strength!**
