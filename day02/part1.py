def is_invalid_id(id: int):
    id_str = str(id)
    middle = len(id_str) // 2

    if len(id_str) % 2 == 0 and id_str[:middle] == id_str[middle:]:
        return True

    return False


def part1():
    solution = 0
    input = []

    with open("input.txt", "r") as f:
        input = f.readline().rsplit(",")

    # we could do significantly fewer checks
    for range in input:
        start, end = [int(x) for x in range.split("-")]

        while start < end:
            if is_invalid_id(start):
                solution += start

            start += 1

    print(solution)


if __name__ == "__main__":
    part1()
