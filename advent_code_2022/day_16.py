

def dp(
    mins_remaining, current_pos, flow_rates, tunnels,
    current_rate, open_valves, memo
):
    if mins_remaining == 0:
        return 0

    if mins_remaining == 1:
        return current_rate

    key = (mins_remaining, current_pos, "_".join(sorted(list(open_valves))))
    if key in memo:
        return memo[key]

    # do nothing
    pressure_released_in_remaining = dp(
        mins_remaining=mins_remaining-1, current_pos=current_pos,
        flow_rates=flow_rates, tunnels=tunnels,
        current_rate=current_rate,
        open_valves=open_valves,
        memo=memo
    )
    pressure_released_doing_nothing = pressure_released_in_remaining + current_rate

    current_max_pressure_released = pressure_released_doing_nothing

    # open current valve
    if current_pos not in open_valves and flow_rates[current_pos] > 0:
        pressure_released_in_remaining = dp(
            mins_remaining=mins_remaining-1, current_pos=current_pos,
            flow_rates=flow_rates, tunnels=tunnels,
            current_rate = current_rate + flow_rates[current_pos],
            open_valves = open_valves | {current_pos}, memo=memo
        )
        pressure_released_open_valve = pressure_released_in_remaining + current_rate
        current_max_pressure_released = max(
            current_max_pressure_released,
            pressure_released_open_valve
        )
    
    # move to each neighbour one by one
    for dest in tunnels[current_pos]:
        pressure_released_in_remaining = dp(
            mins_remaining=mins_remaining-1, current_pos=dest,
            flow_rates=flow_rates, tunnels=tunnels,
            current_rate=current_rate,
            open_valves=open_valves, memo=memo
        )
        pressure_released_visit_neighbour = pressure_released_in_remaining + current_rate
        current_max_pressure_released = max(
            current_max_pressure_released,
            pressure_released_visit_neighbour
        )
    memo[key] = current_max_pressure_released
    return current_max_pressure_released

def run():
    flow_rates = {}
    tunnels = {}
    with open("./input16.txt") as f:
        for i,line in enumerate(f):
            print(f"line = {line.rstrip()}")
            splits = line.rstrip().split(" ")
            name = splits[1]
            flow_rate = int(splits[4].split("=")[1][:-1])
            paths = splits[9:]
            paths = [x.strip(",") for x in paths]
            flow_rates[name] = flow_rate
            tunnels[name] = paths
            print(f"name = {name}, flow_rate = {flow_rate}, paths = {paths}")

    open_valves = set()
    memo = dict()
    pressure_released = dp(
        mins_remaining=30, current_pos="AA",
        flow_rates=flow_rates, tunnels=tunnels,
        current_rate=0, open_valves=open_valves,
        memo=memo
    )
    print(f"pressure released = {pressure_released}")

if __name__ == '__main__':
    run()
