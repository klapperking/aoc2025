import argparse
import sys
from typing import Literal


def is_invalid_id(id: int):
    id_str = str(id)
    middle = len(id_str) // 2

    if len(id_str) % 2 == 0 and id_str[:middle] == id_str[middle:]:
        return True

    return False


def is_invalid_id_p2(id: int):
    id_str = str(id)
    length = len(id_str)

    # check all sample_sizes for repeating
    for sample_size in range(1, length // 2 + 1):
        # skip ranges that don't fit repeating
        if length % sample_size != 0:
            continue

        repeated_sample = id_str[:sample_size] * (length // sample_size)

        if repeated_sample == id_str:
            return True

    return False


def main(part: Literal[1] | Literal[2]):
    solution = 0

    input_file = sys.stdin.read()
    input = input_file.split(",")

    if part == 1:
        for range in input:
            start, end = [int(x) for x in range.split("-")]

            while start < end + 1:
                if is_invalid_id(start):
                    solution += start

                start += 1

    else:
        # we could do significantly fewer checks
        for range in input:
            start, end = [int(x) for x in range.split("-")]

            while start < end + 1:
                if is_invalid_id_p2(start):
                    solution += start

                start += 1

    print(solution)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", choices=[1, 2], type=int, required=True)

    args = parser.parse_args()

    main(args.part)
