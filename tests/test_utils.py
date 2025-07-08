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
        ("graph", "expected", "is_expected_to_fail"),
        [
            (TEST_GRAPHS["0_sum"], EXPECTED_EDGES["0_sum"], False),
            (TEST_GRAPHS["4_trans_to_3"], EXPECTED_EDGES["4_trans_to_3"], False),
            (
                TEST_GRAPHS["counter_example_longest"],
                EXPECTED_EDGES["counter_example_longest"],
                True,
            ),
        ],
        ids=["balances equal to 0", "4->3", "Counter Example"],
    )
    def test_pair_largest_difference_first(self, graph, expected, is_expected_to_fail):
        # The function expects a graph that has already been reduced
        tmp = utils.pair_largest_difference_first(utils.reduce_net_balance(graph))

        # print(tmp)

        found_edges = 0
        for expected_e in expected:
            edge = next(
                (
                    e
                    for e in tmp["edges"]
                    if e["origin"]["id"] == expected_e["origin"]["id"]
                    and e["destination"]["id"] == expected_e["destination"]["id"]
                ),
                None,
            )
            if edge:
                if not is_expected_to_fail:
                    assert edge["weight"] == expected_e["weight"]
                found_edges += 1
            else:
                assert is_expected_to_fail

        if not is_expected_to_fail:
            assert found_edges == len(tmp["edges"])
