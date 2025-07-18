import copy
import operator
import pandas as pd
from math import inf as INFINITY

from typing import Dict, TypedDict, Optional, List, Tuple, Callable


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


def pair_matching_differences_first(graph: Graph, use_closest_matching=False) -> Graph:
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

    tmp["edges"] += new_transactions

    if use_closest_matching:
        return pair_closest_differences_first(tmp)
    else:
        return pair_largest_difference_first(tmp)


def pair_closest_differences_first(graph: Graph) -> Graph:
    """
    Takes a list of balances and tries to find number that add up to 0
    Returns a copy with all transactions minimized starting with the best matching differnces
    If none are Found, None is returned.

    Matching from the left
    """
    tmp = copy.deepcopy(graph)

    new_transactions: List[Edge] = []

    balances: List[Node] = sorted(
        list(tmp["nodes"].values()),
        key=lambda d: d["initial_net_balance"],
        reverse=True,
    )

    balances = [b for b in balances if b["current_net_balance"] != 0]

    while len(balances) > 0:
        splitting_index = next(
            (i for i, b in enumerate(balances) if b["current_net_balance"] < 0), None
        )
        if not splitting_index:
            break

        positive_balances = balances[:splitting_index]
        negative_balances = balances[splitting_index:]

        # Find the closest match
        difference = INFINITY
        current_best_match = -1
        for i in range(splitting_index, len(balances)):
            d = abs(
                positive_balances[0]["current_net_balance"]
                + balances[i]["current_net_balance"]
            )
            if d < difference:
                current_best_match = i
                difference = d

        A = balances[0]
        B = balances[current_best_match]
        a = balances[0]["current_net_balance"]
        b = balances[current_best_match]["current_net_balance"]

        # Now match first and last entry
        if a == abs(b):
            # A and B are a perfect match and cancel each other out.
            # Since A > B due to sorting, A hast to pay the amount to B to settle the debt.
            new_transactions.append({"origin": A, "destination": B, "weight": a})

            # ...  and their corresponding net_balance are updated
            tmp["nodes"][A["name"]]["current_net_balance"] = 0
            tmp["nodes"][B["name"]]["current_net_balance"] = 0

        elif a < abs(b):
            # Since |a| < |b|, A can not repay for all the money B has lent.
            new_transactions.append({"origin": A, "destination": B, "weight": a})

            # ...  and their corresponding net_balance are updated
            tmp["nodes"][A["name"]]["current_net_balance"] = 0
            tmp["nodes"][B["name"]]["current_net_balance"] = b + a

        else:  # a > abs(b)
            # Since |a| > |b|, A has to pay back more than B has lent.
            new_transactions.append({"origin": A, "destination": B, "weight": abs(b)})

            # ...  and their corresponding net_balance are updated
            tmp["nodes"][A["name"]]["current_net_balance"] = b + a
            tmp["nodes"][B["name"]]["current_net_balance"] = 0

        # afterwards these nodes are removed from the list ...
        balances = [b for b in balances if b["current_net_balance"] != 0]
        # resort
        balances = sorted(
            list(tmp["nodes"].values()),
            key=lambda d: d["current_net_balance"],
            reverse=True,
        )

    tmp["edges"] += new_transactions

    return tmp


def df_to_graph(df: pd.DataFrame, name="Nina") -> Graph:
    nodes: Dict[str, Node] = {}
    edges: List[Edge] = []

    # Im Nachhinein wäre es sooooooooo viel cleverer gewesen alle Nodes als Dict aufzubauen, aber
    # Jetzt hab ich dazu keinen Bock mehr :(

    node_names = pd.unique(df[["Giver", "Receiver"]].values.ravel("K"))

    for n in node_names:
        nodes[n] = {"name": n, "initial_net_balance": 0, "current_net_balance": 0}

    for _, row in df.iterrows():
        edges.append(
            {
                "origin": nodes[row["Giver"]],
                "destination": nodes[row["Receiver"]],
                "weight": row["Amount"],
            }
        )

    return {"name": name, "edges": edges, "nodes": nodes}


def print_edge(edge: Edge) -> None:
    print(
        f"{edge['origin']['name']} ==> {edge['destination']['name']} : {edge['weight']/100} "
    )


def print_graph(graph: Graph) -> None:

    for edge in graph["edges"]:
        print_edge(edge)


def compare_graphs(graph: Graph, edges: List[Edge]) -> None:
    for i, edge in enumerate(graph["edges"]):
        print(
            f"{edge['origin']['name']} ==> {edge['destination']['name']} : {edge['weight']} \t |  {edges[i]['origin']['name']} ==> {edges[i]['destination']['name']} : {edges[i]['weight']}"
        )


def _assert_graph_correctness(graph: Optional[Graph]) -> None:
    """
    - Asserts that all initial balances equal the new balances
    - Asserts that the overall sum is 0
    - Asserts that everybody pays only the amount they owe.
    """
    if not graph:
        assert False

    initial_negative_balances = 0
    initial_positive_balances = 0
    edge_sum = sum([w["weight"] for w in graph["edges"]])

    for n in graph["nodes"].values():
        if n["initial_net_balance"] > 0:
            initial_positive_balances += n["initial_net_balance"]
        else:
            initial_negative_balances += abs(n["initial_net_balance"])

    assert initial_positive_balances == initial_negative_balances == edge_sum

    oweing_nodes: Dict[str, int] = {}
    lending_nodes: Dict[str, int] = {}

    for n in graph["nodes"].values():
        if n["initial_net_balance"] > 0:
            oweing_nodes[n["name"]] = n["initial_net_balance"]
        else:
            lending_nodes[n["name"]] = n["initial_net_balance"]

    for e in graph["edges"]:
        lending_nodes[e["destination"]["name"]] += e["weight"]
        oweing_nodes[e["origin"]["name"]] -= e["weight"]

    for x in oweing_nodes.values():
        assert x == 0

    for x in lending_nodes.values():
        assert x == 0


def _save_graph(save_csv_path: str, graph: Optional[Graph]) -> None:
    if not graph:
        return

    df = pd.DataFrame(columns=["Giver", "Receiver", "Amount"])

    df = pd.DataFrame(
        [
            (e["origin"]["name"], e["destination"]["name"], e["weight"] / 100)
            for e in graph["edges"]
        ],
        columns=["Giver", "Receiver", "Amount"],
    )

    df.to_csv(save_csv_path, index=False)


def process_CSV(
    path_to_csv: str, save_csv_path: Optional[str] = None
) -> Optional[Graph]:
    try:
        df = pd.read_csv(path_to_csv)
        df["Amount"] = df["Amount"].astype(float).fillna(0) * 100
    except ValueError:  # Sometimes Excel uses the german decimal seperator ...
        df = pd.read_csv(path_to_csv, decimal=",")
        df["Amount"] = df["Amount"].astype(float).fillna(0) * 100

    # It is easier to do calculations using integer values to avoid rounding erros and move the decimal place afterwards.
    df["Amount"] = df["Amount"].astype(int)

    graph = df_to_graph(df, name=path_to_csv)
    graph = reduce_net_balance(graph)

    matching_algorithms: List[Callable[[Graph], Graph]] = [
        pair_largest_difference_first,
        lambda g: pair_matching_differences_first(g, False),
        lambda g: pair_matching_differences_first(g, True),
        pair_closest_differences_first,
    ]

    current_best_graph: Optional[Graph] = None
    current_best_score = INFINITY

    for a in matching_algorithms:
        tmp = a(graph)

        if len(tmp["edges"]) < current_best_score:
            current_best_score = len(tmp["edges"])
            current_best_graph = tmp

    _assert_graph_correctness(current_best_graph)

    if not current_best_graph:
        return None

    if save_csv_path:
        _save_graph(save_csv_path, graph=current_best_graph)

    return current_best_graph
