import argparse
import itertools
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
0: 3
1: 2
4: 4
6: 4
'''
EXPECTED = 10


def compute(s: str) -> int:
    multiples = dict(
        tuple(map(int, row.split(': ')))
        for row in s.strip().splitlines()
    )

    for delay in itertools.count():
        positions = (
            (depth + delay) % (2 * size - 2) == 0
            for depth, size in multiples.items()
        )
        if not any(positions):
            return delay


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
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
