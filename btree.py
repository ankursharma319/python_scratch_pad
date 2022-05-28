
class Node:
    def __init__(self, keys=[], values=[], children=[], parent=None) -> None:
        self.keys = keys
        self.values = values
        self.children = children
        self.parent = parent

    def to_string(self):
        res = ""
        for key in self.keys:
            res += f"{key}, "
        res = res[:]
        res += f"[{res}]"
        return res

class BTree:
    def __init__(self, order=2):
        self.order = order
        self.root = None

    def insert(self, key, value):
        if self.root is None:
            self.root = Node([key], [value])
        return
 
    def to_string(self):
        res = self.root.to_string()
        for child in self.root.children:
            res += f"\n{child.to_string()}"
        return res
