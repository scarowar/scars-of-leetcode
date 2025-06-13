# Problem 0021: Merge Two Sorted Lists

## Link
https://leetcode.com/problems/merge-two-sorted-lists/

## Intuition
Use two pointers to traverse both lists, always attaching the smaller node to the merged list, similar to the merge step in merge sort.

## Approach
Iterate through both lists with pointers, linking the smaller node to a dummy node's next, and append any remaining nodes at the end.

## Complexity
- Time complexity: O(n + m), where n and m are the lengths of the two lists.
- Space complexity: O(1), as merging is done in-place without extra data structures.

## Notes
Recursive solutions are common but use extra stack space; always handle empty lists and lists of different lengths.

