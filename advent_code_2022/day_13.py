import json

"""
If both values are integers, the lower integer should come first.
If the left integer is lower than the right integer, the inputs are in the right order.
If the left integer is higher than the right integer, the inputs are not in the right order.
Otherwise, the inputs are the same integer; continue checking the next part of the input.

If both values are lists, compare the first value of each list, then the second value, and so on.
If the left list runs out of items first, the inputs are in the right order. If the right list runs
out of items first, the inputs are not in the right order. If the lists are the same length and no
comparison makes a decision about the order, continue checking the next part of the input.

If exactly one value is an integer, convert the integer to a list which contains that integer as its
only value, then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right
value to [2] (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].
"""

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

def run():
    packets = []
    with open("./input13.txt") as f:
        for i,line in enumerate(f):
            if line.rstrip() == '':
                continue
            json_parsed = json.loads(line)
            print(f"json_parsed =  {json_parsed}")
            packets.append(json_parsed)

    assert len(packets) % 2 == 0
    sum_of_indices = 0
    for i in range(0, len(packets), 2):
        in_order = compare_pairs(packets[i], packets[i+1])
        if in_order:
            sum_of_indices += (i//2) + 1
    print(f"sum_of_indices = {sum_of_indices}")

if __name__ == '__main__':
    run()
