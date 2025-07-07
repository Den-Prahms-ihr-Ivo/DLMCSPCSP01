from typing import Dict


graph = {
    'A': {'B': 5, 'C': 2},
    'B': {'C': 1},
    'C': {'A': 3},
    'D': {}
}

def has_cycle_directed(graph: Dict[str, int]) -> bool:
  return False
