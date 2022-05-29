import btree

# def test_btree_insert():
#     tree = btree.BTree(order=3)
#     tree.insert(10, "ran")
#     tree.insert(20, "random")
#     tree.insert(30, "value")
#     tree.insert(40, True)
#     assert tree.to_string() == """
# [20]
# [10] [30 40]
# """
#     tree.insert(50, 34)
#     tree.insert(35, 2.345)
#     assert tree.to_string() == """
# [20 40]
# [10] [30 35] [50]
# """

def test_btree_dfs_visit():
	tree = btree.BTree(order=3)
	tree.insert(10, "ran")
	tree.insert(20, "random")
	tree.insert(30, "value")
	tree.insert(40, True)
	tree.insert(50, 34)
	tree.insert(35, 2.345)
	assert [10, 20, 30, 35, 40, 50] == tree.dfs_visit_in_order()

def test_btree_bfs_visit():
	tree = btree.BTree(order=3)
	tree.insert(10, "ran")
	tree.insert(20, "random")
	tree.insert(30, "value")
	tree.insert(40, True)
	tree.insert(50, 34)
	tree.insert(35, 2.345)
	assert [20, 40, 10, 30, 35, 50] == tree.bfs_visit()
