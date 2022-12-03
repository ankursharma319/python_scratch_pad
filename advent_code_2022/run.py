
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

def _find_common_char(a, b):
    set_a = set()
    for c in a:
        set_a.add(c)
    answer = None
    for c in b:
        if c in set_a:
            assert (answer is None) or (answer == c)
            answer = c
    assert answer is not None
    return answer

def _get_priority(c):
    assert len(c) == 1
    if ord(c) >= ord('a') and ord(c) <= ord('z'):
        return ord(c)-ord('a')+1
    if ord(c) >= ord('A') and ord(c) <= ord('Z'):
        return ord(c)-ord('A')+27
    assert False

def run_day_03():
    with open('./input03.txt') as f:
        total_priority = 0
        for line in f:
            stripped = line.rstrip()
            mid_index = len(stripped)//2
            print(f"mid_index = {mid_index}")
            compartment_a = stripped[0:mid_index]
            compartment_b = stripped[mid_index:]
            assert(len(compartment_a) == len(compartment_b))
            print(f"compartment_a={compartment_a} , compartment_b={compartment_b}")
            c = _find_common_char(compartment_a, compartment_b)
            current_priority = _get_priority(c)
            total_priority+= _get_priority(c)
        print(f"total_priority = {total_priority}")
run_day_03()
