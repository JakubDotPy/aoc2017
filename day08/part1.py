import argparse
import os.path
from collections import defaultdict

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
'''
EXPECTED = 1


def compute(s: str) -> int:
    registers = defaultdict(int)
    lines = s.splitlines()
    for line in lines:
        match line.split():
            case reg1, 'inc', val1, 'if', reg2, op, val2:
                if eval(f'registers["{reg2}"]{op}{val2}'):
                    registers[reg1] += int(val1)
            case reg1, 'dec', val1, 'if', reg2, op, val2:
                if eval(f'registers["{reg2}"]{op}{val2}'):
                    registers[reg1] -= int(val1)
            case _:
                raise AssertionError('uncaught')
    return max(registers.values())


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
