import numpy as np
from copy import deepcopy

from .parameter_learning_models import LRModel
from .graph_preliminaries import DirectedGraph
from .msa import ChuLiuEdmonds
from .inference import JunctionTreeAlgorithm


PARAMETER_STATEGIES = {
    "lr":LRModel
}

class Utils:
    
    @staticmethod
    def get_column_vector(array):
        return np.expand_dims(array, axis=1)

    @staticmethod
    def get_row_vector(array):
        return np.expand_dims(array, axis=0)


class CTBN:

    def __init__(self, parameter_strategy="lr"):
        self.parameter_strategy = parameter_strategy
        self.optimal_graph = None
        self.root_node = "root" #this is a special node to represent self-loops

    def _generate_graph(self, X, Y):
        num_nodes = Y.shape[1]
        all_nodes = [self.root_node] + [str(i+1) for i in range(num_nodes)]
        cpts = {n:{} for n in all_nodes}
        graph_dict = {n:{} for n in all_nodes}
        for i in range(num_nodes):
            for j in range(num_nodes):
                dst_node = str(j+1)
                if i == j:
                    src_node = self.root_node
                    models, edge_weight = LRModel.get_cll(X, Y[:,j])
                else:
                    src_node = str(i+1)
                    X_temp = np.hstack([
                        X, Utils.get_column_vector(Y[:,i])
                    ])
                    models, edge_weight = LRModel.get_cll_with_parents(X_temp, Y[:,j])
                cpts[src_node][dst_node] = models
                graph_dict[src_node][dst_node] = {"weight":edge_weight}
        return cpts, graph_dict

    def _remove_root_node(self):
        nodes = deepcopy(self.optimal_graph.nodes)
        nodes.remove(self.root_node)
        edges = [e.copy() for e in self.optimal_graph.edges if e.src != self.root_node]
        return DirectedGraph(nodes, edges)

    def fit(self, X, Y):
        self.cpts, complete_graph_dict = self._generate_graph(X, Y)
        graph = DirectedGraph.from_dict(complete_graph_dict)
        self.optimal_graph = ChuLiuEdmonds().find_msa(graph)
        return
    
    def _get_factors(self, X):
        factors = {}
        for edge in self.optimal_graph.edges:
            models = self.cpts[edge.src][edge.dst]
            if edge.src == self.root_node:
                sample = Utils.get_row_vector(X)
                factors[edge.dst] = models.predict_log_proba(sample).T
            else:
                factor = np.zeros((2,2))
                for val in (0,1):
                    sample = Utils.get_row_vector(
                        np.hstack([X, [val]])
                    )
                    factor[val] = models[val].predict_log_proba(sample)
                factors[edge.dst] = factor
        return factors

    def predict(self, X):
        assert self.optimal_graph, "The model is not fit to the dataset yet. Please run the fit method."
        factors = self._get_factors(X)
        graph = self._remove_root_node()
        max_prob, prediction = JunctionTreeAlgorithm(graph, factors).find_max_prob_assignment()
        return max_prob, prediction
