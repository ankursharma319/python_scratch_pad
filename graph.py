
from math import inf
import random

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

def edge_classifying_recursive_dfs(
    adj_list, starting_vertex, 
    parents, visited_nodes, classes,
    starting_times, ending_times,
    current_time_step
):
    current_time_step += 1
    visited_nodes.append(starting_vertex)
    starting_times[starting_vertex] = current_time_step
    # run dfs recursively (but with more metadata recording)
    for dest in adj_list[starting_vertex]:
        if dest not in parents:
            # if move this append after the recursive call
            # then it will be deepest elements first (in the list)
            parents[dest] = starting_vertex
            classes[starting_vertex][dest] = "tree"
            ( parents, visited_nodes, classes
            , starting_times, ending_times, current_time_step
            ) = edge_classifying_recursive_dfs(
                adj_list=adj_list,
                starting_vertex=dest,
                parents=parents,
                visited_nodes=visited_nodes,
                classes=classes,
                starting_times=starting_times,
                ending_times=ending_times,
                current_time_step=current_time_step
            )
        else:
            assert dest in starting_times
            if starting_times[starting_vertex] < starting_times[dest]:
                assert dest in ending_times, f"should have already finished visiting dest completely but it is still in stack"
                classes[starting_vertex][dest] = "forward"
            elif starting_times[starting_vertex] > starting_times[dest] and dest not in ending_times:
                classes[starting_vertex][dest] = "back"
            elif starting_times[starting_vertex] > starting_times[dest] and dest in ending_times:
                classes[starting_vertex][dest] = "cross"
            else:
                assert False, f"internal logical error"

        current_time_step += 1
    current_time_step += 1
    ending_times[starting_vertex] = current_time_step
    return parents, visited_nodes, classes, starting_times, ending_times, current_time_step

def edge_classify_single_source(adj_list, starting_vertex):
    # inspiration from https://www.youtube.com/watch?v=wm6qRWGjvkA
    # and from https://www.geeksforgeeks.org/tree-back-edge-and-cross-edges-in-dfs-of-graph/
    classes = {}
    parents = {starting_vertex : None}
    visited_nodes = []
    starting_times = {}
    ending_times = {}
    current_time_step = 0
    for v in adj_list:
        classes[v] = {}
    parents, visited_nodes, classes, starting_times, ending_times, current_time_step = edge_classifying_recursive_dfs(
        adj_list=adj_list,
        starting_vertex=starting_vertex,
        parents=parents,
        visited_nodes=visited_nodes,
        classes=classes,
        starting_times=starting_times,
        ending_times=ending_times,
        current_time_step=current_time_step
    )
    return classes

def edge_classify(adj_list):
    classes = {}
    parents = {}
    visited_nodes = []
    starting_times = {}
    ending_times = {}
    current_time_step = 0
    for v in adj_list:
        classes[v] = {}
    for starting_vertex in adj_list:
        if starting_vertex not in parents:
            parents[starting_vertex] = None
            parents, visited_nodes, classes, starting_times, ending_times, current_time_step = edge_classifying_recursive_dfs(
                adj_list=adj_list,
                starting_vertex=starting_vertex,
                parents=parents,
                visited_nodes=visited_nodes,
                classes=classes,
                starting_times=starting_times,
                ending_times=ending_times,
                current_time_step=current_time_step
            )
    return classes

def dfs_visit_for_top_sort(adj_list, result, unvisited_set, starting_node):
    if isinstance(starting_node, tuple):
        starting_node = starting_node[0]
    if starting_node in unvisited_set:
        unvisited_set.remove(starting_node)
    for dest in adj_list[starting_node]:
        if isinstance(dest, tuple):
            dest = dest[0]
        if dest in unvisited_set:
            result, unvisited_set = dfs_visit_for_top_sort(
                adj_list=adj_list, result=result, unvisited_set=unvisited_set, starting_node=dest
            )
    result.append(starting_node)
    return result, unvisited_set

def top_sort(adj_list):
    result = []
    unvisited_set = set(adj_list.keys())
    while len(unvisited_set) > 0:
        unvisited_node = unvisited_set.pop()
        result, unvisited_set = dfs_visit_for_top_sort(adj_list=adj_list, result=result, unvisited_set=unvisited_set, starting_node=unvisited_node)
    return list(reversed(result))

def dag_shortest_path(adj_list, starting_vertex):
    deltas = {}
    pis = {}
    for vertex in adj_list:
        deltas[vertex] = inf
        pis[vertex] = None
    top_sorted_vertices = top_sort(adj_list=adj_list)
    index_of_starting_vertex = top_sorted_vertices.index(starting_vertex)
    top_sorted_vertices = top_sorted_vertices[index_of_starting_vertex:]
    deltas[starting_vertex] = 0
    for vertex in top_sorted_vertices:
        for (dest, weight) in adj_list[vertex]:
            if deltas[dest] > deltas[vertex] + weight:
                deltas[dest] = deltas[vertex] + weight
                pis[dest] = vertex
    return deltas, pis
