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

def test_depth_first_visit_example_2():
    visited_nodes, parent_dict = graph.dfs_visit(adj_list={
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
    assert visited_nodes == [1,2,8,9,3,4]
    assert parent_dict == {1:None, 2: 1, 3: 1, 8: 2, 4: 3, 9:8}

def test_depth_first_visit_iterative_example_1():
    visited_nodes, parent_dict = graph.dfs_visit_iterative(adj_list={
        1 : [2, 3],
        2 : [],
        3 : [1,4],
        4 : [],
        5 : []
    }, starting_vertex=1)
    assert visited_nodes == [1,2,3,4]
    assert parent_dict == {1:None, 2: 1, 3: 1, 4: 3}

def test_depth_first_visit_iterative_example_2():
    visited_nodes, parent_dict = graph.dfs_visit_iterative(adj_list={
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
    assert visited_nodes == [1,2,8,9,3,4]
    assert parent_dict == {1:None, 2: 1, 3: 1, 8: 2, 4: 3, 9:8}

def test_edge_classify_example_1():
    classifications = graph.edge_classify(adj_list={
        1 : [2, 3, 4],
        2 : [],
        3 : [1 ,4],
        4 : [],
        5 : [4]
    })
    assert classifications == {
        1 : {2:"tree", 3:"tree", 4: "forward"},
        2 : {},
        3 : {1:"back", 4:"tree"},
        4 : {},
        5 : {4:"cross"}
    }

def test_edge_classify_example_2():
    classifications = graph.edge_classify_single_source(adj_list={
        'a' : ['b', 'f'],
        'b' : ['c'],
        'c' : ['e', 'd'],
        'd' : ['e', 'b'],
        'e' : [],
        'f' : ['g'],
        'g' : ['l', 'h', 'm'],
        'h' : ['i', 'k', 'f'],
        'i' : ['d', 'j'],
        'j' : [],
        'k' : ['l', 'm'],
        'l' : [],
        'm' : ['i', 'h'],
    }, starting_vertex='a')
    assert classifications == {
        'a' : {'b':"tree", 'f':"tree"},
        'b' : {'c':"tree"},
        'c' : {'e':"tree", 'd':"tree"},
        'd' : {'e':"cross", 'b':"back"},
        'e' : {},
        'f' : {'g':"tree"},
        'g' : {'l':"tree", 'h':"tree", 'm':"forward"},
        'h' : {'i':"tree", 'k':"tree", 'f':"back"},
        'i' : {'d':"cross", 'j':"tree"},
        'j' : {},
        'k' : {'l':"cross", 'm':"tree"},
        'l' : {},
        'm' : {'i':"cross", 'h':"back"},
    }

def test_top_sort():
    adj_list = {
        'a' : ['b', 'f'],
        'b' : ['c'],
        'c' : ['e', 'd'],
        'd' : ['e', 'b'],
        'e' : [],
        'f' : ['g'],
        'g' : ['l', 'h', 'm'],
        'h' : ['i', 'k', 'f'],
        'i' : ['d', 'j'],
        'j' : [],
        'k' : ['l', 'm'],
        'l' : [],
        'm' : ['i', 'h'],
    }
    result = graph.top_sort(adj_list=adj_list)
    assert isinstance(result, list)
    assert len(result) == len(adj_list)
    print(f"result = {result}")
    checked = []
    for x in result:
        print(f"verifying that {x} has its dependencies already visited")
        for possible_source in adj_list:
            if x in adj_list[possible_source]:
                print(f"making sure node {x} has its dependency {possible_source} already visited ({checked})")
                assert possible_source in checked
        print(f"verified that {x} has its dependencies already visited")
        checked.append(x)
