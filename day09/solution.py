import argparse
import sys


def parse_input(input_data: str) -> list[tuple[int, int]]:
    result = []
    for line in input_data.splitlines():
        x, y = map(int, line.split(","))
        result.append((x, y))
    return result


def compress_coordinates(red_tiles: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # sort all x and y ascending
    all_x = sorted(set(x for x, y in red_tiles))
    all_y = sorted(set(y for x, y in red_tiles))

    # map original position values to their compressed counterparts
    x_map = {x: i for i, x in enumerate(all_x)}
    y_map = {y: i for i, y in enumerate(all_y)}

    # for original order, "replace" coordinates with the compressed equivalent
    return [(x_map[x], y_map[y]) for x, y in red_tiles]


def point_in_polygon(point: tuple[int, int], polygon: list[tuple[int, int]]) -> bool:
    x, y = point
    length = len(polygon)

    inside = False

    # check all edges of polygon for intersection
    p1x, p1y = polygon[0]
    for i in range(1, length + 1):
        p2x, p2y = polygon[i % length]

        # skip if point is below or above edge (2d coordinate system)
        if not (y > min(p1y, p2y) and y <= max(p1y, p2y)):
            p1x, p1y = p2x, p2y
            continue

        # skip if on the right of this edge
        if x > max(p1x, p2x):
            p1x, p1y = p2x, p2y
            continue

        # skip horizontal edge
        if p1y == p2y:
            p1x, p1y = p2x, p2y
            continue

        # get intersection x of horizontal ray and edge
        intersection_point = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

        # if intersecting, increase "intersection counter" by one
        if x <= intersection_point:
            inside = not inside

        p1x, p1y = p2x, p2y

    return inside


def build_green_tiles(red_tiles: list[tuple[int, int]]) -> set[tuple[int, int]]:
    # Build edge tiles
    edge_tiles = set()
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        # account for last edge wrapping around
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]

        if x1 == x2:
            # add vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                edge_tiles.add((x1, y))
        else:
            # add horizontal
            for x in range(min(x1, x2), max(x1, x2) + 1):
                edge_tiles.add((x, y1))

    # fill interior tiles
    all_x = set(x for x, _ in red_tiles)
    all_y = set(y for _, y in red_tiles)

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    interior = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            point = (x, y)
            if point not in edge_tiles and point not in set(red_tiles):
                if point_in_polygon(point, red_tiles):
                    interior.add(point)

    return edge_tiles | interior


def calc_area(pos1: tuple[int, int], pos2: tuple[int, int]):
    return (abs(pos2[0] - pos1[0]) + 1) * (abs(pos2[1] - pos1[1]) + 1)


def is_rectangle_valid(
    pos1: tuple[int, int],
    pos2: tuple[int, int],
    valid_tiles: set[tuple[int, int]],
) -> bool:
    x1, x2 = sorted((pos1[0], pos2[0]))
    y1, y2 = sorted((pos1[1], pos2[1]))

    # Check top and bottom edges
    for x in range(x1, x2 + 1):
        if (x, y1) not in valid_tiles or (x, y2) not in valid_tiles:
            return False

    # Check left and right edges
    for y in range(y1, y2 + 1):
        if (x1, y) not in valid_tiles or (x2, y) not in valid_tiles:
            return False

    return True


def find_largest_area_rectangle(positions: list[tuple[int, int]]) -> int:
    max_area = 0
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            area = calc_area(positions[i], positions[j])
            max_area = max(max_area, area)
    return max_area


def find_largest_area_rectangle_with_green_tiles(
    red_tiles: list[tuple[int, int]],
) -> int:
    compressed_tiles = compress_coordinates(red_tiles)

    green_tiles = build_green_tiles(compressed_tiles)
    red_set = set(compressed_tiles)
    valid_tiles = red_set | green_tiles

    # for each rectangle combination, get the area and its compressed coordinates
    pairs: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            area = calc_area(red_tiles[i], red_tiles[j])

            pairs.append((area, compressed_tiles[i], compressed_tiles[j]))

    # sort descending by area
    pairs.sort(reverse=True)

    # check rectangles to find largest
    for area, pos1, pos2 in pairs:
        if is_rectangle_valid(pos1, pos2, valid_tiles):
            return area

    return 0


def part1(input_data: str) -> None:
    red_tiles = parse_input(input_data)
    result = find_largest_area_rectangle(red_tiles)
    print(result)


def part2(input_data: str) -> None:
    red_tiles = parse_input(input_data)
    result = find_largest_area_rectangle_with_green_tiles(red_tiles)
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
