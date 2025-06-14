# Problem 0876: Middle Of The Linked List

## Link
https://leetcode.com/problems/middle-of-the-linked-list/

## Intuition
Use two pointers moving at different speeds to find the middle efficiently in a single pass.

## Approach
Initialize fast and slow pointers at the head; move fast by two steps and slow by one until fast reaches the end, then return slow.

## Complexity
- Time complexity: O(n), as each node is visited at most once.
- Space complexity: O(1), using only two pointers regardless of list size.

## Notes
Alternate: count nodes then index to middle; for even length, returns second middle; handles empty/one-node lists gracefully.

