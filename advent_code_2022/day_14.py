
def update_dust_pos(dust_pos, stones, dusts, floor_row):
    below = (dust_pos[0]+1, dust_pos[1])
    left = (dust_pos[0]+1, dust_pos[1]-1)
    right = (dust_pos[0]+1, dust_pos[1]+1)

    if floor_row == below[0]:
        return False
    if (below not in stones) and (below not in dusts):
        return below
    elif (left not in stones) and (left not in dusts):
        return left
    elif (right not in stones) and (right not in dusts):
        return right
    else:
        return False

def run():
    stones = set()
    dusts = set()
    lowest_stone_row = -1
    with open("./input14.txt") as f:
        for i,line in enumerate(f):
            splits = line.rstrip().split(" -> ")
            print(f"line = {splits}")
            coords = []
            for split in splits:
                pair = split.split(",")
                assert len(pair) == 2
                col = int(pair[0])
                row = int(pair[1])
                print(f"row, col = {row}, {col}")
                coords.append((row, col))
            prev_r, prev_c = coords[0]
            for (r,c) in coords:
                assert (prev_r == r) or (prev_c == c)
                if prev_r == r:
                    for i in range(min(c, prev_c), max(c, prev_c)+1):
                        stones.add((r,i))
                else:
                    for i in range(min(r, prev_r), max(r, prev_r)+1):
                        stones.add((i,c))
                prev_r = r
                prev_c = c
                lowest_stone_row = max(r, lowest_stone_row)
    print(f"len(stones) = {len(stones)}")
    print(f"lowest stone row = {lowest_stone_row}")

    while True:
        # generate dust at 500,0
        dust_pos = (0, 500)
        settled = False
        while not settled:
            new_dust_pos = update_dust_pos(dust_pos, stones, dusts, floor_row=lowest_stone_row+2)
            if not new_dust_pos:
                dusts.add(dust_pos)
                settled = True
                continue
            dust_pos = new_dust_pos
        if dust_pos == (0, 500):
            break
    print(f"answer = {len(dusts)}")

if __name__ == '__main__':
    run()
