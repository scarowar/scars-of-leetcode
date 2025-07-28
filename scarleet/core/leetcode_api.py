import requests
import rich

from scarleet.config import config

PROBLEM_QUERY = """
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    questionFrontendId
    title
    titleSlug
    content
    isPaidOnly
    difficulty
    likes
    dislikes
    topicTags {
      name
      slug
    }
    codeSnippets {
        lang
        langSlug
        code
    }
  }
}
"""


def get_problem_details(title_slug: str) -> dict | None:
    api_url = config.get("leetcode", {}).get("api_url")
    if not api_url:
        rich.print(
            "[bold red]Error:[/bold red] 'leetcode.api_url' not set in scarleet.toml"
        )
        return None

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
    }

    try:
        response = requests.post(
            api_url,
            json={
                "query": PROBLEM_QUERY,
                "variables": {"titleSlug": title_slug.strip().lower()},
            },
            headers=headers,
            timeout=10,
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            rich.print(f"[bold red]API Request Failed:[/bold red] {e}")
            rich.print(f"[bold yellow]Response content:[/bold yellow] {response.text}")
            return None

        data = response.json()

        if "errors" in data:
            rich.print(f"[bold red]GraphQL Error:[/bold red] {data['errors']}")
            return None

        question_data = data.get("data", {}).get("question")
        if not question_data:
            return None

        formatted_data = {
            "title": question_data.get("title"),
            "frontend_id": question_data.get("questionFrontendId"),
            "difficulty": question_data.get("difficulty"),
            "tags": [tag["name"] for tag in question_data.get("topicTags", [])],
            "code_snippet": next(
                (
                    s["code"]
                    for s in question_data.get("codeSnippets", [])
                    if s["langSlug"] == "python3"
                ),
                None,
            ),
        }

        return formatted_data

    except requests.exceptions.RequestException as e:
        rich.print(f"[bold red]API Request Failed:[/bold red] {e}")
        return None
