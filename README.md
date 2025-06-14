# Scars of LeetCode

**Every Accepted was paid in blood, sweat, and runtime errors.**

> **Note:** This documentation and workflow are a work in progress. Expect ongoing improvements and refinements.

---

## What is This?

Scars of LeetCode is an automation-driven workflow for mastering LeetCode problems, generating high-quality spaced-repetition flashcards, and tracking your progress. It is designed for power users who want:

- Effortless problem management and documentation
- Automated, evidence-based Anki flashcard generation
- Seamless integration with Anki (including WSL support)
- A single source of truth for all your LeetCode learning

---

## Quick Start

### 1. Add a New Problem

Use the `new-problem.sh` script to scaffold a new problem:

```bash
./new-problem.sh <problem_number> <problem_slug> <neetcode_150>
# Example:
./new-problem.sh 21 merge-two-sorted-lists true
```

- **<problem_number>**: The LeetCode problem number (e.g., 21)
- **<problem_slug>**: The LeetCode slug (e.g., merge-two-sorted-lists)
- **<neetcode_150>**: 'true' if part of NeetCode 150, else 'false'

This creates a folder under `problems/` with:
- A ready-to-edit `README.md` (with all required sections)
- A starter `solution.py`
- Automatic update of the main tracker in `problems/README.md`

### 2. Document and Solve

Edit the generated `README.md` and `solution.py` for your problem. Follow the template for concise, memory-friendly notes. The tracker will always reflect your current progress.

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

## Contributing & Support

Contributions, suggestions, and improvements are welcome! Please open an issue or PR.

---

**Happy grinding — and may your scars become your strength.**
