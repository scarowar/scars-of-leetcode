


# Scars of LeetCode

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/scarowar/scars-of-leetcode)
[![pre-commit](https://github.com/scarowar/scars-of-leetcode/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/scarowar/scars-of-leetcode/actions/workflows/pre-commit.yml)
[![CodeQL](https://github.com/scarowar/scars-of-leetcode/actions/workflows/codeql.yml/badge.svg)](https://github.com/scarowar/scars-of-leetcode/actions/workflows/codeql.yml)
[![Dependabot Status](https://img.shields.io/badge/dependabot-enabled-brightgreen?logo=dependabot)](https://github.com/scarowar/scars-of-leetcode/pulls?q=is%3Apr+label%3Adependencies)

**Every Accepted was paid in blood, sweat, and runtime errors.**

> **Note:** This repository is a work in progress. Expect ongoing improvements and refinements!

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [File/Folder Structure](#filefolder-structure)
- [Best Practices](#best-practices)
- [Code Quality: pre-commit Hooks](#code-quality-pre-commit-hooks)
- [Contributing & Support](#contributing--support)
- [License](#license)
- [Citation](#citation)

---

## Overview

Scars of LeetCode is an automation-driven workflow and knowledge base for mastering LeetCode problems. It helps you:
- Organize and document solutions
- Generate high-quality spaced-repetition flashcards
- Track your progress
- Integrate with Anki for efficient review

This project is ideal for learners, interview preppers, and anyone who wants to build a deep, recallable understanding of algorithms and data structures.

## Features

- Effortless problem management and documentation
- Automated, evidence-based Anki flashcard generation
- Seamless integration with Anki (including WSL support)
- A single source of truth for all your LeetCode learning
- Automated code quality, security, and dependency checks

---

## Installation

**Prerequisites:**
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- [pre-commit](https://pre-commit.com/) (for code quality)
- [Anki](https://apps.ankiweb.net/) with [AnkiConnect](https://ankiweb.net/shared/info/2055492159) (for flashcard import)

**Setup:**
```sh
git clone https://github.com/scarowar/scars-of-leetcode.git
cd scars-of-leetcode
pip install pre-commit
pre-commit install
# (Optional) Install other dependencies as needed
```

---


## What is This?

Scars of LeetCode is an automation-driven workflow for mastering LeetCode problems, generating high-quality spaced-repetition flashcards, and tracking your progress. It is designed for power users who want:

- Effortless problem management and documentation
- Automated, evidence-based Anki flashcard generation
- Seamless integration with Anki (including WSL support)
- A single source of truth for all your LeetCode learning

---



## Usage

### 1. Add a New Problem

Use the `new-problem.sh` script to scaffold a new problem:

```sh
./new-problem.sh <problem_number> <problem_slug> <neetcode_150>
# Example:
./new-problem.sh 21 merge-two-sorted-lists true
```

- `<problem_number>`: The LeetCode problem number (e.g., 21)
- `<problem_slug>`: The LeetCode slug (e.g., merge-two-sorted-lists)
- `<neetcode_150>`: 'true' if part of NeetCode 150, else 'false'

This creates a folder under `problems/` with:
- A ready-to-edit `README.md` (with all required sections)
- A starter `solution.py`
- Automatic update of the main tracker in `problems/README.md`

### 2. Document and Solve

Edit the generated `README.md` and `solution.py` for your problem. Follow the template for concise, memory-friendly notes. The tracker will always reflect your current progress.

### 3. Generate and Import Anki Flashcards

For each problem, generate a `cards.json` (using the provided prompt and your README/solution). Place it in the problem's folder.

To merge all cards and import them into Anki:

```sh
python3 scripts/create_import_anki_flashcards.py
```

---

---


## Advanced: Automated Flashcard Generation


### 3. Use the Prompts for Consistent, High-Quality Notes & Cards

Prompts in `prompts/` ensure your documentation and flashcards are world-class:

- **`autofill-problem-readme.txt`**: Guidance for writing the perfect problem README, focusing on intuition, approach, complexity, and key notes. Use this as a reference or with LLMs to auto-generate your README.
- **`create-update-anki-json.txt`**: The gold standard for generating Anki flashcards from your README and solution. Cards are designed for active recall, cloze deletions, and spaced repetition. Use this prompt with LLMs to generate a `cards.json` for each problem.


### 4. Generate and Merge Anki Flashcards

For each problem, generate a `cards.json` (using the above prompt and your README/solution). Place it in the problem's folder.

To merge all cards and import them into Anki:

```bash
python3 scripts/create_import_anki_flashcards.py
```

This script will:
- Merge all `cards.json` files into a master deck (`anki/scars-of-leetcode.json`)
- Prevent duplicate cards
- Add the `NeetCode150` tag automatically if the problem is part of NeetCode 150
- Import all cards into your Anki deck via AnkiConnect

---


## AnkiConnect Setup (WSL & Linux)

**Prerequisite:** You must have the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed in your Anki desktop app.

**For WSL users:**
1. Open Anki on Windows.
2. Go to `Tools` → `Add-ons` → select AnkiConnect → `Config`.
3. Change the config to:
   ```json
   { "webBindAddress": "0.0.0.0" }
   ```
4. Restart Anki.

This allows the Python script in WSL to connect to Anki running on Windows.

---



## File/Folder Structure

- `problems/` — Each problem gets its own folder with `README.md`, `solution.py`, and `cards.json`
- `scripts/create_import_anki_flashcards.py` — Merges and imports all flashcards into Anki
- `anki/scars-of-leetcode.json` — Master deck (auto-generated)
- `prompts/` — LLM prompts for README and flashcard generation
- `new-problem.sh` — Script to scaffold new problems and update the tracker

---




## Best Practices

- Always use the provided prompts for README and flashcard generation for consistency and quality.
- Run the Python script regularly to keep your Anki deck up to date.
- Use the NeetCode 150 flag accurately for tagging and filtering.
- Review the generated tracker in `problems/README.md` for your progress overview.

---



## Code Quality: pre-commit Hooks

This repository uses [pre-commit](https://pre-commit.com/) to ensure code quality, security, and documentation standards. Hooks are run automatically before every commit to help you ship your best work!

**Checks include:**
- Python formatting with [Black](https://github.com/psf/black)
- Linting and autofix with [Ruff](https://github.com/astral-sh/ruff)
- Security scanning with [Bandit](https://github.com/PyCQA/bandit) and [Gitleaks](https://github.com/gitleaks/gitleaks) (detects secrets!)
- Markdown linting for `README.md` and docs
- YAML, JSON, and whitespace checks
- Various best-practice and safety checks

**Setup:**
1. Install pre-commit (once):
   ```sh
   pip install pre-commit
   ```
2. Install the hooks:
   ```sh
   pre-commit install
   ```
3. (Optional) Run on all files:
   ```sh
   pre-commit run --all-files
   ```

See `.pre-commit-config.yaml` for details and customization.

---




## Contributing & Support

Contributions, suggestions, and improvements are welcome! Please open an issue or PR. By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---



## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---

## Citation

If you use or reference this project in your research, blog, or elsewhere, please cite it as:

```
scarowar, "Scars of LeetCode", GitHub, https://github.com/scarowar/scars-of-leetcode
```

---

## Community & Support

- Open an [issue](https://github.com/scarowar/scars-of-leetcode/issues) for help, suggestions, or bug reports
- See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved
- Please review our [Code of Conduct](CODE_OF_CONDUCT.md) and [Security Policy](SECURITY.md)


This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

---


**Happy grinding — and may your scars become your strength!**
