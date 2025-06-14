# Problem 0021: Merge Two Sorted Lists

## Link
https://leetcode.com/problems/merge-two-sorted-lists/

## Intuition
Merge by always attaching the smaller node from either list, like the merge step in merge sort.

## Approach
Use two pointers and a dummy node; link the smaller node each time, then append leftovers.

## Complexity
- Time: O(n + m), where n and m are the lengths of the lists.
- Space: O(1), in-place merge.

## Notes
- Always handle empty lists and unequal lengths.
- Dummy node simplifies head handling.
- Recursive solutions use extra stack space.

NeetCode 150: true
