from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fast, slow = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow


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
    list2 = build_list([1, 2, 3, 4, 5, 6])
    answer_one = s.middleNode(list1)
    answer_two = s.middleNode(list2)
    print(to_list(answer_one))  # Expected: [3,4,5]
    print(to_list(answer_two))  # Expected: [4,5,6]
