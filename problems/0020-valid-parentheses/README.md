# Problem 0020: Valid Parentheses

## Link
https://leetcode.com/problems/valid-parentheses/

## Intuition
Use a stack to ensure every opening bracket has a matching closing bracket in the correct order.

## Approach
Iterate through the string, pushing opening brackets onto a stack and popping to match each closing bracket; return false if a mismatch or leftover remains.

## Complexity
- Time: O(n)
- Space: O(n)

## Notes
- Handle cases where the string starts with a closing bracket or ends with unmatched openings.
- Use a helper function to map each closing bracket to its corresponding opening bracket.
- Works for all three bracket types: (), {}, [].
- Returns false immediately on any mismatch or if the stack is not empty at the end.
