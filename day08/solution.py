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
) -> bool:
    root_circuit_x = find_circuit_root(node_parents, node_x)
    root_circuit_y = find_circuit_root(node_parents, node_y)

    if root_circuit_x == root_circuit_y:
        return False

    # attach smaller circuit to larger one -> fewer traversals to circuit root
    if circuit_sizes[root_circuit_x] < circuit_sizes[root_circuit_y]:
        node_parents[root_circuit_x] = root_circuit_y
        circuit_sizes[root_circuit_y] += circuit_sizes[root_circuit_x]
    else:
        node_parents[root_circuit_y] = root_circuit_x
        circuit_sizes[root_circuit_x] += circuit_sizes[root_circuit_y]

    return True


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


def prepare_sorted_edges(
    input_data: str,
) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    positions = parse_input(input_data)
    edges = generate_edges(positions)
    edges.sort(
        key=lambda edge: euclidian_distance(positions[edge[0]], positions[edge[1]])
    )
    return positions, edges


def calculate_result(circuit_sizes: list[int]) -> int:
    if len(circuit_sizes) < PART1_MIN_CIRCUITS:
        raise ValueError(f"Connected less than {PART1_MIN_CIRCUITS}, can't count")

    circuit_sizes.sort(reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def part1(input_data: str) -> None:
    positions, edges = prepare_sorted_edges(input_data)

    length = len(positions)
    parent = list(range(length))
    size = [1] * length

    pairs_processed = 0
    for node1, node2 in edges:
        if pairs_processed >= PART1_MAX_CONNECTIONS:
            break

        connect_circuits(parent, size, node1, node2)
        pairs_processed += 1

    circuit_sizes = get_circuit_sizes(parent, size)
    result = calculate_result(circuit_sizes)

    print(result)


def part2(input_data: str) -> None:
    positions, edges = prepare_sorted_edges(input_data)

    length = len(positions)
    parent = list(range(length))
    size = [1] * length

    last_connected_pair = None

    for node1, node2 in edges:
        # Try to merge the circuits
        if connect_circuits(parent, size, node1, node2):
            last_connected_pair = (node1, node2)

            # check if all nodes are in one circuit
            root = find_circuit_root(parent, node1)
            if size[root] == length:
                break

    if last_connected_pair is None:
        raise ValueError("Could not connect all nodes into one circuit")

    result = positions[last_connected_pair[0]][0] * positions[last_connected_pair[1]][0]

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
