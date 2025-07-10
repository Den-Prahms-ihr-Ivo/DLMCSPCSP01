from src import graph_utils
from tests.data import TEST_GRAPHS, EXPECTED_EDGES

if __name__ == "__main__":
    graph_utils.compare_graphs(
        graph_utils.pair_matching_differences_first_LEFT(
            graph_utils.reduce_net_balance(TEST_GRAPHS["counter_example_longest"])
        ),
        EXPECTED_EDGES["counter_example_longest"],
    )

    # print("\n")
    # graph_utils.print_graph(
    #     graph_utils.pair_matching_differences_first_LEFT(
    #         graph_utils.reduce_net_balance(
    #             TEST_GRAPHS["counter_example_opposite_reverse"]
    #         )
    #     )
    # )
