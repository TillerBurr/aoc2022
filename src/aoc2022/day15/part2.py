from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from rich import print

from aoc2022.utils.point import Point

SAMPLE_INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
EXPECTED = 56000011

data = (Path(__file__).parent / "input.txt").read_text()

X_MIN = 0
X_MAX = 4_000_000
# X_MAX = 20


def parse_line(line: str) -> tuple[Point, Point]:
    sensor, beacon = line.split(": ")
    sensor_x, sensor_y = sensor.split(", ")
    sensor_x = sensor_x.split("=")[-1]
    sensor_y = sensor_y.split("=")[-1]
    beacon_x, beacon_y = beacon.split(", ")
    beacon_x = beacon_x.split("=")[-1]
    beacon_y = beacon_y.split("=")[-1]
    return Point(int(sensor_x), int(sensor_y)), Point(int(beacon_x), int(beacon_y))


@dataclass(frozen=True)
class SensorBeacon:
    sensor: Point
    beacon: Point
    distance: int


def parse_input(_input: str) -> list[SensorBeacon]:
    lines = _input.splitlines()
    parsed_lines = [parse_line(line) for line in lines]
    sensors = [
        SensorBeacon(x[0], x[1], x[0].manhattan_distance(x[1])) for x in parsed_lines
    ]
    return sensors


"""TODO This is slow. find a better algorithm.

Find Outside perimeter
and compute intervals.
"""


def compute_coverage(_input: str, row: int) -> list[list[int]]:
    parsed = parse_input(_input)
    no_beacons = []

    for sensor_beacon in parsed:
        d = sensor_beacon.distance
        y_s = sensor_beacon.sensor.y
        x_s = sensor_beacon.sensor.x
        # d(Point(x_s,y_s),Point(x,y))=|x_s-x|+|y_s-y|
        d_x = d - abs(row - y_s)  # |x-x_s|
        if d_x < 0:
            continue
        x_min = x_s - d_x if x_s - d_x > X_MIN else X_MIN

        x_max = x_s + d_x if x_s + d_x < X_MAX else X_MAX
        no_beacons.append([x_min, x_max])

    no_beacons.sort(key=lambda x: x[0])
    # every interval has x[0]<=y[0] for x<=y
    merged_no_beacons = [no_beacons[0]]
    for it in no_beacons[1:]:
        prev_interval_upper_bound = merged_no_beacons[-1][1]
        if prev_interval_upper_bound == X_MAX:
            return merged_no_beacons
        """
        Four Cases for x<y
            1. x[1]<y[0]-1, intervals don't intersect
            2. x[1]=y[0]-1, intervals are next to each other
            3. y[0]<=x[1]<y[1], Intervals are partially covered
            4. y[1]<=x[1], y is inside of x
        """
        # if prev_interval_upper_bound >= it[1]:  # #4
        #     continue
        if prev_interval_upper_bound < it[0] - 1:  # #1
            merged_no_beacons.append(it)
        elif (
            it[0] <= prev_interval_upper_bound <= it[1]
            or it[0] - 1 == prev_interval_upper_bound
        ):  # #2 and #3
            merged_no_beacons[-1][1] = it[1]
    # num_no_beacons = sum([x[1] - x[0] for x in merged_no_beacons])

    return merged_no_beacons


def compute_soln(_input: str) -> Any:
    for row in range(X_MAX + 1):
        intervals = compute_coverage(_input, row)
        # print(row, intervals)
        if len(intervals) > 1:
            x_value = intervals[0][1] + 1
            y_value = row
            return x_value * 4_000_000 + y_value


@pytest.mark.parametrize(
    ("_input", "expected"),
    ((SAMPLE_INPUT, EXPECTED),),
)
def test(_input: str, expected: int) -> None:
    soln = compute_soln(_input)
    assert soln == expected


if __name__ == "__main__":
    # soln = compute_soln(SAMPLE_INPUT)
    soln = compute_soln(data)
    print(soln)
