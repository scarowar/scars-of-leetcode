from typing import *


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode()

        dummy.next = head
        p1 = dummy

        for _ in range(n + 1):
            p1 = p1.next

        p2 = dummy

        while p1:
            p2 = p2.next
            p1 = p1.next

        p2.next = p2.next.next

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
    list1 = build_list([1, 2, 3, 4, 5])
    list2 = build_list([1])
    answer_one = s.removeNthFromEnd(list1, 2)
    answer_two = s.removeNthFromEnd(list2, 1)
    print(to_list(answer_one))  # Expected: [1,2,3,5]
    print(to_list(answer_two))  # Expected: []
