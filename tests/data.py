from typing import Dict, List

from src.graph_utils import Edge, Node, Graph

A: Node = {"id": 1, "name": "A", "initial_net_balance": 0, "current_net_balance": 0}
B: Node = {"id": 2, "name": "B", "initial_net_balance": 0, "current_net_balance": 0}
C: Node = {"id": 3, "name": "C", "initial_net_balance": 0, "current_net_balance": 0}
D: Node = {"id": 4, "name": "D", "initial_net_balance": 0, "current_net_balance": 0}
E: Node = {"id": 5, "name": "E", "initial_net_balance": 0, "current_net_balance": 0}
F: Node = {"id": 6, "name": "F", "initial_net_balance": 0, "current_net_balance": 0}


TEST_GRAPHS: Dict[str, Graph] = {
    "has_no_cycle": {
        "name": "No Cylces",
        "nodes": [A, B, C],
        "edges": [
            {"origin": A, "destination": B, "weight": 1},
            {"origin": B, "destination": C, "weight": 3},
        ],
    },
    "4_friends": {
        "name": "No Cylces",
        "nodes": [A, B, C, D],
        "edges": [
            {"origin": A, "destination": B, "weight": 2},
            {"origin": A, "destination": D, "weight": 6},
            {"origin": B, "destination": C, "weight": 1},
            {"origin": C, "destination": A, "weight": 2},
            {"origin": D, "destination": C, "weight": 3},
        ],
    },
    "0_sum": {
        "name": "Nullsumme",
        "nodes": [A, B, C],
        "edges": [
            {"origin": A, "destination": C, "weight": 20},
            {"origin": C, "destination": A, "weight": 10},
            {"origin": B, "destination": A, "weight": 10},
            {"origin": C, "destination": B, "weight": 10},
        ],
    },
    "4_trans_to_3": {
        "name": "Reducing 4 Transactions to 3",
        "nodes": [A, B, C, D],
        "edges": [
            {"origin": A, "destination": C, "weight": 1},
            {"origin": A, "destination": D, "weight": 2},
            {"origin": B, "destination": C, "weight": 3},
            {"origin": B, "destination": D, "weight": 4},
        ],
    },
    "counter_example_longest": {
        "name": "Counterexample for Greatest Distance Matching",
        "nodes": [A, B, C, D, E],
        "edges": [
            {"origin": C, "destination": A, "weight": 3},
            #
            {"origin": E, "destination": B, "weight": 4},
            {"origin": E, "destination": A, "weight": 4},
            #
            {"origin": D, "destination": A, "weight": 2},
            {"origin": D, "destination": B, "weight": 4},
        ],
    },
    "counter_example_opposite": {
        "name": "Counterexample for Closest Opposite Matching",
        "nodes": [A, B, C, D, E, F],
        "edges": [
            {"origin": D, "destination": A, "weight": 4},
            {"origin": E, "destination": A, "weight": 5},
            #
            {"origin": F, "destination": B, "weight": 8},
            {"origin": F, "destination": C, "weight": 2},
        ],
    },
    "counter_example_opposite_reverse": {
        "name": "Counterexample for Closest Opposite Matching",
        "nodes": [A, B, C, D, E, F],
        "edges": [
            {"origin": A, "destination": D, "weight": 4},
            {"origin": A, "destination": E, "weight": 5},
            #
            {"origin": B, "destination": F, "weight": 8},
            {"origin": C, "destination": F, "weight": 2},
        ],
    },
}

EXPECTED_EDGES: Dict[str, List[Edge]] = {
    "0_sum": [],
    "4_trans_to_3": [
        {"origin": C, "destination": A, "weight": 3},
        {"origin": C, "destination": B, "weight": 1},
        {"origin": D, "destination": B, "weight": 6},
    ],
    "counter_example_longest": [
        {"origin": B, "destination": A, "weight": 8},
        {"origin": A, "destination": C, "weight": 3},
        {"origin": A, "destination": D, "weight": 6},
    ],
    "counter_example_opposite": [
        {"origin": A, "destination": D, "weight": 4},
        {"origin": A, "destination": E, "weight": 5},
        #
        {"origin": B, "destination": F, "weight": 8},
        {"origin": C, "destination": F, "weight": 2},
    ],
    "counter_example_opposite_reverse": [
        {"origin": D, "destination": A, "weight": 4},
        {"origin": E, "destination": A, "weight": 5},
        #
        {"origin": F, "destination": B, "weight": 8},
        {"origin": F, "destination": C, "weight": 2},
    ],
}
