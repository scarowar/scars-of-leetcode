# Problem 0876: Middle Of The Linked List

## Link
https://leetcode.com/problems/middle-of-the-linked-list/

## Intuition
Fast and slow pointers let you find the middle in one pass.

## Approach
Start both pointers at head; move fast by two and slow by one until fast reaches the end, then return slow.

## Complexity
- Time: O(n)
- Space: O(1)

## Notes
- For even length, returns the second middle node.
- Handles empty and single-node lists.
- Alternate: count nodes, then index to middle.

NeetCode 150: false
