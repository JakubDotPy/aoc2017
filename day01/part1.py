import argparse
import os.path
from itertools import pairwise

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\

'''
EXPECTED = 1


def compute(s: str) -> int:
    # parse numbers
    nums = list(map(int, s.strip()))
    pairs = []
    for a, b in pairwise(nums + [nums[0]]):
        if a == b:
            pairs.append(a)
    return sum(pairs)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('1122', 3),
            ('1111', 4),
            ('1234', 0),
            ('91212129', 9),
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
