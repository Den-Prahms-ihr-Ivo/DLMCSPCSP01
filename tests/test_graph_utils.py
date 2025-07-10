"""
Test Cases for Graph Ultility Functions.
They do the bulk of the work when it comes to minimizing debts
"""

import pytest


from src import graph_utils
from .data import TEST_GRAPHS, EXPECTED_EDGES, EXPECTED_CSV_EDGES


class TestGraphUtils:

    @pytest.mark.parametrize(
        "graph, expected",
        [
            (TEST_GRAPHS["has_no_cycle"], [-1, -2, 3]),
            (TEST_GRAPHS["4_friends"], [-6, 1, 2, 3]),
        ],
    )
    def test_reduce_net_balance(self, graph, expected):
        tmp = graph_utils.reduce_net_balance(graph)

        for i, node in enumerate(list(tmp["nodes"].values())):
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
            (
                TEST_GRAPHS["counter_example_opposite"],
                EXPECTED_EDGES["counter_example_opposite"],
                True,
            ),
            (
                TEST_GRAPHS["counter_example_opposite_reverse"],
                EXPECTED_EDGES["counter_example_opposite_reverse"],
                True,
            ),
        ],
        ids=[
            "LARGEST - balances equal to 0",
            "LARGEST - simple 4->3",
            "LARGEST - Counter Example",
            "LARGEST - Counter Example Opposite #2",
            "LARGEST - REVERSE Counter Example Opposite #2",
        ],
    )
    def test_pair_largest_difference_first(self, graph, expected, is_expected_to_fail):
        # The function expects a graph that has already been reduced
        tmp = graph_utils.pair_largest_difference_first(
            graph_utils.reduce_net_balance(graph)
        )

        # print(tmp)

        found_edges = 0
        for expected_e in expected:
            edge = next(
                (
                    e
                    for e in tmp["edges"]
                    if e["origin"]["name"] == expected_e["origin"]["name"]
                    and e["destination"]["name"] == expected_e["destination"]["name"]
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

    @pytest.mark.parametrize(
        ("graph", "expected", "is_expected_to_fail"),
        [
            (TEST_GRAPHS["0_sum"], EXPECTED_EDGES["0_sum"], False),
            (TEST_GRAPHS["4_trans_to_3"], EXPECTED_EDGES["4_trans_to_3"], False),
            (
                TEST_GRAPHS["counter_example_longest"],
                EXPECTED_EDGES["counter_example_longest"],
                False,
            ),
            (
                TEST_GRAPHS["counter_example_opposite"],
                EXPECTED_EDGES["counter_example_opposite"],
                False,
            ),
            (
                TEST_GRAPHS["counter_example_opposite_reverse"],
                EXPECTED_EDGES["counter_example_opposite_reverse"],
                False,
            ),
            (
                TEST_GRAPHS["problematic_matching"],
                EXPECTED_EDGES["problematic_matching"],
                False,
            ),
        ],
        ids=[
            "MATCH - balances equal to 0",
            "MATCH - simple 4->3",
            "MATCH - Counter Example",
            "MATCH - Counter Example Opposite #2",
            "MATCH - REVERSE Counter Example Opposite #2",
            "MATCH - Problematic Matching",
        ],
    )
    def test_pair_matching_differences_first_LEFT(
        self, graph, expected, is_expected_to_fail
    ):
        # The function expects a graph that has already been reduced
        tmp = graph_utils.pair_matching_differences_first_LEFT(
            graph_utils.reduce_net_balance(graph)
        )

        found_edges = 0
        for expected_e in expected:
            edge = next(
                (
                    e
                    for e in tmp["edges"]
                    if e["origin"]["name"] == expected_e["origin"]["name"]
                    and e["destination"]["name"] == expected_e["destination"]["name"]
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

    @pytest.mark.parametrize(
        ("target", "arr", "expected"),
        [
            (9, [4, 4, 5, 9, 10], [0, 2]),
            (7, [1, 3, 5], []),
            (9, [], []),
            (10, [10], [0]),
            (10, [1, 2, 3, 4], [0, 1, 2, 3]),
        ],
    )
    def test_find_subset_indices(self, arr, target, expected):
        result = graph_utils._find_subset_indices(arr=arr, target=target)

        assert len(expected) == len(result)

        for i, e in enumerate(expected):
            assert e == result[i]

    @pytest.mark.parametrize(
        ("path_to_csv", "expected"),
        [
            ("./data/Test_Case_1", EXPECTED_CSV_EDGES["Test_Case_1"]),
        ],
        ids=[
            "TEST CASE 1",
        ],
    )
    def test_integration(self, path_to_csv, expected):
        # The function expects a graph that has already been reduced
        tmp = graph_utils.process_CSV(path_to_csv)

        found_edges = 0
        for expected_e in expected:
            edge = next(
                (
                    e
                    for e in tmp["edges"]
                    if e["origin"]["name"] == expected_e["origin"]["name"]
                    and e["destination"]["name"] == expected_e["destination"]["name"]
                ),
                None,
            )
            if edge:
                assert edge["weight"] == expected_e["weight"]
                found_edges += 1
            else:
                print("\n--------\n")
                graph_utils.print_edge(expected_e)
                print("\n\n")
                graph_utils.print_graph(tmp)
                assert False

        assert found_edges == len(tmp["edges"])
