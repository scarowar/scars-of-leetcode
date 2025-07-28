# Scarleet CLI Installation (Local, Editable)

You can install Scarleet as a CLI tool locally, so you can run `scarleet` from anywhere on your system.

## 1. Install in Editable Mode

From the root of your project, run:

```sh
pip install --editable .
```

This will make the `scarleet` command available globally (in your environment).

## 2. Install dependencies

You can install all required dependencies for Scarleet using either:

```sh
pip install -r requirements.txt
```

or, for modern Python packaging:

```sh
pip install .
```

Both methods will set up everything needed for the CLI.

## 3. Usage

After installation, you can run:

```sh
scarleet --help
```

or any subcommand, e.g.:

```sh
scarleet new <problem-slug>
scarleet setup
scarleet docgen <problem-slug>
scarleet flashcards <problem-slug>
scarleet status
```

## 4. Uninstall

To remove the CLI:

```sh
pip uninstall scarleet
```

---

**Note:** This does not publish your package to PyPI. It only makes it available on your local machine for development and use.


## OpenAI or Azure OpenAI Usage (Optional)

Scarleet can use either OpenAI or Azure OpenAI models for flashcard and docgen generation. Set the following environment variables in a `.env` file (recommended, and git-ignored):

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
