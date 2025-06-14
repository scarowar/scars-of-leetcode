from typing import *


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        fast, slow = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False


if __name__ == "__main__":

    def build_list_with_cycle(arr, pos):
        dummy = ListNode(0)
        curr = dummy
        nodes = []
        for v in arr:
            curr.next = ListNode(v)
            curr = curr.next
            nodes.append(curr)
        if pos != -1 and nodes:
            curr.next = nodes[pos]
        return dummy.next

    s = Solution()
    head1 = build_list_with_cycle([3, 2, 0, -4], 1)
    print(s.hasCycle(head1))  # Expected: True
    head2 = build_list_with_cycle([1, 2], 0)
    print(s.hasCycle(head2))  # Expected: True
    head3 = build_list_with_cycle([1], -1)
    print(s.hasCycle(head3))  # Expected: False
