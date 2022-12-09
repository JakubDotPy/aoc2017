import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
3,4,1,5
'''
EXPECTED = 12


def take_slice(index, amount, lst):
    length = len(lst)
    return [
        lst[(index + di) % length]
        for di in range(amount)
    ]


def compute(s: str) -> int:
    steps = (int(n) for n in s.strip().split(','))
    n_nums = 256  # FIXME: change to valid input
    nums = list(range(n_nums))
    idx = 0
    for ds, step in enumerate(steps):
        slice = take_slice(idx, step, nums)
        for dx, num in enumerate(reversed(slice)):
            insert_idx = (idx + dx) % n_nums
            nums[insert_idx] = num
        idx += step + ds
    return nums[0] * nums[1]


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
