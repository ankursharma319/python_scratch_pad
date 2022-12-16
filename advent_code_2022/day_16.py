

def dp(
    mins_remaining, current_pos, elephant_pos, flow_rates, tunnels,
    current_rate, open_valves, memo
):
    if mins_remaining == 0:
        return 0

    if mins_remaining == 1:
        return current_rate

    key = (mins_remaining, current_pos, elephant_pos, "_".join(sorted(list(open_valves))))
    if key in memo:
        return memo[key]

    print(f"solving dp for key={key}")

    my_actions = tunnels[current_pos].copy()
    elephant_actions = tunnels[elephant_pos].copy()

    if (current_pos not in open_valves) and (flow_rates[current_pos] > 0):
        my_actions.append("open_current")
    if (elephant_pos not in open_valves) and (flow_rates[elephant_pos] > 0):
        elephant_actions.append("open_current")

    if len(my_actions) == 0:
        my_actions.append("nothing")
    if len(elephant_actions) == 0:
        elephant_actions.append("nothing")

    current_max_pressure_released = 0
    for my_action in my_actions:
        for elephant_action in elephant_actions:
            remaining_rate = current_rate
            remaining_current_pos = current_pos
            remaining_elephant_pos = elephant_pos
            remaining_open_valves = open_valves.copy()
            if my_action == "nothing":
                pass
            elif my_action == "open_current":
                assert ((current_pos not in open_valves) and (flow_rates[current_pos] > 0))
                remaining_rate = remaining_rate + flow_rates[current_pos]
                remaining_open_valves = remaining_open_valves | {current_pos}
            else:
                remaining_current_pos = my_action
            if elephant_action == "nothing":
                pass
            elif elephant_action == "open_current":
                if elephant_pos not in remaining_open_valves and flow_rates[elephant_pos] > 0:
                    remaining_rate = remaining_rate + flow_rates[elephant_pos]
                    remaining_open_valves = remaining_open_valves | {elephant_pos}
            else:
                remaining_elephant_pos = elephant_action

            pressure_released_in_remaining = dp(
                mins_remaining=mins_remaining-1,
                current_pos=remaining_current_pos,
                elephant_pos=remaining_elephant_pos,
                flow_rates=flow_rates, tunnels=tunnels,
                current_rate=remaining_rate,
                open_valves=remaining_open_valves,
                memo=memo
            )
            current_pressure_released = pressure_released_in_remaining + current_rate
            current_max_pressure_released = max(
                current_max_pressure_released,
                current_pressure_released
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
        mins_remaining=26, current_pos="AA", elephant_pos="AA",
        flow_rates=flow_rates, tunnels=tunnels,
        current_rate=0, open_valves=open_valves,
        memo=memo
    )
    print(f"pressure released = {pressure_released}")

if __name__ == '__main__':
    run()
