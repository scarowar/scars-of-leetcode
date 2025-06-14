# Problem 0707: Design Linked List

## Link
https://leetcode.com/problems/design-linked-list/

## Intuition
Dummy head and tail nodes make insertions and deletions at boundaries simple and safe.

## Approach
Use a doubly linked list with dummy nodes; traverse from head to index, and use helper checks for valid positions.

## Complexity
- Time: O(1) for addAtHead/addAtTail; O(n) for get, addAtIndex, deleteAtIndex.
- Space: O(n) for n nodes.

## Notes
- Always check index bounds before operations.
- Dummy nodes prevent edge-case bugs at head/tail.
- Alternative: singly linked list is possible but less efficient for some ops.
- Handle empty list and boundary cases carefully.

NeetCode 150: false
