# Problem 0217: Contains Duplicate

## Link
https://leetcode.com/problems/contains-duplicate/

## Intuition
Duplicates can be detected instantly by tracking seen numbers in a set.

## Approach
Use a set to record numbers as you iterate; return True if a number is already present.

## Complexity
- Time: O(n)
- Space: O(n)

## Notes
- One-liner: return len(nums) != len(set(nums)).
- Handles empty and single-element lists.
- Set lookup is O(1) on average.

NeetCode 150: true
