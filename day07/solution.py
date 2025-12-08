import argparse
import sys
from collections import deque


def parse_input(input_data: str) -> list[list[str]]:
    return [list(line) for line in input_data.splitlines()]


def get_start_pos(rows: list[list[str]]) -> tuple[int, int] | None:
    for row_idx in range(0, len(rows)):
        for col_idx in range(0, len(rows[0])):
            if rows[row_idx][col_idx] == "S":
                return (row_idx + 1, col_idx)

    return None


def get_n_splits(rows: list[list[str]]) -> int:
    result = 0

    checked: set[tuple[int, int]] = set()
    queued: deque[tuple[int, int]] = deque()

    start = get_start_pos(rows)
    if start is None:
        raise ValueError("Start positiion not found, input invalid")
    queued.append(start)

    while len(queued) > 0:
        check = queued.popleft()

        if check in checked:
            continue

        checked.add(check)

        y, x = check[0], check[1]

        grid_value = rows[y][x]

        new_positions: list[tuple[int, int]] = []

        if grid_value == ".":
            new_positions = [(y + 1, x)]
        elif grid_value == "^":
            new_positions = [(y + 1, x - 1), (y + 1, x + 1)]
            result += 1

        for pos in new_positions:
            if (
                pos[0] < 0
                or pos[0] >= len(rows)
                or pos[1] < 0
                or pos[1] >= len(rows[0])
            ):
                continue

            if pos not in checked:
                queued.append(pos)

    return result


# backtracking solution? -> start backtracking once the followed timeline gets out of bounds -> we can ignore x-OOB


def magic(rows: list[list[str]]):
    pass


def part1(input_data: str) -> None:
    grid = parse_input(input_data)
    result = get_n_splits(grid)
    print(result)


def part2(input_data: str) -> None:
    grid = parse_input(input_data)
    result = get_n_splits(grid)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    else:
        pass

# trace the beam, start at S. when a spli happens, append new positions to queue
# breadth first, check which positions are now beams -> add the next positions to queue
# when checking position, check if it is . -> append below, otherwise append left and right
# for each append, see if this position was checked -> set of tuples for checked positions
