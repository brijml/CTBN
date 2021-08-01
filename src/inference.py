import numpy as np


class JunctionTreeAlgorithm():
    
    def __init__(self, graph, factors):
        self.graph = graph
        ##Note the factors must have log probability values
        self.factors = factors

    def _fill_factors_in_buckets(self):
        return {var:[cpt] for var, cpt in self.factors.items()}

    def _sum(self, factors):
        return sum(factors)

    def _max_out(self, message):
        message = np.amax(message, axis=1)
        ##message is a single dimensional array, make it a column vector
        return np.expand_dims(message, axis=1)

    def _pass_messages_from_leaf_to_root(self, ordering, parents):
        for node in ordering[::-1]:
            factors = self.buckets[node]
            message = self._sum(factors)
            self.buckets[node] = message
            parent_node = parents[node]
            if parent_node:
                message = self._max_out(message)
                self.buckets[parent_node].append(message)
        return

    def _pass_messages_from_root_to_leaf(self, ordering, parents):
        root = ordering[0]
        max_log_prob = np.max(self.buckets[root])
        max_assignment_root = np.argmax(self.buckets[root])
        max_assignment = {root:max_assignment_root}
        for node in ordering[1:]:
            factor = self.buckets[node]
            max_assignment_parent = max_assignment[parents[node]]
            max_log_prob+=np.max(factor[max_assignment_parent])
            max_assignment[node] = np.argmax(factor[max_assignment_parent])
        return max_log_prob, max_assignment

    def find_max_prob_assignment(self):
        self.buckets = self._fill_factors_in_buckets()
        ordering, parents = self.graph.get_topological_order()
        self._pass_messages_from_leaf_to_root(ordering, parents)        
        max_prob, max_assignment = self._pass_messages_from_root_to_leaf(ordering, parents)
        return max_prob, max_assignment