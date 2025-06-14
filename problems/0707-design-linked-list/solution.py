from typing import *

class Node:
    def __init__(self, x):
        self.val = x
        self.next = None
        self.prev = None

class MyLinkedList:

    def __init__(self):
        self.head = Node(None)
        self.tail = Node(None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def get(self, index: int) -> int:
        if not self.checkElementAtIndex(index):
            return -1
        
        p = self.getNode(index)
        
        return p.val

    def addAtHead(self, val: int) -> None:
        temp = self.head.next
        x = Node(val)
        
        self.head.next = x
        x.prev = self.head
        
        x.next = temp
        temp.prev = x
        
        self.size += 1

    def addAtTail(self, val: int) -> None:
        temp = self.tail.prev
        x = Node(val)
        
        temp.next = x
        x.prev = temp
        
        x.next = self.tail
        self.tail.prev = x
        
        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if not self.checkPositionAtIndex(index):
            return

        if index == self.size:
            self.addAtTail(val)
            return

        p = self.getNode(index)
        temp = p.prev
        
        x = Node(val)
        
        temp.next = x
        x.prev = temp
        
        x.next = p
        p.prev = x
        
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if self.size == 0:
            return

        if not self.checkElementAtIndex(index):
            return
        
        p = self.getNode(index)
        
        prev = p.prev
        next = p.next
        
        prev.next = next
        next.prev = prev
        
        self.size -= 1
    
    # utils
    def checkElementAtIndex(self, index):
        return 0 <= index < self.size
    
    def checkPositionAtIndex(self,index):
        return 0 <= index <= self.size
    
    def getNode(self, index):
        x = self.head.next
        
        for _ in range(index):
            x = x.next
        
        return x

if __name__ == "__main__":
    obj = MyLinkedList()
    obj.addAtHead(1)
    obj.addAtTail(3)
    obj.addAtIndex(1, 2)
    print(obj.get(1))
    obj.deleteAtIndex(1)
    print(obj.get(1))
