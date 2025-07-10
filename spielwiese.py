import pandas as pd

from src import graph_utils
from tests.data import TEST_GRAPHS, EXPECTED_EDGES


if __name__ == "__main__":
    graph = TEST_GRAPHS["has_no_cycle"]

    print(graph)

    money_given = sum(
        [e["weight"] for e in graph["edges"] if e["destination"]["name"] == "C"]
    )
    print(money_given)

    tmp = graph_utils.reduce_net_balance(graph)
    # print([t[""] for t in tmp["nodes"]])
    for i, node in enumerate(list(tmp["nodes"].values())):
        print(node["initial_net_balance"])
