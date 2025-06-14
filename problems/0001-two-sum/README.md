# Problem 0001: Two Sum

## Link
https://leetcode.com/problems/two-sum/

## Intuition
Use a hashmap to instantly find if the complement of the current number has already been seen.

## Approach
Iterate through the array, storing each number's index in a hashmap; for each number, check if its complement (target - num) exists in the hashmap.

## Complexity
- Time: O(n)
- Space: O(n)

## Notes
- Hashmap enables constant-time lookups for complements.
- Return indices as soon as a valid pair is found.
- Only one valid answer exists per input; no need to check further after a match.
- Handles duplicates and negative numbers.

NeetCode 150: true
