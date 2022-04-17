
class Node:
    def __init__(self, prev = None, next = None, data = None) -> None:
        self.prev = prev
        self.next = next
        self.data = data
    
    def __repr__(self):
        return str(self.data)

class LinkedList:
    def __init__(self, values=[]) -> None:
        self.head = None
        self.tail = None
        self.size = 0

        if values is not None:
            self.add_multiple_nodes(values=values)
            
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.data
            node = node.next
    
    def __reversed__(self):
        node = self.tail
        while node is not None:
            yield node.data
            node = node.prev
    
    def __len__(self):
        return self.size

    def __getnode__(self, i):
        if len(self) < i or i < 0:
            raise IndexError
        node = self.head
        j = 0
        while j < i:
            node = node.next
            j += 1
        return node

    def __getitem__(self, i):
        if len(self) <= i or i < 0:
            raise IndexError
        return self.__getnode__(i).data

    def __repr__(self):
        res = "\n"
        res += "repr:\n"
        for value in self:
            res += "_________\n"
            res += "|       |\n"
            res += "|   " + str(value) + "   |\n"
            res += "|_______|\n"
            res += "    |    \n"
            res += "    v    \n"
        return res

    def backward_repr(self):
        res = "\n"
        res += "backward repr:\n"
        for value in reversed(self):
            res += "_________\n"
            res += "|       |\n"
            res += "|   " + str(value) + "   |\n"
            res += "|_______|\n"
            res += "    |    \n"
            res += "    v    \n"
        return res

    def add_multiple_nodes(self, values=[]):
        for value in values:
            self.push_back(value)

    def push_back(self, value) -> None:
        node = Node(prev=self.tail, next=None, data=value)
        if self.tail:
            self.tail.next = node
        else:
            assert self.head is None
            self.head = node
        self.tail = node
        self.size += 1

    def push_front(self, value) -> None:
        node = Node(prev=None, next=self.head, data=value)
        if self.head:
            self.head.prev = node
        else:
            assert self.tail is None
            self.tail = node
        self.head = node
        self.size += 1

    def pop_front(self):
        assert self.head is not None
        ret = self.head.data
        if self.head.next is not None:
            self.head.next.prev = None
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return ret

    def pop_back(self):
        assert self.tail is not None
        ret = self.tail.data
        if self.tail.prev is not None:
            self.tail.prev.next = None
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        self.size -= 1
        return ret

    def push_at(self, index, value):
        node = self.__getnode__(index)
        if node is None:
            # push to end
            self.push_back(value)
            return
        prev_node = node.prev
        new_node = Node(prev=prev_node, next=node, data=value)
        if prev_node is not None:
            prev_node.next = new_node
        else:
            # new_node must be the new head
            self.head = new_node
        node.prev = new_node
        self.size += 1

    def pop_at(self, index):
        node = self.__getnode__(index)
        assert node is not None
        if node == self.head:
            return self.pop_front()
        if node == self.tail:
            return self.pop_back()
        ret = node.data
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return ret
