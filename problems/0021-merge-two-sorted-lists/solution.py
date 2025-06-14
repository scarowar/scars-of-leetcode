from typing import *


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        dummy = ListNode(None)
        p = dummy

        p1 = list1
        p2 = list2

        while p1 and p2:
            if p1.val < p2.val:
                p.next = p1
                p1 = p1.next
            else:
                p.next = p2
                p2 = p2.next
            p = p.next

        if p1:
            p.next = p1

        if p2:
            p.next = p2

        return dummy.next


if __name__ == "__main__":

    def build_list(arr):
        dummy = ListNode()
        curr = dummy
        for v in arr:
            curr.next = ListNode(v)
            curr = curr.next
        return dummy.next

    def to_list(node):
        res = []
        while node:
            res.append(node.val)
            node = node.next
        return res

    s = Solution()
    list1 = build_list([1, 2, 4])
    list2 = build_list([1, 3, 4])
    merged = s.mergeTwoLists(list1, list2)
    print(to_list(merged))  # Expected: [1,1,2,3,4,4]
