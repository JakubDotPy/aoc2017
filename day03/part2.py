import argparse
import os.path

import pytest

from support import Direction4
from support import adjacent_8
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
17  16  15  14  13  30
18   5   4   3  12  29
19   6   1   2  11  28
20   7   8   9  10  27
21  22  23  24  25  26
'''
EXPECTED = 1


def spiral_generator():
    """Generates the spiral

    steps:
    1R,  n-2U, n-1L, n-1D, n-1R
    """
    pos = 0, 0
    n = 3
    while True:
        pos = Direction4.RIGHT.apply(*pos);
        yield pos  # 1R
        for _ in range(n - 2): pos = Direction4.UP.apply(*pos); yield pos  # n-2U
        for _ in range(n - 1): pos = Direction4.LEFT.apply(*pos); yield pos  # n-1L
        for _ in range(n - 1): pos = Direction4.DOWN.apply(*pos); yield pos  # n-1D
        for _ in range(n - 1): pos = Direction4.RIGHT.apply(*pos); yield pos  # n-1R
        n += 2


def compute(s: str) -> int:
    target = int(s)
    grid = {(0, 0): 1}
    sg = spiral_generator()
    while True:
        pos = next(sg)
        val = sum(grid.get(adj, 0) for adj in adjacent_8(*pos))
        print(f'{pos}\t{val}')
        if val > target:
            return val
        grid[pos] = val


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (1, 0),
            (12, 3),
            (23, 2),
            (1024, 31),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
