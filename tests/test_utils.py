# type: ignore
import pytest

from src import utils
from data.test_graphs import TEST_GRAPHS

class TestUtils:
    
    @pytest.mark.parametrize("graph, expected", [(TEST_GRAPHS['has_no_cycle'], False)])
    def test_has_cycle_directed(self, graph, expected):
        assert utils.has_cycle_directed(graph) == expected

