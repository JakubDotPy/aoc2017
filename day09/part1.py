import argparse
import os.path
import re

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
'''
EXPECTED = 1


def reduce_junk(s):
    s = re.sub(r'!.', '', s)
    s = re.sub(r'<.*?>', '<>', s)
    return s


def remove_junk_groups(s: str):
    s = s.replace('<>', '')
    s = re.sub(r',+', '', s)
    return s


def compute(s: str) -> int:
    text = remove_junk_groups(reduce_junk(s))
    depth, score = 0, []
    for c in text:
        if c == '{':
            depth += 1
            score.append(depth)
        elif c == '}':
            depth -= 1

    return sum(score)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            ('{}', 1),
            ('{{{}}}', 6),
            ('{{},{}}', 5),
            ('{{{},{},{{}}}}', 16),
            ('{<a>,<a>,<a>,<a>}', 1),
            ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
            ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
            ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
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
