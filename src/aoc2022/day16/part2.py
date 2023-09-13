import re
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any, Deque

import pytest
from rich import print

SAMPLE_INPUT = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""
EXPECTED = 1707

VALVE = re.compile(r"[A-Z]{2}")
FLOW_RATE = re.compile(r"flow rate=(\d+)")
data = (Path(__file__).parent / "input.txt").read_text()


@dataclass(frozen=True)
class Valve:
    name: str
    flow_rate: int
    destinations: tuple[str, ...]


def parse_input(_input: str) -> dict[str, Valve]:
    valves: dict[str, Valve] = {}

    lines = _input.splitlines()
    for line in lines:
        valve, *dest_valves = VALVE.findall(line)
        dest_valves = tuple(dest_valves)
        flow_rate = int(FLOW_RATE.findall(line)[0])
        valve = Valve(valve, flow_rate, dest_valves)
        valves[valve.name] = valve

    return valves


def find_shortest_path_bfs(
    valves: dict[str, Valve], start: str, end: str
) -> tuple[tuple[Valve, ...], int]:
    start_valve = valves[start]
    visited = set()
    to_visit: Deque[tuple[Valve, ...]] = deque([(start_valve,)])
    while to_visit:
        pth = to_visit.popleft()

        curr = pth[-1]
        if curr.name == end:
            return pth, len(pth) - 1
        if curr not in visited:
            visited.add(curr)
        for nghbr in curr.destinations:
            if nghbr not in visited:
                to_visit.append(pth + (valves[nghbr],))
    raise SyntaxError()


def get_distances(
    valves: dict[str, Valve]
) -> dict[tuple[str, str], tuple[tuple[Valve, ...], int]]:
    distances = {}
    pos_valves = [v.name for v in valves.values() if v.flow_rate > 0]
    interesting_valves = ["AA"] + pos_valves
    nodes = product(interesting_valves, interesting_valves)
    for n0, n1 in nodes:
        distances[(n0, n1)] = find_shortest_path_bfs(valves, n0, n1)

    return distances


@dataclass
class FlowRate:
    current_valve: Valve
    time_remaining: int
    total_flow: int
    unopened: set[str]
    sequence: tuple[str, ...]


def get_max_flow(valves: dict[str, Valve]) -> dict[frozenset[str], int]:
    distances = get_distances(valves)
    possible_paths = defaultdict(list)
    unopened = {v.name for v in valves.values() if v.flow_rate > 0}
    to_visit = deque([FlowRate(valves["AA"], 26, 0, unopened, ("AA",))])
    max_flow = 0
    # print(unopened)
    while to_visit:
        curr = to_visit.popleft()
        curr_name = curr.current_valve.name
        possible_paths[frozenset(curr.sequence)].append(curr.total_flow)

        for d in curr.unopened - set(curr.sequence):
            curr_distance = distances[(curr_name, d)]
            travel_and_open_time = curr_distance[1] + 1
            if curr.time_remaining > travel_and_open_time:
                remaining_time = curr.time_remaining - travel_and_open_time
                dest_flow_rate = valves[d].flow_rate
                total_flow = curr.total_flow + remaining_time * dest_flow_rate
                remaining = curr.unopened - {d}
                flow = FlowRate(
                    valves[d],
                    time_remaining=remaining_time,
                    total_flow=total_flow,
                    unopened=remaining,
                    sequence=curr.sequence + (d,),
                )
                to_visit.append(flow)
            else:
                continue

        max_flow = max(max_flow, curr.total_flow)

    return {k: max(v) for k, v in possible_paths.items()}


def compute_soln(_input: str) -> Any:
    parsed = parse_input(_input)
    optimal = get_max_flow(parsed)
    optimal_nodes = tuple(optimal.keys())
    best_flow = 0
    for i, j in product(optimal_nodes, optimal_nodes):
        if i.intersection(j) == frozenset({"AA"}):
            # Can't open a node more than once. The only place they intersect is
            # at the starting point
            best_flow = max(best_flow, optimal[i] + optimal[j])

    return best_flow


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    soln = compute_soln(_input)
    assert soln == expected


if __name__ == "__main__":
    soln = compute_soln(data)
    # soln = compute_soln(SAMPLE_INPUT)
    print(soln)
