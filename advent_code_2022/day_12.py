import math
import pprint

pp = pprint.PrettyPrinter(indent=4)

def bfs(adj_list: dict, starting_vertex, end_vertex):
    parents = {starting_vertex: None,}
    levels = {starting_vertex: 0}
    frontier = [starting_vertex]
    level = 0
    answer = 0
    print(f"starting bfs from start {starting_vertex} to end {end_vertex}")
    while frontier:
        next = []
        #print(f"exploring frontier = {frontier}")
        for vertex in frontier:
            for neighbour in adj_list[vertex]:
                if neighbour not in parents:
                    next.append(neighbour)
                    parents[neighbour] = vertex
                    levels[neighbour] = level + 1
                    if neighbour == end_vertex:
                        answer = level + 1
        frontier = next
        level += 1
    return answer, parents
                

def _char_height(c):
    if c == 'S':
        return ord('a')
    if c == 'E':
        return ord('z')
    return ord(c)

def _create_adj_list(grid):
    adj_list = {}
    start_vertex = None
    end_vertex = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            current_char = _char_height(grid[i][j])
            if grid[i][j] == "S":
                assert start_vertex is None
                start_vertex = (i,j)
            if grid[i][j] == "E":
                assert end_vertex is None
                end_vertex = (i,j)

            if j != 0:
                left_char = _char_height(grid[i][j-1])
            else:
                left_char = math.inf

            if j == len(grid[i]) - 1:
                right_char = math.inf
            else:
                right_char = _char_height(grid[i][j+1])

            if i == 0:
                up_char = math.inf
            else:
                up_char = _char_height(grid[i-1][j])
            
            if i == len(grid) - 1:
                down_char = math.inf
            else:
                down_char = _char_height(grid[i+1][j])

            edges = []
            if left_char <= current_char + 1:
                edges.append((i, j-1))
            if right_char <= current_char + 1:
                edges.append((i, j+1))
            if up_char <= current_char + 1:
                edges.append((i-1, j))
            if down_char <= current_char + 1:
                edges.append((i+1, j))
            adj_list[(i,j)] = edges
    return adj_list, start_vertex, end_vertex

def run():
    grid = []
    with open("./input12.txt") as f:
        for line in f:
            arr = []
            for char in line.rstrip():
                arr.append(char)
            grid.append(arr)
    
    print(f"grid =")
    pp.pprint(grid)
    adj_list, start_vertex, end_vertex = _create_adj_list(grid=grid)
    print(f"adj_list =\n")
    pp.pprint(adj_list)
    print(f"start_vertex = {start_vertex}")
    print(f"end_vertex = {end_vertex}")

    shortest_path_length, parents = bfs(adj_list=adj_list, starting_vertex=start_vertex, end_vertex=end_vertex)
    print(f"shortest_path_length = {shortest_path_length}")

    #p = end_vertex
    #while p != start_vertex:
    #    print(f"parent of {p} = {parents[p]}")
    #    p = parents[p]

 
if __name__ == '__main__':
    run()
