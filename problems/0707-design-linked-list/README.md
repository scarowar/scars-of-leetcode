# Problem 0707: Design Linked List

## Link
https://leetcode.com/problems/design-linked-list/

## Intuition
Use a doubly linked list with dummy head and tail nodes to simplify edge operations and enable O(1) insertions/deletions at both ends.

## Approach
Maintain a size counter and traverse from head to locate nodes; use helper functions to check index validity and perform operations efficiently.

## Complexity
- Time complexity: O(1) for addAtHead/addAtTail; O(n) for get, addAtIndex, and deleteAtIndex due to traversal.
- Space complexity: O(n) for storing n nodes in the linked list.

## Notes
Alternative: use a singly linked list; always check for invalid indices and handle empty list or boundary insertions/deletions carefully.

