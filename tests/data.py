from typing import Dict, List

from src.utils import Edge, Node, Graph

A: Node = {"id": 1, "name": "A", "initial_net_balance": 0, "current_net_balance": 0}
B: Node = {"id": 2, "name": "B", "initial_net_balance": 0, "current_net_balance": 0}
C: Node = {"id": 3, "name": "C", "initial_net_balance": 0, "current_net_balance": 0}
D: Node = {"id": 4, "name": "D", "initial_net_balance": 0, "current_net_balance": 0}

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
}

EXPECTED_EDGES: Dict[str, List[Edge]] = {
    "0_sum": [],
    "4_trans_to_3": [
        {"origin": A, "destination": C, "weight": 3},
        {"origin": B, "destination": C, "weight": 1},
        {"origin": B, "destination": D, "weight": 6},
    ],
}
