from typing import *


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class MyLinkedList:

    def __init__(self):
        self.head = Node(None)
        self.tail = self.head
        self.size = 0

    def get(self, index: int) -> int:
        if not self.checkElementIndex(index):
            return -1

        p = self.head.next
        for _ in range(index):
            p = p.next

        return p.val

    def addAtHead(self, val: int) -> None:
        x = Node(val)

        x.next = self.head.next
        self.head.next = x

        if self.size == 0:
            self.tail = x

        self.size += 1

    def addAtTail(self, val: int) -> None:
        x = Node(val)
        self.tail.next = x
        self.tail = x

        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if not self.checkPositionIndex(index):
            return

        if index == self.size:
            self.addAtTail(val)
            return

        prev = self.head

        for _ in range(index):
            prev = prev.next

        x = Node(val)

        x.next = prev.next
        prev.next = x

        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if not self.checkElementIndex(index):
            return

        prev = self.head

        for _ in range(index):
            prev = prev.next

        node_to_remove = prev.next
        prev.next = node_to_remove.next

        if index == self.size - 1:
            self.tail = prev

        self.size -= 1

        return node_to_remove.val

    # utils
    def checkElementIndex(self, index):
        return 0 <= index < self.size

    def checkPositionIndex(self, index):
        return 0 <= index <= self.size


if __name__ == "__main__":
    obj = MyLinkedList()
    obj.addAtHead(1)
    obj.addAtTail(3)
    obj.addAtIndex(1, 2)
    print(obj.get(1))
    obj.deleteAtIndex(1)
    print(obj.get(1))
