
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
            if line.startswith("$"):
                line = line[1:].lstrip()
                if line.startswith("cd"):
                    cd_dir = line.split(" ")[1]
                    if cd_dir == "/":
                        current_node = root_node
                    elif cd_dir == "..":
                        current_node = current_node.parent
                    else:
                        matches = [x for x in current_node.children if (x.is_dir and (x.name == cd_dir))]
                        current_node = matches[0]
                continue
            if not line.startswith("dir"):
                splits = line.split(" ")
                size = int(splits[0])
                file_name = splits[1]
                current_node.children.append(FsNode(is_dir=False, name=file_name, parent=current_node, size=size))
            else:
                dir_name = line.split(" ")[1]
                current_node.children.append(FsNode(is_dir=True, name=dir_name, parent=current_node))

    populate_accum_size(root_node)
    dirs_list = get_dirs_list(root_node=root_node)

    answer_1 = sum([x.accum_size for x in dirs_list if x.accum_size < 100000])
    print(f"answer_1 = {answer_1}")

    dirs_list_sizes_all = sorted([x.accum_size for x in dirs_list])
    for x in dirs_list_sizes_all:
        if x > root_node.accum_size - 40000000:
            print(f"answer_2 = {x}")
            break

import numpy as np

def run_day_08():
    arr = []
    with open('./input08.txt') as f:
        for line in f:
            row = []
            for i in range(len(line.rstrip())):
                row.append(int(line[i]))
            arr.append(row)
    arr = np.array(arr, dtype=np.int32)
    visibility_arr = np.zeros(arr.shape, dtype=np.int32)
    print(f"arr.shape = {arr.shape}")
    print(f"visibility_arr.shape = {visibility_arr.shape}")

    # update visibility from left
    for r in range(arr.shape[0]):
        current_max = -1
        for c in range(arr.shape[1]):
            if arr[r, c] > current_max:
                visibility_arr[r, c] = 1
            current_max = max(current_max, arr[r,c])

    print(f"visibility_arr after updating from left = \n{visibility_arr}")

    # update visibility from right
    for r in range(arr.shape[0]):
        current_max = -1
        for c in range(arr.shape[1]-1, -1, -1):
            if arr[r, c] > current_max:
                visibility_arr[r, c] = 1
            current_max = max(current_max, arr[r,c])

    print(f"visibility_arr after updating from right = \n{visibility_arr}")

    # update visibility from bottom
    for c in range(arr.shape[1]):
        current_max = -1
        for r in range(arr.shape[0]-1, -1, -1):
            if arr[r, c] > current_max:
                visibility_arr[r, c] = 1
            current_max = max(current_max, arr[r,c])
    print(f"visibility_arr after updating from bottom = \n{visibility_arr}")

    # update visibility from top
    for c in range(arr.shape[1]):
        current_max = -1
        for r in range(arr.shape[0]):
            if arr[r, c] > current_max:
                visibility_arr[r, c] = 1
            current_max = max(current_max, arr[r,c])
    
    print(f"visibility_arr after updating from top = \n{visibility_arr}")
    print(f"visible trees count = {np.sum(visibility_arr)}")

    max_visibility_score = 0
    for r in range(1, arr.shape[0]-1):
        for c in range(1, arr.shape[1]-1):
            current_tree = arr[r,c]
            left_visibility = 0
            for i in range(c-1, -1, -1):
                left_visibility += 1
                if current_tree <= arr[r,i]:
                    break
            right_visibility = 0
            for i in range(c+1, arr.shape[1]):
                right_visibility += 1
                if current_tree <= arr[r,i]:
                    break
            bottom_visibility = 0
            for i in range(r+1, arr.shape[0]):
                bottom_visibility += 1
                if current_tree <= arr[i,c]:
                    break
            top_visibility = 0
            for i in range(r-1, -1,-1):
                top_visibility += 1
                if current_tree <= arr[i,c]:
                    break
            visibility_score = left_visibility * right_visibility * bottom_visibility * top_visibility
            max_visibility_score = max(max_visibility_score, visibility_score)
    print(f"max_visibility_score = {max_visibility_score}")

def _get_updated_tail_coords(x_head, y_head, x_tail, y_tail):
    if abs(x_head - x_tail) > 1:
        assert abs(x_head - x_tail) == 2
        if (abs(y_head - y_tail) >= 1):
            # move diagonally
            if y_head > y_tail:
                y_tail += 1
            else:
                y_tail -= 1
            if x_head > x_tail:
                x_tail += 1
            else:
                x_tail -= 1
        else:
            assert (y_head == y_tail)
            # move horizontally
            if x_head > x_tail:
                x_tail += 1
            else:
                x_tail -= 1
    if abs(y_head - y_tail) > 1:
        if (abs(x_head - x_tail) >= 1):
            # move diagonally
            if y_head > y_tail:
                y_tail += 1
            else:
                y_tail -= 1
            if x_head > x_tail:
                x_tail += 1
            else:
                x_tail -= 1
        else:
            assert (x_head == x_tail)
            #move vertically
            if y_head > y_tail:
                y_tail += 1
            else:
                y_tail -= 1
    assert abs(x_tail - x_head) <= 1
    assert abs(y_tail - y_head) <= 1
    return (x_tail, y_tail)

def run_day_09():
    with open('./input09.txt') as f:
        vertices_visited = set()
        vertices_visited.add((0,0))
        coords = [(0,0)] * 10
        for line in f:
            splits = line.rstrip().split(" ")
            assert len(splits) == 2
            dir = splits[0]
            num = int(splits[1])
            for i in range(num):
                if dir == "U":
                    coords[0] = (coords[0][0], coords[0][1] + 1)
                elif dir == "D":
                    coords[0] = (coords[0][0], coords[0][1] - 1)
                elif dir == "R":
                    coords[0] = (coords[0][0] + 1, coords[0][1])
                else:
                    assert dir == "L"
                    coords[0] = (coords[0][0] - 1, coords[0][1])
                for i in range(1, len(coords)):
                    coords[i] = _get_updated_tail_coords(x_head=coords[i-1][0], y_head=coords[i-1][1], x_tail=coords[i][0], y_tail=coords[i][1])
                vertices_visited.add(coords[-1])
        print(f"number of vertices visited = {len(vertices_visited)}")

def run_day_10():
    with open('./input10.txt') as f:
        cycle_number = 1
        x_value = 1
        interesting_cycles = [41, 81, 121, 161, 201]
        crt = ""
        for i, line in enumerate(f):
            #print(f"i={i}, line={line.rstrip()}")
            if cycle_number in interesting_cycles:
                crt = crt + "\n"
            horizontal_pos = (cycle_number-1) % 40
            if abs(horizontal_pos - x_value) <= 1:
                crt = crt + "#"
            else:
                crt = crt + "."

            if line.rstrip() == "noop":
                cycle_number += 1
            else:
                splits = line.rstrip().split(" ")
                assert len(splits) == 2
                assert splits[0] == "addx"
                addx = int(splits[1])
                if (cycle_number + 1) in interesting_cycles:
                    crt = crt + "\n"
                horizontal_pos = (cycle_number) % 40
                if abs(horizontal_pos - x_value) <= 1:
                    crt = crt + "#"
                else:
                    crt = crt + "."
                x_value += addx
                cycle_number += 2

        print(f"crt =\n{crt}")

class Monkey:
    def __init__(self, items, operation, test) -> None:
        self.items = items
        self.operation = operation
        self.test = test
        self.total_items_inspected = 0
    
    def __repr__(self) -> str:
        return f"Monkey with items: {str(self.items)}"

def _parse_operation(line):
    assert line.startswith("  Operation: new = ")
    op_splits = line.split("  Operation: new = ")
    assert len(op_splits) == 2
    line = op_splits[1]
    op = lambda x: x
    if "+" in line:
        op_splits = line.split("+")
        assert len(op_splits) == 2
        op_splits = sorted(op_splits)
        assert op_splits[1].strip() == 'old'
        if op_splits[0].strip() == 'old':
            op = lambda x: x + x
        else:
            const = int(op_splits[0].strip())
            op = lambda x: x + const
    else:
        assert "*" in line
        op_splits = line.split("*")
        assert len(op_splits) == 2
        op_splits = sorted(op_splits)
        assert op_splits[1].strip() == 'old'
        if op_splits[0].strip() == 'old':
            op = lambda x: x * x
        else:
            const = int(op_splits[0].strip())
            op = lambda x: x * const
    return op

def _parse_test(lines):
    assert len(lines) == 3
    assert lines[0].startswith("  Test: divisible by ")
    divisible_by = int(lines[0].split("divisible by ")[1])
    assert lines[1].startswith("    If true: throw to monkey ")
    assert lines[2].startswith("    If false: throw to monkey ")
    success_monkey = int(lines[1].split("to monkey ")[1])
    fail_monkey = int(lines[2].split("to monkey ")[1])
    op = lambda x: success_monkey if (x%divisible_by == 0) else fail_monkey
    return op, divisible_by

def _process_monkey(monkeys: dict, id: int, lcm:int):
    monkey : Monkey = monkeys[id]
    for x in monkey.items:
        new_worry_lvl = monkey.operation(x)
        new_worry_lvl = new_worry_lvl%lcm
        to_monkey = monkey.test(new_worry_lvl)
        assert to_monkey != id
        monkeys[to_monkey].items.append(new_worry_lvl)
    monkey.total_items_inspected += len(monkey.items)
    monkey.items = []

def _run_monkey_rounds(monkeys: dict, rounds: int, lcm: int):
    current_round = 0
    while (current_round < rounds):
        current_monkey_id = 0
        while current_monkey_id < len(monkeys):
            _process_monkey(monkeys=monkeys, id=current_monkey_id, lcm=lcm)
            current_monkey_id += 1
        current_round += 1

def run_day_11():
    content = None
    with open('./input11.txt') as f:
        content = f.read()
    splits = content.split("\n\n")
    monkeys = {}
    divisible_bys = set()
    for split in splits:
        lines = split.split("\n")
        assert len(lines) == 6
        assert lines[0].startswith("Monkey ")
        id = int(lines[0].rstrip(":").split(" ")[1])
        assert lines[1].startswith("  Starting items: "), f"{lines[1]}"
        items = lines[1].split(":")[1].strip().split(",")
        items = list(map(int, items))
        op = _parse_operation(line=lines[2])
        test, divisible_by = _parse_test(lines=lines[3:6])
        divisible_bys.add(divisible_by)
        monkeys[id] = Monkey(items=items, operation=op, test=test)

    lcm = 1
    for x in divisible_bys:
        lcm *= x

    assert set(monkeys.keys()) == set(range(len(monkeys)))
    print(f"monkeys initially = {monkeys}")
    _run_monkey_rounds(monkeys=monkeys, rounds=10000, lcm=lcm)
    print(f"monkeys after running rounds = {monkeys}")
    monkey_activities = [x.total_items_inspected for (_, x) in monkeys.items()]
    print(f"monky_activities = {monkey_activities}")
    monkey_activities = sorted(monkey_activities, reverse=True)[0:2]
    print(f"Final answer = {monkey_activities[0] * monkey_activities[1]}")
