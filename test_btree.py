import btree

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

def test_btree_size():
	tree = btree.BTree(order=3)
	assert tree.size() == 0
	assert tree.node_count == 0
	tree.insert(10, 0)
	tree.insert(20, 0)
	assert tree.size() == 2
	assert tree.node_count == 1
	tree.insert(30, 0)
	tree.insert(40, True)
	tree.insert(50, 0)
	tree.insert(35, 0)
	assert tree.size() == 6
	assert tree.node_count == 4

def test_btree_tostring():
	tree = btree.BTree(order=3)
	tree.insert(10, 0)
	tree.insert(20, 0)
	tree.insert(30, 0)
	tree.insert(40, True)
	tree.insert(50, 0)
	tree.insert(35, 0)
	assert tree.to_string() == """[20 40]
[10] [30 35] [50]
"""
def test_btree_large():
	tree_order = 32
	tree = btree.BTree(order=tree_order)
	large_n = 100000
	for i in range(large_n):
		tree.insert(i, i)
		assert tree.size() == i+1
	print(f"printing final tree =\n{tree.to_string()}")
	assert [i for i in range(large_n)] == tree.dfs_visit_in_order()
	assert tree.node_count > tree.size() / tree_order
	assert tree.node_count < tree.size()
