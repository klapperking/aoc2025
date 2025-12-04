import argparse
import sys
from collections import deque

CHECK_POSITIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def parse_input(input_data: str) -> list[list[str]]:
    rows: list[list[str]] = []

    for line in input_data.splitlines():
        rows.append(list(line))

    return rows


def get_neighbor_papers(
    rows: list[list[str]], row_idx: int, col_idx: int, height: int, width: int
) -> list[tuple[int, int]]:
    neighbors = []

    for x, y in CHECK_POSITIONS:
        neighbor_x, neighbor_y = row_idx + x, col_idx + y

        if (
            neighbor_x < 0
            or neighbor_x >= height
            or neighbor_y < 0
            or neighbor_y >= width
        ):
            continue

        if rows[neighbor_x][neighbor_y] == "@":
            neighbors.append((neighbor_x, neighbor_y))

    return neighbors


def is_movable(
    rows: list[list[str]], row_idx: int, col_idx: int, height: int, width: int
) -> bool:
    adjacent = 0

    for x, y in CHECK_POSITIONS:
        check_row = row_idx + x
        check_col = col_idx + y

        if check_row < 0 or check_row >= height or check_col < 0 or check_col >= width:
            continue

        if rows[check_row][check_col] == "@":
            adjacent += 1
            if adjacent >= 4:
                return False

    return True


def calculate_solution(rows: list[list[str]], single_pass: bool) -> int:
    height = len(rows)
    width = len(rows[0]) if height > 0 else 0

    queue: deque[tuple[int, int]] = deque()

    for row_idx in range(height):
        for col_idx in range(width):
            if rows[row_idx][col_idx] == "@" and is_movable(
                rows, row_idx, col_idx, height, width
            ):
                queue.append((row_idx, col_idx))

    # part 1 -> return
    if single_pass:
        return len(queue)

    # part 2: do until nothing gets removed
    total_removed = 0

    while queue:
        row_idx, col_idx = queue.popleft()

        # skip if has been removed
        if rows[row_idx][col_idx] != "@":
            continue

        # can it be moved?
        if not is_movable(rows, row_idx, col_idx, height, width):
            continue

        # move it
        rows[row_idx][col_idx] = "."
        total_removed += 1

        # queue its paper neighbors for checking
        for neighbor in get_neighbor_papers(rows, row_idx, col_idx, height, width):
            queue.append(neighbor)

    return total_removed


def part1(input_data: str) -> None:
    rows = parse_input(input_data)
    result = calculate_solution(rows, single_pass=True)
    print(result)


def part2(input_data: str) -> None:
    rows = parse_input(input_data)
    result = calculate_solution(rows, single_pass=False)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    else:
        part2(input_data)
