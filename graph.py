
from math import inf
from tracemalloc import start


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

def bfs_visit(adj_list, starting_vertex):
    levels = {starting_vertex:0}
    parents = {starting_vertex: None}
    visited_nodes = []
    level_counter = 1
    frontier_queue = [starting_vertex]
    while len(frontier_queue) > 0:
        new_frontier = []
        for v in frontier_queue:
            edges = adj_list[v]
            for u in edges:
                if u not in parents:
                    parents[u] = v
                    levels[u] = level_counter
                    new_frontier.append(u)
            visited_nodes.append(v)
        level_counter += 1
        frontier_queue = new_frontier

    return (visited_nodes, parents, levels)

def dfs_visit_recursive(adj_list, starting_vertex, parents, visited_nodes):
    for dest in adj_list[starting_vertex]:
        if dest not in parents:
            # if move this append after the recursive call
            # then it will be deepest elements first (in the list)
            visited_nodes.append(dest)
            parents[dest] = starting_vertex
            visited_nodes, parents = dfs_visit_recursive(
                adj_list=adj_list,
                starting_vertex=dest,
                parents=parents,
                visited_nodes=visited_nodes
            )
    return visited_nodes, parents

def dfs_visit_iterative(adj_list, starting_vertex):
    parents = {starting_vertex: None}
    visited_nodes = []
    stack = [starting_vertex]
    while len(stack) > 0:
        v = stack.pop()
        for dest in reversed(adj_list[v]):
            if dest not in parents:
                parents[dest] = v
                stack.append(dest)
        visited_nodes.append(v)
    return visited_nodes, parents

def dfs_visit(adj_list, starting_vertex):
    parents = {starting_vertex : None}
    visited_nodes = [starting_vertex]
    return dfs_visit_recursive(
        adj_list=adj_list,
        starting_vertex=starting_vertex,
        parents = parents,
        visited_nodes= visited_nodes
    )
