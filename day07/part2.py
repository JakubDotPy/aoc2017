import argparse
import os.path
import re
from collections import Counter

import matplotlib.pyplot as plt
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
EXPECTED = 60


def parse(s):
    lines = s.splitlines()
    G = nx.DiGraph()
    for line in lines:
        this_node, weight, *others = re.findall(r'\w+', line)
        G.add_node(this_node, weight=int(weight))
        for other in others:
            G.add_edge(this_node, other)
    return G


def show_graph(G):
    pos_nodes = nx.planar_layout(G)
    nx.draw(G, pos_nodes, with_labels=True)
    pos_attrs = {}
    for node, coords in pos_nodes.items():
        pos_attrs[node] = (coords[0] + 0.10, coords[1])

    custom_node_attrs = {
        node: f'{node["weight"]} {node.get("total", 0)}'
        for node in G.nodes()
    }

    nx.draw_networkx_labels(G, pos_attrs, labels=custom_node_attrs)
    plt.show()


def compute(s: str) -> int:
    G = parse(s)
    topo_sort = list(nx.topological_sort(G))

    # Keep track of each node's total weight (itself + its children)
    weights = {}

    for node in reversed(topo_sort):
        total = G.nodes[node]['weight']

        counts = Counter(weights[child] for child in G[node])
        unbalanced = None

        for child in G[node]:
            # If this child's weight is different from others, we've found it
            if len(counts) > 1 and counts[weights[child]] == 1:
                unbalanced = child
                break
            # Otherwise add to the total weight
            total += weights[child]

        if unbalanced:
            # Find the weight adjustment and the new weight of this node
            diff = (max(counts) - min(counts))
            return G.nodes[unbalanced]['weight'] - diff

        # Store the total weight of the node
        weights[node] = total


# @pytest.mark.solved
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
