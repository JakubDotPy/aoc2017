import argparse
import math
import os.path
from itertools import islice

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
0 2 7 0
'''
EXPECTED = 4


def parts_gen(how_many, n_parts):
    iterable = range(how_many)
    n = math.ceil(how_many / n_parts)
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := list(islice(it, n))):
        yield len(batch)


def compute(s: str) -> int:
    # parse numbers
    banks = [int(n) for n in s.split()]
    n_banks = len(banks)
    seen = set()
    step = 0
    n_seen = 0
    steps = []
    to_check_again = None
    seen.add(str(banks))
    while True:
        max_ind = banks.index(max(banks))
        to_distribute = banks[max_ind]
        banks[max_ind] = 0
        pg = parts_gen(to_distribute, n_banks)
        for i, addition in enumerate(pg, start=1):
            next_index = (max_ind + i) % n_banks
            banks[next_index] += addition
        step += 1
        if not to_check_again:
            if str(banks) in seen:
                n_seen += 1
                steps.append(step)
                to_check_again = str(banks)
                seen.remove(to_check_again)
                continue
        else:
            if to_check_again in seen:
                n_seen += 1
                steps.append(step)
        if n_seen == 2:
            break
        seen.add(str(banks))
    return steps[-1] - steps[0] - 1


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
