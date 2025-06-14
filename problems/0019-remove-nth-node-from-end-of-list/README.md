# Problem 0019: Remove Nth Node From End Of List

## Link
https://leetcode.com/problems/remove-nth-node-from-end-of-list/

## Intuition
Use two pointers to efficiently locate the node to remove in a single pass by maintaining a fixed gap.

## Approach
Create a dummy node, advance the first pointer n+1 steps, then move both pointers until the first reaches the end; remove the target node.

## Complexity
- Time complexity: O(n), where n is the length of the list (single traversal).
- Space complexity: O(1), as only a few pointers are used.

## Notes
Alternative: calculate length in two passes; handle edge cases like removing the head or single-node lists.

