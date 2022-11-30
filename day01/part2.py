import argparse
import os.path

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
    for i, num in enumerate(nums):
        index = (i + len(nums) // 2) % len(nums)
        if num == nums[index]:
            pairs.append(num)
    return sum(pairs)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('1212', 6),
            ('1221', 0),
            ('123425', 4),
            ('123123', 12),
            ('12131415', 4),
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
