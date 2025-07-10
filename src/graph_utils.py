import copy
import operator
import pandas as pd

from typing import Dict, TypedDict, Optional, List, Tuple


class Node(TypedDict):
    name: str
    initial_net_balance: int
    current_net_balance: int


class Edge(TypedDict):
    origin: Node
    destination: Node
    weight: int


class Graph(TypedDict):
    name: str
    nodes: Dict[str, Node]
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

    for key, node in tmp["nodes"].items():
        # outgoing edges
        money_given = sum(
            [e["weight"] for e in tmp["edges"] if e["origin"]["name"] == key]
        )
        # incoming edges
        money_received = sum(
            [e["weight"] for e in tmp["edges"] if e["destination"]["name"] == key]
        )

        net_balance = money_received - money_given

        node["initial_net_balance"] = net_balance
        node["current_net_balance"] = net_balance

    # TODO: assertion, dass alles aufgeht

    tmp["edges"] = []

    return tmp


def pair_largest_difference_first(graph: Graph) -> Graph:
    """
    First sorts all balances then matches the ones with the largest difference.
    Returns a copy with all transactions minimized starting with the largest differnce
    """
    tmp = copy.deepcopy(graph)

    # Largest balance is now at position [0] and the lowest at [-1]
    balances: List[Node] = sorted(
        list(tmp["nodes"].values()),
        key=lambda d: d["current_net_balance"],
        reverse=True,
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
            tmp["nodes"][A["name"]]["current_net_balance"] = 0
            tmp["nodes"][B["name"]]["current_net_balance"] = 0

            # In this case there is no need to resort the array

        elif a < abs(b):
            # Since |a| < |b|, A can not repay for all the money B has lent.
            new_transactions.append({"origin": A, "destination": B, "weight": a})

            # now A has a balance of 0 and disapears therefore from the balance list.
            balances = balances[1:]
            # ...  and their corresponding net_balance are updated
            tmp["nodes"][A["name"]]["current_net_balance"] = 0
            tmp["nodes"][B["name"]]["current_net_balance"] = b + a

            # resort
            balances = sorted(
                list(tmp["nodes"].values()),
                key=lambda d: d["current_net_balance"],
                reverse=True,
            )
        else:  # a > abs(b)
            # Since |a| > |b|, A has to pay back more than B has lent.
            new_transactions.append({"origin": A, "destination": B, "weight": abs(b)})

            # now B has a balance of 0 and disapears therefore from the balance list.
            balances = balances[:-1]
            # ...  and their corresponding net_balance are updated
            tmp["nodes"][A["name"]]["current_net_balance"] = b + a
            tmp["nodes"][B["name"]]["current_net_balance"] = 0

            # resort
            balances = sorted(
                list(tmp["nodes"].values()),
                key=lambda d: d["current_net_balance"],
                reverse=True,
            )

    tmp["edges"] += new_transactions

    return tmp


def _find_subset_indices(arr, target):
    """
    Recursive Search if a target number can be expressed as the sum of a subset of an array
    """

    # Depth First Search
    def dfs(i, remaining):
        if remaining == 0:
            return []

        if i >= len(arr) or remaining < 0:
            return None

        # Include arr[i]
        with_curr = dfs(
            i + 1, remaining - abs(arr[i])
        )  # Absolute, for this specific case.
        if with_curr is not None:
            result = [i] + with_curr
            return result

        # Exclude arr[i]
        without_curr = dfs(i + 1, remaining)
        return without_curr

    tmp = dfs(0, abs(target))
    return tmp if tmp else []


def _reduce_possible_combinations(
    balances, reverse=True
) -> Optional[Tuple[int, List[int]]]:
    """
    It is assumed, that the balance list is already sorted from high to low.
    i.e. 9,8,2,-4,-5,10

    Returns ( index of number that has a subset)
    None if not possible
    """
    # Find possible commbinations to settle debts more efficiently
    comp = operator.lt if reverse else operator.gt

    splitting_index = next((i for i, b in enumerate(balances) if comp(b, 0)), None)

    if not splitting_index:
        return None

    right_balances = balances[splitting_index:]

    # Now we try to find a way to express a balance on the left as a sum of balances on the right (i.r)
    for l, left in enumerate(balances[:splitting_index]):
        subset = _find_subset_indices(arr=right_balances, target=left)
        if len(subset) > 0:
            return (l, [s + splitting_index for s in subset])

    return None


def pair_matching_differences_first_LEFT(graph: Graph) -> Graph:
    """
    Takes a list of balances and tries to find number that add up to 0
    Returns a copy with all transactions minimized starting with the best matching differnces
    If none are Found, None is returned.

    Matching from the left
    """
    tmp = copy.deepcopy(graph)

    # First sorts all balances then matches differences.
    # Largest balance is now at position [0] and the lowest at [-1]
    balances: List[Node] = sorted(
        list(tmp["nodes"].values()),
        key=lambda d: d["initial_net_balance"],
        reverse=True,
    )

    new_transactions: List[Edge] = []

    tpl = _reduce_possible_combinations(
        balances=[b["initial_net_balance"] for b in balances]
    )

    while tpl:
        idx, combinations = tpl
        A = balances[idx]

        # update Edges
        for c in combinations:
            if balances[c]["current_net_balance"] < 0:
                new_transactions.append(
                    {
                        "origin": A,
                        "destination": balances[c],
                        "weight": abs(balances[c]["current_net_balance"]),
                    }
                )
            else:
                new_transactions.append(
                    {
                        "destination": A,
                        "origin": balances[c],
                        "weight": abs(balances[c]["current_net_balance"]),
                    }
                )

            # update balances
            tmp["nodes"][balances[idx]["name"]]["current_net_balance"] = abs(
                balances[idx]["current_net_balance"]
            ) - abs(balances[c]["current_net_balance"])
            tmp["nodes"][balances[c]["name"]]["current_net_balance"] = 0

        balances = sorted(
            list(tmp["nodes"].values()),
            key=lambda d: d["current_net_balance"],
            reverse=True,
        )
        tpl = _reduce_possible_combinations(
            balances=[b["current_net_balance"] for b in balances]
        )

        # TRY the other way around
        if tpl is None:
            balances = sorted(
                list(tmp["nodes"].values()),
                key=lambda d: d["current_net_balance"],
                reverse=False,
            )
            tpl = _reduce_possible_combinations(
                balances=[b["current_net_balance"] for b in balances], reverse=False
            )

    # ############################
    # TODO: IMPLEMENT
    # ############################
    # TODO: Weitermachen mit largest matching.

    # tmp["nodes"] = balances
    tmp["edges"] += new_transactions

    return pair_largest_difference_first(tmp)


def simplify_transactions(graph: Graph) -> Graph:
    """
    Expects a graph with simplified expenses and returns a copy of the initial graph
    """
    tmp = copy.deepcopy(graph)

    return tmp


"""
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
"""

# TODO: IVO
# def df_to_graph(df: pd.DataFrame) -> Graph:
#     nodes: Dict[str, Node] = []
#     edges: List[Edge] = []

#     # Im Nachhinein wäre es sooooooooo viel cleverer gewesen alle Nodes als Dict aufzubauen, aber
#     # Jetzt hab ich dazu keinen Bock mehr :(

#     node_names = pd.unique(df[["Giver", "Receiver"]].values.ravel("K"))

#     for i, n in enumerate(node_names):
#         nodes[n] = {"name": n, "initial_net_balance": 0, "current_net_balance": 0}

#     for index, row in df.iterrows():
#         print(row["c1"], row["c2"])


def print_graph(graph: Graph) -> None:
    for edge in graph["edges"]:
        print(
            f"{edge['origin']['name']} ==> {edge['destination']['name']} : {edge['weight']} "
        )


def compare_graphs(graph: Graph, edges: List[Edge]) -> None:
    print("AAAAA")
    for i, edge in enumerate(graph["edges"]):
        print(
            f"{edge['origin']['name']} ==> {edge['destination']['name']} : {edge['weight']} \t |  {edges[i]['origin']['name']} ==> {edges[i]['destination']['name']} : {edges[i]['weight']}"
        )
