# Problem 0217: Contains Duplicate

## Link
https://leetcode.com/problems/contains-duplicate/

## Intuition
A set helps instantly spot duplicates as we scan through the list.

## Approach
Iterate through nums, returning True if a number is already in the set; otherwise, add it and continue.

## Complexity
- Time: O(n)
- Space: O(n)

## Notes
Alternative: return len(nums) != len(set(nums)); this one-liner also detects duplicates efficiently.
