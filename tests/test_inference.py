import numpy as np

from src import (
    JunctionTreeAlgorithm,
    DirectedGraph
)


def test_junction_tree_algorithm():
    graph = {
        "3":["2"],
        "2":["1","4"],
        "1":[],
        "4":[],
    }
    graph = DirectedGraph.from_dict(graph)
    factors = {
        "3":np.array([[0.4],[0.6]]),
        "2":np.array([[0.3,0.7],[0.6,0.4]]),
        "1":np.array([[0.3,0.7],[0.8,0.2]]),
        "4":np.array([[0.6,0.4],[0.9,0.1]])
    }
    factors = {n:np.log(f) for n,f in factors.items()}
    max_log_prob, max_assignment = JunctionTreeAlgorithm(graph, factors).find_max_prob_assignment()
    assert max_assignment == {"3":1,"2":0,"1":1,"4":0}
