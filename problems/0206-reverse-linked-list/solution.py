from typing import *

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        
        pre, cur, nxt = None, head, head.next
        while cur:
            cur.next = pre

            pre = cur
            cur = nxt
            if nxt:
                nxt = nxt.next
        
        return pre

if __name__ == "__main__":
    def list_to_linkedlist(lst):
        dummy = ListNode()
        curr = dummy
        for val in lst:
            curr.next = ListNode(val)
            curr = curr.next
        return dummy.next

    def linkedlist_to_list(node):
        result = []
        while node:
            result.append(node.val)
            node = node.next
        return result

    s = Solution()
if __name__ == "__main__":
    s = Solution()
    for test in [[1, 2, 3, 4, 5], [1, 2], []]:
        ll = list_to_linkedlist(test)
        reversed_ll = s.reverseList(ll)
        print(linkedlist_to_list(reversed_ll))
