from math import inf
import graph

def test_separate_sets_to_adjacency_list():
    adj_list = graph.separate_sets_to_adjacency_list(
        vertices=[1, 2, 3, 4], edges=[(1,2)]
    )
    assert len(adj_list) == 4
    assert adj_list[1] == [2]
    assert adj_list[2] == []
    assert adj_list[3] == []
    assert adj_list[4] == []

    adj_list = graph.separate_sets_to_adjacency_list(
        vertices=[1, 2, 3, 4], edges=[(1,2), (2,1), (2,3), (3,4)]
    )
    assert adj_list[1] == [2]
    assert adj_list[2] == [1, 3]
    assert adj_list[3] == [4]
    assert adj_list[4] == []

    adj_list = graph.separate_sets_to_adjacency_list(
        vertices={1:"hello", 2:"world", 3:"system", 4: "universe"}, edges=[(1,2)]
    )
    assert len(adj_list) == 4
    assert adj_list[1] == [2]
    assert adj_list[2] == []
    assert adj_list[3] == []
    assert adj_list[4] == []

def test_breadth_first_visit_example_1():
    visited_nodes, parent_dict, levels = graph.bfs_visit(adj_list={
        1 : [2, 3],
        2 : [],
        3 : [1,4],
        4 : [],
        5 : []
    }, starting_vertex=1)
    assert visited_nodes == [1,2,3,4]
    assert parent_dict == {1:None, 2: 1, 3: 1, 4: 3}
    assert levels == {1:0, 2:1, 3:1, 4:2}

def test_breadth_first_visit_example_2():
    visited_nodes, parent_dict, levels = graph.bfs_visit(adj_list={
        1 : [2, 3],
        2 : [8],
        3 : [1,4],
        4 : [9],
        5 : [6, 7],
        6 : [5],
        7:  [1],
        8:  [9],
        9: []
    }, starting_vertex=1)
    assert visited_nodes == [1,2,3,8,4,9]
    assert parent_dict == {1:None, 2: 1, 3: 1, 8: 2, 4: 3, 9:8}
    assert levels == {1:0, 2:1, 3:1, 8:2, 4:2, 9:3}

def test_depth_first_visit_example_1():
    visited_nodes, parent_dict = graph.dfs_visit(adj_list={
        1 : [2, 3],
        2 : [],
        3 : [1,4],
        4 : [],
        5 : []
    }, starting_vertex=1)
    assert visited_nodes == [1,2,3,4]
    assert parent_dict == {1:None, 2: 1, 3: 1, 4: 3}
