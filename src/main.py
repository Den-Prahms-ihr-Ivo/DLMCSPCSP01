"""
This is the only place to edit to actually use the program
It is only necessary to provide a valid path to a csv. and then run main.py
"""

from .graph_utils import process_CSV, print_graph

graph = process_CSV("<your PATH>", "<your save PATH>")
if graph:
    print_graph(graph)
else:
    print("No Graph found...")
