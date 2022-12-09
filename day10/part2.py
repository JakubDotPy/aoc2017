import argparse
import os.path
from functools import reduce
from itertools import zip_longest
from operator import xor

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


def grouper(iterable, n):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    return zip_longest(*args)


def compute(s: str) -> int:
    steps = [ord(c) for c in s.strip()] + [17, 31, 73, 47, 23]
    n_nums = 256
    nums = list(range(n_nums))
    idx = 0
    ds = 0
    for _ in range(64):
        for step in steps:
            slice = take_slice(idx, step, nums)
            for dx, num in enumerate(reversed(slice)):
                insert_idx = (idx + dx) % n_nums
                nums[insert_idx] = num
            idx += step + ds
            ds += 1

    dense_hash = [
        reduce(xor, block)
        for block in grouper(nums, 16)
    ]
    return ''.join(f'{n:02x}' for n in dense_hash)


# @pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('', 'a2582a3a0e66e6e86e3812dcb672a272'),
            ('AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
            ('1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'),
            ('1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e'),
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
