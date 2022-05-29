import math
import copy

class Node:
    def __init__(self, keys=[], values=[], children=[], parent=None, max_capacity=1) -> None:
        self.keys = keys
        self.values = values
        self.children = children
        self.parent = parent
        self.max_capacity = max_capacity
        self.verify_constraints()

    def verify_constraints(self):
        assert len(self.keys) == len(self.values)
        assert len(self.keys) <= self.max_capacity
        if len(self.children) != 0:
            assert len(self.children) == len(self.keys) + 1
        if self.parent is not None:
            assert len(self.keys) >= math.ceil(self.max_capacity/2)
        for child in self.children:
            assert child is not None
        prev_key = self.keys[0]
        for i in range(1, len(self.keys)):
            key = self.keys[i]
            assert key > prev_key
            prev_key = key

    def space_left(self):
        self.verify_constraints()
        return self.max_capacity - len(self.keys)

    def simple_insert(self, key, value, right_child=None):
        assert self.space_left()
        self.verify_constraints()
        if len(self.children) > 0:
            assert right_child is not None
        else:
            assert right_child is None
        for i in range(0, len(self.keys)):
            key_left = self.keys[i]
            assert key != key_left
            if key < key_left:
                self.keys.insert(i, key)
                self.values.insert(i, value)
                if right_child is not None:
                    self.children.insert(i+1, right_child)
                    right_child.parent = self
                self.verify_constraints()
                return self
        assert key > self.keys[-1]
        self.keys.append(key)
        self.values.append(value)
        if right_child is not None:
            self.children.append(right_child)
            right_child.parent = self
        self.verify_constraints()
        return self

    def to_string(self):
        self.verify_constraints()
        res = ""
        for key in self.keys:
            res += f"{key}, "
        res = f"[{res}]"
        return res
    
    def dfs_visit_in_order(self):
        self.verify_constraints()
        result = []
        for i in range(0, len(self.keys)):
            if len(self.children) > 0:
                result.extend(self.children[i].dfs_visit_in_order())
            result.append(self.keys[i])
        if len(self.children) > 0:
            result.extend(self.children[-1].dfs_visit_in_order())
        return result

class BTree:
    def __init__(self, order=2):
        assert order > 1
        self.order = order
        self.root = None
        self.element_count = 0
        self.node_count = 0

    def size(self):
        return self.element_count

    def insert(self, key, value):
        if self.root is None:
            print(f"Creating a root node of key {key}")
            self.root = Node([key], [value], max_capacity=self.order-1)
            self.element_count = 1
            self.node_count = 1
            return self.root
        current_node = self.root
        i = 0
        while True:
            print(f"Iteration #{i} of while loop in insert to find correct insert position")
            i+=1
            print(f"current_node = {current_node.to_string()}")
            if not current_node.children and current_node.space_left():
                print(f"Doing a simple insert of key {key} in to the node {current_node.to_string()}")
                self.element_count += 1
                return current_node.simple_insert(key, value)
            if not current_node.children and not current_node.space_left():
                print(f"Need to do a split insert of key {key} in to node {current_node.to_string()}")
                self.element_count += 1
                return self._split_insert(current_node, key, value)
            print(f"Trying to move down to a leaf node so that we can insert key {key}")
            assert len(current_node.children) > 0
            if key > current_node.keys[-1]:
                print("Moving to right most child")
                current_node.verify_constraints()
                current_node = current_node.children[-1]
                continue
            for i in range(0, len(current_node.keys)):
                key_left = current_node.keys[i]
                assert key_left != key
                if key < key_left:
                    current_node = current_node.children[i]
                    print(f"Moving to child at {i}th position")
                    break
        raise RuntimeError("Unreachable code")
    
    def dfs_visit_in_order(self):
        if not self.root:
            return None
        return self.root.dfs_visit_in_order()

    def bfs_visit(self):
        if self.root is None:
            return []
        visited = []
        queue = [self.root]
        while len(queue) > 0:
            node = queue.pop(0)
            visited.extend(node.keys)
            queue.extend(node.children)
        return visited

    def _split_insert(self, node, key, value, new_right_child=None):
        print(f"Doing a split insert of key {key} in to the node {node.to_string()}")
        self.node_count += 1
        keys_to_split = []
        values_to_split = []
        children_to_split = []
        insertion_index = -1
        for i in range(len(node.keys)):
            if (key < node.keys[i]):
                insertion_index = i
                break
        if insertion_index == -1:
            insertion_index = len(node.keys)
        keys_to_split =  copy.copy(node.keys)
        keys_to_split.insert(insertion_index, key)
        values_to_split = copy.copy(node.values)
        values_to_split.insert(insertion_index, value)
        children_to_split.extend(node.children)

        assert bool(children_to_split) == bool(new_right_child is not None)
        if new_right_child is not None:
            insertion_index_for_child = insertion_index + 1
            children_to_split.insert(insertion_index_for_child, new_right_child)

        middle_index = len(keys_to_split)//2
        left_keys = keys_to_split[0:middle_index]
        middle_key = keys_to_split[middle_index]
        right_keys = keys_to_split[middle_index+1:]
        left_values = values_to_split[0:middle_index]
        middle_value = values_to_split[middle_index]
        right_values = values_to_split[middle_index+1:]

        left_children = []
        right_children = []
        if new_right_child is not None:
            left_children = children_to_split[0:middle_index+1]
            right_children = children_to_split[middle_index+1:]
            assert len(left_children) == len(left_keys) + 1
            assert len(right_children) == len(right_keys) + 1
            assert len(children_to_split) == self.order + 1

        assert len(left_keys) - len(right_keys) <= 1
        assert middle_key not in left_keys
        assert middle_key not in right_keys
        assert len(left_keys) + len(right_keys) + 1 == len(keys_to_split)
        assert len(keys_to_split) == self.order
        assert len(values_to_split) == len(keys_to_split)

        right_node = Node(
            keys=right_keys, values=right_values,
            children=right_children, parent=node.parent,
            max_capacity=self.order-1
        )
        node.keys = left_keys
        node.values = left_values
        node.children = left_children

        print(f"insertion_index = {insertion_index}")
        print(f"keys_to_split = {keys_to_split}")
        print(f"children_to_split = {children_to_split}")
        print(f"left_keys = {left_keys}, middle_key = {middle_key}, right_keys = {right_keys}")
        print(f"left_children = {left_children}, right_children = {right_children}")
        print(f"Created a new right_node = {right_node.to_string()}")
        if node.parent is None:
            print(f"Creating a new root node with key {middle_key}")
            self.root = Node(
                keys=[middle_key], values=[middle_value],
                children=[node, right_node], parent=None,
                max_capacity=self.order - 1
            )
            right_node.parent = self.root
            node.parent = self.root
            self.node_count += 1
            return self.root
        elif node.parent.space_left():
            print(f"Doing a simple insert of key {middle_key} in to the node {node.parent.to_string()}")
            return node.parent.simple_insert(key=middle_key, value=middle_value, right_child=right_node)
        else:
            print(f"Recursively split insert into parent node {node.parent.to_string()}")
            return self._split_insert(node=node.parent, key=middle_key, value=middle_value, new_right_child=right_node)
