
import os

def run_day_01():
    sums = []
    with open('./input01.txt') as f:
        current_sum = 0
        for line in f:
            if line == "\n":
                sums.append(current_sum)
                current_sum = 0
            else:
                current_sum += int(line.strip())
    print(sums)
    total_sum = 0
    for i in range(3):
        total_sum += sums.pop(sums.index(max(sums)))
    print(total_sum)

def run_day_02():
    mappings = {"A":"rock", "B":"paper", "C":"scissors"}
    static_scores = {"rock":1, "paper":2, "scissors":3}
    result_mappings = {"X":"loss", "Y":"draw", "Z":"win"}
    result_scores = {"win":6, "draw":3, "loss":0}
    with open('./input02.txt') as f:
        total_score = 0
        for line in f:
            arr = line.rstrip().split(" ")
            target_result = result_mappings[arr[1]]
            opp = mappings[arr[0]]
            me = "None"
            score = result_scores[target_result]
            if (target_result == "draw"):
                me = opp
            elif (target_result == "win"):
                if (opp == "rock"):
                    me = "paper"
                elif opp == "paper":
                    me = "scissors"
                elif opp == "scissors":
                    me = "rock"
            else:
                if (opp == "rock"):
                    me = "scissors"
                elif opp == "paper":
                    me = "rock"
                elif opp == "scissors":
                    me = "paper"
            score += static_scores[me]
            total_score += score
    print(total_score)

def _find_common_char(strings):
    assert len(strings) == 3
    sets = []
    for string in strings:
        set_current = set()
        for c in string:
            set_current.add(c)
        sets.append(set_current)
    assert len(sets) == 3
    print(f"strings={strings}")
    print(f"sets={sets}")
    intersection_set = set.intersection(*sets)
    print(f"intersection_set={intersection_set}")
    assert len(intersection_set) == 1
    return intersection_set.pop()

def _get_priority(c):
    assert len(c) == 1
    if ord(c) >= ord('a') and ord(c) <= ord('z'):
        return ord(c)-ord('a')+1
    if ord(c) >= ord('A') and ord(c) <= ord('Z'):
        return ord(c)-ord('A')+27
    assert False

def run_day_03():
    with open('./input03.txt') as f:
        i = 0
        total_priority = 0
        current_lines = []
        for line in f:
            if (i % 3 == 0):
                current_lines = []
            current_lines.append(line.rstrip())
            i+=1
            if len(current_lines) != 3:
                continue
            c = _find_common_char(current_lines)
            total_priority+= _get_priority(c)
        print(f"total_priority = {total_priority}")

def _fully_contains(range_a, range_b):
    if (range_a[0] < range_b[0]):
        return range_a[1] >= range_b[1]
    if (range_a[0] > range_b[0]):
        return range_a[1] <= range_b[1]
    return True

def _any_overlap(range_a, range_b):
    assert range_a[0] <= range_a[1]
    assert range_b[0] <= range_b[1]
    if range_a[0] < range_b[0]:
        return not range_a[1] < range_b[0]
    if range_a[0] > range_b[0]:
        return not range_b[1] < range_a[0]
    return True

def run_day_04():
    with open('./input04.txt') as f:
        fully_contained_count = 0
        any_overlap_count = 0
        for line in f:
            sides = line.rstrip().split(",")
            assert len(sides) == 2
            left_range = [int(x) for x in sides[0].split("-")]
            right_range = [int(x) for x in sides[1].split("-")]
            assert len(left_range) == 2
            assert len(right_range) == 2
            fc = _fully_contains(left_range, right_range)
            ov = _any_overlap(left_range, right_range)
            print(f"left_range={left_range}, right_range={right_range}, fully_contains={fc}, overlaps={ov}")
            if fc:
                fully_contained_count += 1
            if ov:
                any_overlap_count += 1
        print(f"fully_contained_count = {fully_contained_count}")
        print(f"any_overlap_count = {any_overlap_count}")

def run_day_05():
    stacks = {}
    with open('./input05.txt') as f:
        stack_lines = []
        for line in f:
            if line == '\n':
                break
            stack_lines.append(line.rstrip("\n"))
        stack_keys = stack_lines.pop().strip().split("  ")
        print(f"stack_keys = {stack_keys}")
        for key in stack_keys:
            stacks[int(key)] = []
        print(f"stack_lines = {stack_lines}")
        for line in stack_lines[::-1]:
            splits = [line[i*4:(i+1)*4] for i in range(len(stacks))]
            print(f"splits = {splits}")
            assert len(splits) == len(stack_keys)
            for i in range(len(splits)):
                string = splits[i].strip()
                if not string:
                    continue
                assert string.startswith("[")
                assert string.endswith("]")
                char = string.lstrip("[").rstrip("]")
                stacks[int(stack_keys[i])].append(char)

    #print(f"stacks = {stacks}")
    for stack_key in stacks:
        print(f"printing stack for stack_key = {stack_key}")
        print(f"stack = {stacks[stack_key]}")

    with open('./input05.txt') as f:
        parse_actions = False
        for line in f:
            if line == '\n':
                parse_actions = True
                continue
            if not parse_actions:
                continue
            assert "move " in line
            assert " from " in line
            assert " to " in line
            first_split = line.rstrip().lstrip("move ").split(" from ")
            quantity = int(first_split[0])
            second_split = first_split[1].split(" to ")
            move_from = int(second_split[0])
            move_to = int(second_split[1])
            stacks[move_to].extend(stacks[move_from][-quantity:])
            del stacks[move_from][-quantity:]
            #print(f"quantity = {quantity}, move_from = {move_from}, move_to = {move_to}")
    
    tops = []
    for i in range(1, len(stacks)+1):
        tops.append(stacks[i].pop())
    print(f"top of each stack after running the actions = {''.join(tops)}")

def _find_start_marker(content: str, n_chars=14):
    def is_all_unique(string):
        return len(set(string)) == len(string)

    for i in range(len(content)-n_chars):
        if is_all_unique(content[i:i+n_chars]):
            return i+n_chars
    raise RuntimeError("Shouldnt reach here")

def run_day_06():
    content = ""
    with open('./input06.txt') as f:
        content = f.read()
    start_marker = _find_start_marker(content)
    print(f"start_marker = {start_marker}")

class FsNode:
    def __init__(self, is_dir, name, parent=None, size=0) -> None:
        self.is_dir = is_dir
        self.name = name
        self.parent = parent
        self.size = size
        self.accum_size = size
        self.children = []

def has_file_by_name(node: FsNode, name: str):
    matches = [x for x in node.children if (not x.is_dir) and (x.name == name)]
    assert len(matches) <= 1
    return len(matches) > 0

def has_dir_by_name(node: FsNode, name: str):
    matches = [x for x in node.children if x.is_dir and (x.name == name)]
    assert len(matches) <= 1
    return len(matches) > 0

def print_tree(root: FsNode, prefix=""):
    print(f"{prefix}{'d' if root.is_dir else 'f'} - {root.name}")
    for child in root.children:
        #print(f"child = {child.name}")
        print_tree(child, prefix=f"     {prefix}")

def get_accum_size(node):
    size = 0
    for child in node.children:
        size += child.size
    pass

def populate_accum_size(root_node):
    for child in root_node.children:
        root_node.accum_size += child.size
        if child.is_dir:
            populate_accum_size(child)
            root_node.accum_size += child.accum_size

def get_dirs_list(root_node):
    dirs = [root_node]
    for child in root_node.children:
        if child.is_dir:
            dirs += get_dirs_list(child)
    return dirs

def run_day_07():
    root_node = FsNode(is_dir=True, name="/")
    current_node = None
    with open('./input07.txt') as f:
        for line in f:
            line = line.rstrip()
            #print(f"line={line}")
            if line.startswith("$"):
                line = line[1:].lstrip()
                if line.startswith("cd"):
                    #print("cd command")
                    splits = line.split(" ")
                    assert len(splits) == 2
                    assert splits[0] == "cd"
                    cd_dir = splits[1]
                    if cd_dir == "/":
                        current_node = root_node
                    elif cd_dir == "..":
                        current_node = current_node.parent
                        assert current_node
                    else:
                        matches = [x for x in current_node.children if (x.is_dir and (x.name == cd_dir))]
                        assert len(matches) == 1, f"{len(matches)}==1"
                        current_node = matches[0]
                    #print(f"now the current node is {current_node.name}")
                else:
                    assert line == "ls"
                    #print("ls command")
                continue
            if not line.startswith("dir"):
                splits = line.split(" ")
                assert len(splits) == 2
                size = int(splits[0])
                file_name = splits[1]
                assert not has_file_by_name(current_node, file_name)
                #print(f"adding file by name {file_name} to {current_node.name}")
                current_node.children.append(FsNode(is_dir=False, name=file_name, parent=current_node, size=size))
            else:
                splits = line.split(" ")
                assert len(splits) == 2
                assert splits[0] == "dir"
                dir_name = splits[1]
                assert not has_dir_by_name(current_node, dir_name)
                #print(f"adding dir by name {dir_name} to {current_node.name}")
                current_node.children.append(FsNode(is_dir=True, name=dir_name, parent=current_node))

    populate_accum_size(root_node)
    print("printing parsed tree")
    print_tree(root_node)
    dirs_list = get_dirs_list(root_node=root_node)
    for dir_node in dirs_list:
        print(f"dir by name {dir_node.name} has accum_size {dir_node.accum_size}")
    dirs_list_sizes = [x.accum_size for x in dirs_list if x.accum_size < 100000]
    print(f"dirs_list_sizes = {dirs_list_sizes}")

    answer_1 = sum(dirs_list_sizes)
    print(f"answer_1 = {answer_1}")

    space_to_be_reclaimed = root_node.accum_size - 40000000
    dirs_list_sizes_all = [x.accum_size for x in dirs_list]
    dirs_list_sizes_all = sorted(dirs_list_sizes_all)
    print(f"space_to_be_reclaimed = {space_to_be_reclaimed}")
    print(f"dirs_list_sizes_all = {dirs_list_sizes_all}")
    for x in dirs_list_sizes_all:
        if x > space_to_be_reclaimed:
            print(f"answer_2 = {x}")
            break
