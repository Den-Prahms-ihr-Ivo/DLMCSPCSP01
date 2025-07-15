import pandas as pd

from src import graph_utils
from tests.data import TEST_GRAPHS, EXPECTED_EDGES, EXPECTED_CSV_EDGES


if __name__ == "__main__":
    # graph = TEST_GRAPHS["counter_example_longest"]
    # edges = EXPECTED_CSV_EDGES["Test_Case_2"]

    graph = graph_utils.process_CSV("./data/Test_Case_1.csv")
    if graph:
        graph_utils.print_graph(graph)

    print("\n----------\n")
    # for e in edges:
    # graph_utils.print_edge(e)
