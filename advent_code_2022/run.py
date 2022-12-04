
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
