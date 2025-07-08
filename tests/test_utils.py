import pytest


from src import utils
from .data import TEST_GRAPHS, EXPECTED_EDGES


class TestUtils:

    @pytest.mark.parametrize(
        "graph, expected",
        [
            (TEST_GRAPHS["has_no_cycle"], [-1, -2, 3]),
            (TEST_GRAPHS["4_friends"], [-6, 1, 2, 3]),
        ],
    )
    def test_reduce_net_balance(self, graph, expected):
        tmp = utils.reduce_net_balance(graph)

        for i, node in enumerate(tmp["nodes"]):
            assert node["initial_net_balance"] == expected[i]

    @pytest.mark.parametrize(
        "graph, expected",
        [
            (TEST_GRAPHS["0_sum"], EXPECTED_EDGES["0_sum"]),
        ],
    )
    def test_pair_largest_difference_first(self, graph, expected):
        tmp = utils.pair_largest_difference_first(graph)

        for e in tmp["edges"]:
            assert e["origin"]["id"] == expected["origin"]["id"]
            assert e["destination"]["id"] == expected["destination"]["id"]
            assert e["weight"] == expected["weight"]
