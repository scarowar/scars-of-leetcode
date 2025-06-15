# Problem 1: Two Sum

## Link
- [Two Sum](https://leetcode.com/problems/two-sum/)

## Intuition
By using a hash map to store previously seen numbers and their indices, we can efficiently check if the complement (target - current number) exists.

## Approach
Iterate through the list, calculate the complement for each number, check if the complement is already in the hash map, and if so, return the indices; otherwise, store the current number and its index in the hash map.

## Complexity
- Time: `O(n)`
- Space: `O(n)`

## Notes
- Utilizes a hash map for constant time look-ups.
- Returns indices as soon as the pair is found, ensuring only one valid pair is returned.
- Handles edge cases where no valid pair exists by implicit assumption that input guarantees a solution.
