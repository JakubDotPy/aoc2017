import argparse
import os.path
import re
from itertools import product

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
5 9 2 8
9 4 7 3
3 8 6 5
'''
EXPECTED = 9


def compute(s: str) -> int:
    checksum = 0
    lines = s.splitlines()
    for line in lines:
        nums = list(map(int, re.findall(r'\d+', line)))
        for n1, n2 in product(nums, nums):
            if n1 % n2 == 0 and n1 != n2:
                checksum += n1 // n2
    return checksum


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
