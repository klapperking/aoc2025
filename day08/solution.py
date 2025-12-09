import argparse
import math
import sys

PART1_MAX_CONNECTIONS = 1000
PART1_MIN_CIRCUITS = 3


def parse_input(input_data: str) -> list[tuple[int, int, int]]:
    positions: list[tuple[int, int, int]] = []

    for line in input_data.splitlines():
        position = tuple([int(x) for x in line.split(",")])
        if not len(position) == 3:
            raise ValueError("bad input")
        positions.append(position)

    return positions


def euclidian_distance(start: tuple[int, int, int], end: tuple[int, int, int]):
    # sqrt needed?
    return math.sqrt(
        (start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2 + (start[2] - end[2]) ** 2
    )


def find_circuit_root(parent: list[int], x: int) -> int:
    # TODO: path compression?
    while parent[x] != x:
        x = parent[x]
    return x


def connect_circuits(
    node_parents: list[int], circuit_sizes: list[int], node_x: int, node_y: int
):
    root_circuit_x = find_circuit_root(node_parents, node_x)
    root_circuit_y = find_circuit_root(node_parents, node_y)

    if root_circuit_x == root_circuit_y:
        return

    # attach smaller circuit to larger one -> fewer traversals to circuit root
    if circuit_sizes[root_circuit_x] < circuit_sizes[root_circuit_y]:
        node_parents[root_circuit_x] = root_circuit_y
        circuit_sizes[root_circuit_y] += circuit_sizes[root_circuit_x]
    else:
        node_parents[root_circuit_y] = root_circuit_x
        circuit_sizes[root_circuit_x] += circuit_sizes[root_circuit_y]


def get_circuit_sizes(parent: list[int], size: list[int]) -> list[int]:
    roots = set()

    for i in range(len(parent)):
        root = find_circuit_root(parent, i)
        roots.add(root)

    circuit_sizes = []
    for root in roots:
        circuit_sizes.append(size[root])

    return circuit_sizes


def generate_edges(positions: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            edges.append((i, j))

    return edges


def connect_closest_pairs(
    edges: list[tuple[int, int]],
    positions: list[tuple[int, int, int]],
    max_pairs: int,
) -> tuple[list[int], list[int]]:
    length = len(positions)
    node_parents = list(range(length))
    circuit_sizes = [1] * length
    pairs_processed = 0

    for node_x, node_y in edges:
        if pairs_processed >= max_pairs:
            break

        connect_circuits(node_parents, circuit_sizes, node_x, node_y)
        pairs_processed += 1

    return node_parents, circuit_sizes


def calculate_result(circuit_sizes: list[int]) -> int:
    if len(circuit_sizes) < PART1_MIN_CIRCUITS:
        raise ValueError(f"Connected less than {PART1_MIN_CIRCUITS}, can't count")

    circuit_sizes.sort(reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def part1(input_data: str) -> None:
    positions = parse_input(input_data)
    edges = generate_edges(positions)
    edges.sort(
        key=lambda edge: euclidian_distance(positions[edge[0]], positions[edge[1]])
    )

    parent, size = connect_closest_pairs(edges, positions, PART1_MAX_CONNECTIONS)
    circuit_sizes = get_circuit_sizes(parent, size)
    result = calculate_result(circuit_sizes)

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
