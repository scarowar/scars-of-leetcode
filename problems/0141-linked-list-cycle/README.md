# Problem 0141: Linked List Cycle

## Link
https://leetcode.com/problems/linked-list-cycle/

## Intuition
Fast and slow pointers reveal a cycle if they ever meet.

## Approach
Use two pointers; move fast by two and slow by one, return True if they meet.

## Complexity
- Time: O(n)
- Space: O(1)

## Notes
- Floyd's Tortoise and Hare is optimal for space.
- Alternate: use a hash set for O(n) space.
- Always check for empty or single-node lists.

NeetCode 150: true
