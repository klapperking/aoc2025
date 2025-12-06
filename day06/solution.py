import argparse
import math
import sys


def parse_input(input_data: str) -> tuple[list[tuple[int]], list[str]]:
    lines = input_data.splitlines()

    num_lines = lines[:-1]
    nums = [[int(x.strip()) for x in line.split(" ") if x] for line in num_lines]
    operations = [x.strip() for x in lines[-1].split(" ") if x]

    numbers: list[tuple[int]] = list(zip(*nums))

    return (numbers, operations)


def get_results(nums: list[tuple[int]], operations: list[str]) -> int:
    result = 0

    for i in range(0, len(operations)):
        numbers = nums[i]
        operation = operations[i]

        if operation == "+":
            result += sum(numbers)
        elif operation == "*":
            result += math.prod(numbers)

    return result


def prepare_p2(nums: list[tuple[int]]) -> list[tuple[int]]:
    return nums


def part1(input_data: str) -> None:
    nums, operations = parse_input(input_data)
    result = get_results(nums, operations)
    print(result)


def part2(input_data: str) -> None:
    nums, operations = parse_input(input_data)
    adjusted_nums = prepare_p2(nums)
    result = get_results(adjusted_nums, operations)
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
