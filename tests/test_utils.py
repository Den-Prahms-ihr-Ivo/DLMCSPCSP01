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
            (TEST_GRAPHS["4_trans_to_3"], EXPECTED_EDGES["4_trans_to_3"]),
        ],
    )
    def test_pair_largest_difference_first(self, graph, expected):
        tmp = utils.pair_largest_difference_first(graph)

        found_edges = 0
        for e in tmp["edges"]:
            edge = next(
                (
                    expected_e
                    for expected_e in expected
                    if expected_e["origin"]["id"] == e["origin"]["id"]
                    and expected_e["destination"]["id"] == e["destination"]["id"]
                ),
                None,
            )
            if edge:
                assert e["weight"] == edge["weight"]
                found_edges += 1
            else:
                assert False

        assert found_edges == len(tmp["edges"])
