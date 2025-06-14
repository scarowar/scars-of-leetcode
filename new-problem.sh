#!/bin/bash
set -euo pipefail

usage() {
  echo "Usage: $0 <problem_number> <problem_slug> <neetcode_150>"
  echo "  <neetcode_150> should be 'true' or 'false'"
  exit 1
}

if [ "$#" -ne 3 ]; then
  usage
fi

NUM_RAW="$1"
SLUG="$2"
NEETCODE_150="$3"

# Validate problem number
if ! [[ "$NUM_RAW" =~ ^[0-9]+$ ]]; then
  echo "Error: problem_number must be a positive integer."
  exit 1
fi

# Validate slug (simple check: lowercase, digits, hyphens)
if ! [[ "$SLUG" =~ ^[a-z0-9-]+$ ]]; then
  echo "Error: problem_slug must contain only lowercase letters, digits, and hyphens."
  exit 1
fi

# Validate neetcode_150 boolean
if ! [[ "$NEETCODE_150" =~ ^(true|false)$ ]]; then
  echo "Error: neetcode_150 must be 'true' or 'false'."
  exit 1
fi

# Pad problem number to 4 digits
NUM=$(printf "%04d" "$NUM_RAW")

# Convert slug to title case with spaces
title_case() {
  echo "$1" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1'
}
TITLE=$(title_case "$SLUG")

DIR="problems/${NUM}-${SLUG}"

if [ -d "$DIR" ]; then
  echo "Problem folder '$DIR' already exists!"
  exit 1
fi

mkdir -p "$DIR"

cat > "$DIR/README.md" <<EOF
# Problem $NUM: $TITLE

## Link
https://leetcode.com/problems/${SLUG}/

## Intuition
<!-- Describe your first thoughts on how to solve this problem. -->

## Approach
<!-- Describe your approach to solving the problem. -->

## Complexity
- Time complexity:
<!-- Add your time complexity here. -->

- Space complexity:
<!-- Add your space complexity here. -->

## Notes
<!-- Any alternate solutions, tricky details, edge cases, or key points to remember. -->

NeetCode 150: $NEETCODE_150

EOF

cat > "$DIR/solution.py" <<EOF
from typing import *

class Solution:
    def function_name(self, *args) -> Any:
        # Implement your solution here
        pass

if __name__ == "__main__":
    s = Solution()
    print(s.function_name(...))  # Replace with test inputs
EOF

echo "Created new problem folder: $DIR"
echo "Edit solution.py and README.md to add your code and notes."

# --- Update tracker ---

TRACKER="problems/README.md"
TEMP_TRACKER="$(mktemp)"

{
  echo "# Scars of LeetCode - Problem Tracker"
  echo
  echo "| Number | Title | NeetCode 150 | Link | Folder |"
  echo "| ------ | ----- | ------------ | ---- | ------ |"

  # List all problem folders, extract number, slug and neetcode_150 from README
  find problems -mindepth 1 -maxdepth 1 -type d | while read -r folder; do
    base=$(basename "$folder")
    num=${base%%-*}
    slug=${base#*-}

    # Default neetcode_150 status
    nc_status="false"

    readme_file="${folder}/README.md"
    if [ -f "$readme_file" ]; then
      # Look for line "NeetCode 150: true" or "NeetCode 150: false"
      line=$(grep "^NeetCode 150:" "$readme_file" || true)
      if [[ "$line" == *true* ]]; then
        nc_status="true"
      fi
    fi

    echo "$num $slug $nc_status $folder"
  done | sort -n | while read -r num slug nc_status folder; do
    title=$(echo "$slug" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
    rel_folder="$folder"
    if [[ "$rel_folder" == problems/* ]]; then
      rel_folder="${rel_folder#problems/}"
    fi

    problem_url="https://leetcode.com/problems/${slug}/"

    echo "| $num | $title | $nc_status | [Link]($problem_url) | [$rel_folder]($rel_folder) |"
  done
} > "$TEMP_TRACKER"

mv "$TEMP_TRACKER" "$TRACKER"
