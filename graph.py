
def separate_sets_to_adjacency_list(vertices, edges):
    if isinstance(vertices, dict):
        vertices = list(vertices.keys())
    assert isinstance(vertices, list), f"{type(vertices)}"
    assert isinstance(edges, list)
    adj_list = {}
    for v in vertices:
        adj_list[v] = []
    for e in edges:
        assert isinstance(e, tuple)
        assert len(e) == 2
        assert e[0] in vertices
        assert e[1] in vertices
        assert e[1] not in adj_list[e[0]]
        adj_list[e[0]].append(e[1])
    return adj_list

def bfs(adj_list=None):
    pass
