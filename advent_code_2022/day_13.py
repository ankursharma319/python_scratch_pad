import json
from functools import cmp_to_key

def _comp_pairs(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        else:
            return None
    if isinstance(left, list) and isinstance(right, list):
        for i in range(len(left)):
            if i == len(right):
                return False
            ret = _comp_pairs(left=left[i], right=right[i])
            if ret is None:
                continue
            else:
                return ret
        if len(left) < len(right):
            return True
        if len(left) == len(right):
            return None

    if isinstance(left, list) and isinstance(right, int):
        return _comp_pairs(left, [right])
    if isinstance(right, list) and isinstance(left, int):
        return _comp_pairs([left], right)

def compare_pairs(left, right):
    ret = _comp_pairs(left, right)
    if ret is None:
        return True
    return ret

def sort_compare_func(left, right):
    ret = _comp_pairs(left=left, right=right)
    if ret is None:
        return 0
    if ret:
        return -1
    else:
        return 1

def run():
    packets = []
    with open("./input13.txt") as f:
        for i,line in enumerate(f):
            if line.rstrip() == '':
                continue
            json_parsed = json.loads(line)
            packets.append(json_parsed)

    assert len(packets) % 2 == 0
    sum_of_indices = 0
    for i in range(0, len(packets), 2):
        in_order = compare_pairs(packets[i], packets[i+1])
        if in_order:
            sum_of_indices += (i//2) + 1
    print(f"sum_of_indices = {sum_of_indices}")

    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=cmp_to_key(sort_compare_func))
    indice_1 = packets.index([[2]])
    indice_2 = packets.index([[6]])
    print(f"indice_1 = {indice_1}")
    print(f"indice_2 = {indice_2}")
    decoder_key = (indice_1 + 1) * (indice_2 + 1)
    print(f"decoder_key = {decoder_key}")

if __name__ == '__main__':
    run()
