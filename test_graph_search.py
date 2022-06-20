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

def test_breadth_first_search():
    graph.bfs(adj_list={
        1 : [2, 3],
        2 : [],
        3 : [1,4],
        4 : [],
    })
