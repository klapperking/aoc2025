import argparse
import sys


def parse_input(input_data: str) -> list[list[int]]:
    banks: list[list[int]] = []

    for line in input_data.splitlines():
        banks.append([int(x) for x in list(line)])

    return banks


def calculate_solution(banks: list[list[int]]) -> int:
    joltage = 0

    for bank in banks:
        first = max(bank)
        idx = bank.index(first)
        if idx == len(bank) - 1:
            first = max(bank[:-1])

        second = max(bank[bank.index(first) + 1 :])

        joltage += int("".join([str(first), str(second)]))

    return joltage


def part1(input_data: str) -> None:
    batteries = parse_input(input_data)
    result = calculate_solution(batteries)
    print(result)


# def part2(input_data: str) -> None:
#     ranges = parse_input(input_data)
#     result = calculate_solution(ranges, is_invalid_id_p2)
#     print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    input_data = sys.stdin.read()

    if args.part == 1:
        part1(input_data)
    # else:
    #     part2(input_data)
