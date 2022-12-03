import argparse
import os.path

import pytest

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


def compute(s: str) -> int:
    """
    NOTE: solved using math.
      Squares on bottom right diagonal.
      first find num**0.5 and round to get n
      then steps are n-1 + diff of square to num
    """
    return 0


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
