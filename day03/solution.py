import argparse
import sys
from copy import copy


def parse_input(input_data: str) -> list[list[int]]:
    banks: list[list[int]] = []

    for line in input_data.splitlines():
        banks.append([int(x) for x in list(line)])

    return banks


def calculate_solution(banks: list[list[int]], battery_sequence_size: int = 2) -> int:
    joltage = 0

    for bank in banks:
        joltage_components: list[int] = []
        remaining = battery_sequence_size

        check_num = 9
        check_offset = 0

        while remaining >= 1:
            found_idx = (
                bank[check_offset:].index(check_num)
                if check_num in bank[check_offset:]
                else -1
            )

            # if not found, go to next number
            if found_idx == -1:
                check_num -= 1
                continue

            # if found but not enough remaining space, check next number
            if len(bank[check_offset:]) - found_idx < remaining:
                check_num -= 1
                continue

            # if enough space, change offest and continue
            joltage_components.append(check_num)

            check_offset += found_idx + 1
            check_num = 9
            remaining -= 1

        joltage += int("".join([str(x) for x in joltage_components]))

    return joltage


def part1(input_data: str) -> None:
    battery_banks = parse_input(input_data)
    result = calculate_solution(battery_banks)
    print(result)


def part2(input_data: str) -> None:
    battery_banks = parse_input(input_data)
    result = calculate_solution(battery_banks, 12)
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
