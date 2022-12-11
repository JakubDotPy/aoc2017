import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\

'''
EXPECTED = 1


def compute(input_s: str) -> int:
    q = r = s = 0
    max_dist = 0
    for dir in input_s.strip().split(','):
        match dir:
            # @formatter:off
            case 'n':  s += 1; r -= 1
            case 'ne': q += 1; r -= 1
            case 'se': q += 1; s -= 1
            case 's':  r += 1; s -= 1
            case 'sw': r += 1; q -= 1
            case 'nw': s += 1; q -= 1
            # @formatter:on
        max_dist = max(max_dist, ((abs(q) + abs(r) + abs(s)) // 2))
    return max_dist


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('ne,ne,ne', 3),
            ('ne,ne,sw,sw', 0),
            ('ne,ne,s,s', 2),
            ('se,sw,se,sw,sw', 3),
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
