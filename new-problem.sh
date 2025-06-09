#!/bin/bash
set -euo pipefail

usage() {
  echo "Usage: $0 <problem_number> <problem_slug>"
  exit 1
}

if [ "$#" -ne 2 ]; then
  usage
fi

NUM_RAW="$1"
SLUG="$2"

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
<!-- Any tricky details, edge cases, or key points to remember. -->

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
  echo "| Number | Title | Folder |"
  echo "| ------ | ----- | ------ |"

  # List all problem folders, extract number and path for numeric sort
  find problems -mindepth 1 -maxdepth 1 -type d | while read -r folder; do
    base=$(basename "$folder")
    num=${base%%-*}
    echo "$num $folder"
  done | sort -n | while read -r num folder; do
    slug=${folder#*-}
    title=$(echo "$slug" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
    echo "| $num | $title | [$folder]($folder) |"
  done
} > "$TEMP_TRACKER"

mv "$TEMP_TRACKER" "$TRACKER"
