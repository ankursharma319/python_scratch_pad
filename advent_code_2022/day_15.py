from functools import cmp_to_key

def _merge_ranges(lst):
    # print(f"lst before merging = {lst}")
    i = 0
    while i < len(lst):
        for j in range(len(lst)):
            if i == j:
                continue
            min_i, max_i = lst[i]
            min_j, max_j = lst[j]
            assert min_i <= max_i
            assert min_j <= max_j
            if (max_i + 1 < min_j) or (max_j + 1 < min_i+1):
                continue
            # print(f"merging {lst[i]} and {lst[j]}")
            new_max = max(max_i, max_j)
            new_min = min(min_i, min_j)
            lst[i] = (new_min, new_max)
            del lst[j]
            i = -1
            break
        i += 1

    lst = [x for x in lst if x is not None]
    def my_cmp(left, right):
        if left[0] < right[0]:
            return -1
        elif left[0] == right[0]:
            return 0
        else:
            return 1
    lst = sorted(lst, key=cmp_to_key(my_cmp))
    # print(f"lst after merging = {lst}")
    return lst



            
def _update_set_of_coords_where_beacon_isnt(sensor_coords, beacon_coords, isnt):
    distance = abs(sensor_coords[0]-beacon_coords[0]) + abs(sensor_coords[1]-beacon_coords[1])
    min_y = sensor_coords[1] - distance
    max_y = sensor_coords[1] + distance
    for y in range(min_y, max_y+1):
        vertical_dist = abs(y-sensor_coords[1])
        horizontal_dist = distance - vertical_dist
        local_min_x = sensor_coords[0] - horizontal_dist
        local_max_x = sensor_coords[0] + horizontal_dist
        if y not in isnt:
            isnt[y] = []
        isnt[y].append((local_min_x, local_max_x))

def run():
    coords = []
    beacon_coords = set()
    with open("./input15.txt") as f:
        for i,line in enumerate(f):
            splits = line.rstrip().split("Sensor at")
            splits = splits[1].split(": closest beacon is at ")
            sensor_split = splits[0].lstrip()[2:]
            beacon_split = splits[1][2:]
            sensor_splits = [int(x) for x in sensor_split.split(", y=")]
            beacon_splits = [int(x) for x in beacon_split.split(", y=")]
            beacon_coords.add((beacon_splits[0], beacon_splits[1]))
            coords.append(((sensor_splits[0], sensor_splits[1]), (beacon_splits[0], beacon_splits[1])))

    print(f"len(coords) = {len(coords)}")
    isnt = {}
    for i, (sensor_coords, beacon_coo) in enumerate(coords):
        print(f"processing coord# {i}")
        _update_set_of_coords_where_beacon_isnt(
            sensor_coords=sensor_coords,
            beacon_coords=beacon_coo,
            isnt = isnt
        )

    interesting_y_line = 2000000
    isnt[interesting_y_line] = _merge_ranges(isnt[interesting_y_line])
    interesting_count = 0
    for (min_x, max_x) in isnt[interesting_y_line]:
        interesting_count += (max_x-min_x)+1
        for bc in beacon_coords:
            if (bc[1] == interesting_y_line) and (bc[0] <= max_x) and (bc[0] >= min_x):
                interesting_count -= 1
    print(f"on line={interesting_y_line}, there are {interesting_count} spots where we know there is no beacon")

    max_coord_val = 4000000
    for y in range(max_coord_val):
        assert y in isnt
        isnt[y] = _merge_ranges(isnt[y])
        # print(f"at y = {y}, isnt = {isnt[y]}")
        for i, (min_x, max_x) in enumerate(isnt[y]):
            if min_x >= 0 and min_x <= max_coord_val:
                print(f"potentially interesting coord range, y = {y} , x = {min_x} to {max_x}")
                if isnt[y][i-1][1] == min_x - 2:
                    freq = (min_x-1) * 4000000 + y
                    print(f"freq = {freq}")
            if max_x >= 0 and max_x <= max_coord_val:
                print(f"potentially interesting coord range, y = {y} , x = {min_x} to {max_x}")

if __name__ == '__main__':
    run()
