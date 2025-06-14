# Problem 0019: Remove Nth Node From End Of List

## Link
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

## Intuition
Keep two pointers n+1 apart to find the node to remove in one pass.

## Approach
Use a dummy node and two pointers; move the first pointer n+1 steps ahead, then move both until the first hits the end.

## Complexity
- Time: O(n)
- Space: O(1)

## Notes
- Dummy node handles head removal cleanly.
- Works for single-node lists and when n equals list length.
- Alternative: two-pass approach by counting nodes first.

NeetCode 150: true
