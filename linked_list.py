
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
        res += self.backward_repr()
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

    def reverse(self):
        current_node = self.head
        while current_node is not None:
            old_prev = current_node.prev
            current_node.prev = current_node.next
            current_node.next = old_prev
            current_node = current_node.prev

        new_tail = self.head
        self.head = self.tail
        self.tail = new_tail

    def sort(self):
        self.head = LinkedList._merge_sort(self.head)
        self.tail = LinkedList._find_tail_node(self.head)

    @staticmethod
    def _merge_sort(left_node):
        #print(f"LinkedList._merge_sort : node length =  {LinkedList._debug_node_length(left_node)}")
        if left_node is None or left_node.next is None:
            return left_node
        right_node = LinkedList._partition_into_nodes(left_node)
        assert LinkedList._debug_node_length(left_node) - LinkedList._debug_node_length(right_node) <= 1
        assert left_node is not None
        assert right_node is not None
        left_node = LinkedList._merge_sort(left_node)
        right_node = LinkedList._merge_sort(right_node)
        assert left_node is not None
        assert right_node is not None
        return LinkedList._merge_sorted_nodes(left_node, right_node)

    @staticmethod
    def _partition_into_nodes(node):
        node_fast = node
        node_slow = node
        while node_fast is not None and node_fast.next is not None and node_fast.next.next is not None:
            node_fast = node_fast.next
            node_fast = node_fast.next
            node_slow = node_slow.next
        left_tail_node = node_slow
        right_head_node = node_slow.next

        right_head_node.prev = None
        left_tail_node.next = None

        #print(f"LinkedList._partition_into_nodes : left node length =  {LinkedList._debug_node_length(node)}")
        #print(f"LinkedList._partition_into_nodes : right node length =  {LinkedList._debug_node_length(right_head_node)}")
        return right_head_node 
    
    @staticmethod
    def _merge_sorted_nodes(node_left, node_right):
        """
        Insert from right_node into left_node, maintaining the sort
        """
        left_node = node_left
        right_node = node_right
        while left_node is not None and right_node is not None:
            if left_node.data > right_node.data:
                # insert right node before left_node
                old_right_next = right_node.next
                if left_node.prev is not None:
                    left_node.prev.next = right_node
                right_node.prev = left_node.prev
                right_node.next = left_node
                left_node.prev = right_node
                right_node = old_right_next
            else:
                # left node is already inserted, just increment
                left_tail_node = left_node
                left_node = left_node.next
        
        if right_node is not None:
            right_node.prev = left_tail_node
            left_tail_node.next = right_node
        return node_left if node_left.data < node_right.data else node_right

    @staticmethod
    def _debug_node_length(node):
        counter = 0
        x = node
        while x is not None:
            x = x.next
            counter += 1
        return counter

    @staticmethod
    def _find_tail_node(node):
        while node.next is not None:
            node = node.next
        return node

