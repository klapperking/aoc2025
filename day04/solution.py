import argparse
import sys


def parse_input(input_data: str) -> list[list[str]]:
    rows: list[list[str]] = []

    for line in input_data.splitlines():
        rows.append([str(x) for x in line])

    return rows


def calculate_solution(rows: list[list[str]], battery_sequence_size: int = 2) -> int:
    movable_papers = 0

    removed_last_pass = True
    removed_positions: list[list[int]] = []

    while removed_last_pass:
        removed_last_pass = False

        for pos in removed_positions:
            rows[pos[0]][pos[1]] = "."

        removed_positions = []

        for row_idx in range(len(rows)):
            for col_idx in range(len(rows[row_idx])):
                adjacent = 0

                # all directions
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        check_row = row_idx + x
                        check_col = col_idx + y

                        # skip outside grid and current position
                        if (
                            (x == 0 and y == 0)
                            or check_row < 0
                            or check_row >= len(rows)
                            or check_col < 0
                            or check_col >= len(rows[0])
                        ):
                            continue

                        if rows[check_row][check_col] == "@":
                            adjacent += 1

                if adjacent < 4 and rows[row_idx][col_idx] == "@":
                    removed_positions.append([row_idx, col_idx])
                    removed_last_pass = True
                    movable_papers += 1

    return movable_papers


def part1(input_data: str) -> None:
    rows = parse_input(input_data)
    result = calculate_solution(rows)
    print(result)


def part2(input_data: str) -> None:
    rows = parse_input(input_data)
    result = calculate_solution(rows)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part2(input_data)
    else:
        part2(input_data)
