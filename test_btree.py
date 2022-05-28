import btree

def test_btree_insert():
    tree = btree.BTree(order=3)
    tree.insert(10, "ran")
    tree.insert(20, "random")
    tree.insert(30, "value")
    tree.insert(40, True)
    assert tree.to_string() == """
[20]
[10] [30 40]
"""
    tree.insert(50, 34)
    tree.insert(35, 2.345)
