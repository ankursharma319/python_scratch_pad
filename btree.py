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

    def space_left(self):
        self.verify_constraints()
        return self.max_capacity - len(self.keys)

    def simple_insert(self, key, value):
        assert self.space_left()
        assert not self.children
        for i in range(0, len(self.keys)):
            key_left = self.keys[i]
            assert key != key_left
            if key < key_left:
                self.keys.insert(i, key)
                self.values.insert(i, value)
                return self
        assert key > self.keys[-1]
        self.keys.append(key)
        self.values.append(value)
        return self

    def to_string(self):
        res = ""
        for key in self.keys:
            res += f"{key}, "
        res = res[:]
        res += f"[{res}]"
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

    def insert(self, key, value):
        if self.root is None:
            self.root = Node([key], [value], max_capacity=self.order-1)
            return self.root
        current_node = self.root
        while True:
            if not current_node.children and current_node.space_left():
                print("Doing a simple insert in to the node")
                return current_node.simple_insert(key, value)
            if not current_node.children and not current_node.space_left():
                print("Need to do a split")
                return self._split_insert(current_node, key, value)
            assert current_node.children
            if key < current_node.keys[0]:
                current_node = current_node.children[0]
                continue
            if key > current_node.keys[-1]:
                current_node = current_node.children[-1]
                continue
            for i in range(1, len(current_node.keys)):
                key_left = current_node.keys[i]
                key_right = current_node.keys[i-1]
                assert key_left != key_right
                assert key != key_left
                assert key != key_right
                if key < key_right and key > key_left:
                    current_node = current_node.children[i]
                    break
        raise RuntimeError("Unreachable code")
    
    def dfs_visit_in_order(self):
        if not self.root:
            return None
        return self.root.dfs_visit_in_order()

    def bfs_visit(self):
        res = []
        return res

    def _split_insert(self, node, key, value, new_right_child=None):
        keys_to_split = []
        values_to_split = []
        children_to_split = []
        insertion_index = -1
        for i in range(len(node.keys)):
            if (key < node.keys[i]):
                insertion_index = i
                break
        keys_to_split =  copy.copy(node.keys)
        keys_to_split.insert(insertion_index, key)
        values_to_split = copy.copy(node.values)
        values_to_split.insert(insertion_index, value)
        children_to_split.extend(node.children)

        assert bool(children_to_split) == bool(new_right_child is not None)
        if new_right_child is not None:
            insertion_index_for_child = -1 if insertion_index == -1 else insertion_index + 1
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

        if node.parent and node.parent.space_left():
            return node.simple_insert(key=key, value=value)
        elif node.parent is None:
            self.root = Node(
                keys=[middle_key], values=[middle_value],
                children=[node, right_node], parent=None,
                max_capacity=self.order - 1
            )
            right_node.parent = self.root
            node.parent = self.root
            return self.root
        else:
            return self._split_insert(node=node.parent, key=middle_key, value=middle_value, new_right_child=right_node)
