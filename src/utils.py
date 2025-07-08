import copy

from typing import Dict, TypedDict, Optional, List


class Node(TypedDict):
    id: int
    name: str
    initial_net_balance: int
    current_net_balance: int


class Edge(TypedDict):
    origin: Node
    destination: Node
    weight: int


class Graph(TypedDict):
    name: str
    nodes: List[Node]
    edges: List[Edge]
    # GGF: used to check which graph is the most optimal
    # outgoing_payments: Optional[int]
    # ingoing_payments: Optional[int]


def reduce_net_balance(graph: Graph) -> Graph:
    """
    Calculates the net balances of a Node by reducing all in and outgoing edges.
    Returns a copy of the initial graph with reduced edges.
    """
    tmp = copy.deepcopy(graph)

    for node in tmp["nodes"]:
        # outgoing edges
        money_given = sum(
            [e["weight"] for e in tmp["edges"] if e["origin"]["id"] == node["id"]]
        )
        # incoming edges
        money_received = sum(
            [e["weight"] for e in tmp["edges"] if e["destination"]["id"] == node["id"]]
        )

        net_balance = money_received - money_given

        node["initial_net_balance"] = net_balance
        node["current_net_balance"] = net_balance

    # TODO: assertion, dass alles aufgeht

    return tmp


def pair_largest_difference_first(graph: Graph) -> Graph:
    """
    First sorts all balances then matches the ones with the largest difference.
    Returns a copy with all transactions minimized starting with the largest differnce
    """
    tmp = copy.deepcopy(graph)

    # Largest balance is now at position [0] and the lowest at [-1]
    balances: List[Node] = sorted(
        tmp["nodes"], key=lambda d: d["initial_net_balance"], reverse=True
    )

    new_transactions: List[Edge] = []

    while len(balances) > 1:
        A = balances[0]
        B = balances[-1]
        a = balances[0]["current_net_balance"]
        b = balances[-1]["current_net_balance"]

        # First check if balance is 0, then remove entry from list
        if a == 0:
            balances = balances[1:]
            continue

        # Now match first and last entry

        if a == abs(b):
            # A and B are a perfect match and cancel each other out.
            # Since A > B due to sorting, A hast to pay the amount to B to settle the debt.
            new_transactions.append({"origin": A, "destination": B, "weight": a})

            # afterwards these nodes are removed from the list ...
            balances = balances[1:-1]
            # ...  and their corresponding net_balance are updated
            item = next((n for n in tmp["nodes"] if n["id"] == A["id"]), None)
            if item:
                item["current_net_balance"] = 0
            item = next((n for n in tmp["nodes"] if n["id"] == B["id"]), None)
            if item:
                item["current_net_balance"] = 0

            # In this case there is no need to resort the array

        elif a < abs(b):
            # Since |a| < |b|, A can not repay for all the money B has lent.
            new_transactions.append({"origin": A, "destination": B, "weight": a})

            # now A has a balance of 0 and disapears therefore from the balance list.
            balances = balances[1:]
            # ...  and their corresponding net_balance are updated
            item = next((n for n in tmp["nodes"] if n["id"] == A["id"]), None)
            if item:
                item["current_net_balance"] = 0
            item = next((n for n in tmp["nodes"] if n["id"] == B["id"]), None)
            if item:
                item["current_net_balance"] = b + a

            # resort
            balances = sorted(
                tmp["nodes"], key=lambda d: d["current_net_balance"], reverse=True
            )
        else:  # a > abs(b)
            # Since |a| > |b|, A has to pay back more than B has lent.
            new_transactions.append({"origin": A, "destination": B, "weight": b})

            # now B has a balance of 0 and disapears therefore from the balance list.
            balances = balances[:-1]
            # ...  and their corresponding net_balance are updated
            item = next((n for n in tmp["nodes"] if n["id"] == A["id"]), None)
            if item:
                item["current_net_balance"] = b + a
            item = next((n for n in tmp["nodes"] if n["id"] == B["id"]), None)
            if item:
                item["current_net_balance"] = 0

            # resort
            balances = sorted(
                tmp["nodes"], key=lambda d: d["current_net_balance"], reverse=True
            )

    tmp["edges"] = new_transactions

    return tmp


def simplify_transactions(graph: Graph) -> Graph:
    """
    Expects a graph with simplified expenses and returns a copy of the initial graph
    """
    tmp = copy.deepcopy(graph)

    return tmp


def print_graph(graph: Graph) -> None:
    for edge in graph["edges"]:
        print(
            f"{edge['origin']['name']} : {edge['weight']} ==> {edge['destination']['name']}"
        )
