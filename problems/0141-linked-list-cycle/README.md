# Problem 0141: Linked List Cycle

## Link
https://leetcode.com/problems/linked-list-cycle/

## Intuition
Use two pointers moving at different speeds to detect a cycle efficiently in a linked list.

## Approach
Initialize fast and slow pointers; move fast by two steps and slow by one, and if they ever meet, a cycle exists.

## Complexity
- Time complexity: O(n), as each node is visited at most twice.
- Space complexity: O(1), using only two pointers regardless of list size.

## Notes
Alternate: use a hash set to track visited nodes (O(n) space); always check for empty or single-node lists; Floyd's Tortoise and Hare is optimal for space.

