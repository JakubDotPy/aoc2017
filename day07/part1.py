import argparse
import os.path
import re

import networkx as nx
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# NOTE: paste test text here
INPUT_S = '''\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''
EXPECTED = 'tknk'


def parse(s):
    lines = s.splitlines()
    G = nx.DiGraph()
    for line in lines:
        this_node, weight, *others = re.findall(r'\w+', line)
        G.add_node(this_node, weight=int(weight))
        for other in others:
            G.add_edge(this_node, other)
    return G


def compute(s: str) -> int:
    G = parse(s)
    for node, preds in G.pred.items():
        if not preds:
            return node


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
