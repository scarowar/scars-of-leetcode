# Problem 0206: Reverse Linked List

## Link
https://leetcode.com/problems/reverse-linked-list/

## Intuition
Reversing a linked list means making each node point to its previous node instead of the next.

## Approach
Use three pointers—previous, current, and next—to iteratively reverse the direction of each node’s pointer until the end of the list.

## Complexity
- Time: O(n)
- Space: O(1)

## Notes
- Handles empty and single-node lists without extra checks.
- Always update all pointers in each loop to avoid losing access to the rest of the list.
- The final head is the last non-null node processed.
- Common mistake: forgetting to update the next pointer before reversing the link.

NeetCode 150: true
