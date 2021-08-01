from copy import deepcopy
from .graph_preliminaries import (
    DirectedEdge,
    DirectedGraph
)

"""
Implementation of the Chu-Liu-Edmonds algorithm to find the maximum spannng arborescence
"""

class ChuLiuEdmonds:

    def __init__(self, root_node="root"):
        self.cycle_node_prefix = "c"
        #There are only outgoing edges from a root node and no incoming edge
        #We need to have such a node for algorithm to find the right answer.
        self.root_node = root_node

    def _get_max_edges_graph(self, graph):
        max_edges = []
        incident_view = graph.get_incident_view()
        for node in graph.nodes:
            if node == self.root_node: continue
            incident_edges = incident_view[node]
            max_edge = max(incident_edges.values(), key=lambda edge:edge.weight)
            max_edges.append(max_edge.copy())
        return DirectedGraph(deepcopy(graph.nodes), max_edges)

    def _get_outgoing_edges_from_cycle(self, orig_graph_edges, cycle_nodes, non_cycle_nodes, cycle_node):
        outgoing_edges = []
        for node in non_cycle_nodes:
            if node == self.root_node: continue
            outgoing_edges_from_cycle = [edge for edge in orig_graph_edges if edge.dst == node and edge.src in cycle_nodes]
            max_edge = max(outgoing_edges_from_cycle, key=lambda edge:edge.weight)
            new_edge = DirectedEdge(
                src=cycle_node, 
                dst=node, 
                weight=max_edge.weight, 
                original_edge=max_edge
            )
            outgoing_edges.append(new_edge)
        return outgoing_edges

    def _get_cycle_weight(self, cycle):
        return sum([edge.weight for edge in cycle])

    def _get_kicked_out_edge(self, dst, cycle):
        for edge in cycle:
            if edge.dst == dst:
                return edge

    def _get_incoming_edges_to_cycle(self, graph, cycle, cycle_node, cycle_nodes, non_cycle_nodes):
        graph_as_dict = graph.as_adjacency_dict()
        cycle_weight = self._get_cycle_weight(cycle)
        incoming_edges = []
        for src in non_cycle_nodes:
            incoming_edges_to_cycle = []
            for dst in cycle_nodes:
                incoming_edge = graph_as_dict[src][dst]
                kicked_out_edge = self._get_kicked_out_edge(dst, cycle)
                adjusted_weight = cycle_weight-kicked_out_edge.weight+incoming_edge.weight
                adjusted_edge = DirectedEdge(
                    src=src, 
                    dst=cycle_node, 
                    weight=adjusted_weight, 
                    original_edge=incoming_edge,
                    kicked_out_edge=kicked_out_edge
                )
                incoming_edges_to_cycle.append(adjusted_edge)
            max_edge = max(incoming_edges_to_cycle, key=lambda e:e.weight)
            incoming_edges.append(max_edge)
        return incoming_edges
    
    def _get_expanded_cycle_edges(self, cycle, kicked_out_edges):
        return [edge for edge in cycle if edge not in kicked_out_edges]

    def _get_nodes_in_expanded_graph(self, contracted_graph, cycle, cycle_node):
        cycle_nodes = set([e.src for e in cycle])
        new_nodes = deepcopy(contracted_graph.nodes)
        new_nodes.remove(cycle_node)
        return new_nodes.union(cycle_nodes)

    def _get_expanded_non_cycle_edges(self, contracted_graph, cycle_node):
        non_cycle_edges, kicked_out_edges = [], []
        for edge in contracted_graph.edges:
            if edge.src == cycle_node:
                new_edge = edge.original_edge.copy()
            elif edge.dst == cycle_node:
                new_edge = edge.original_edge.copy()
                kicked_out_edges.append(edge.kicked_out_edge)
            else:
                new_edge = edge.copy()
            non_cycle_edges.append(new_edge)
        return non_cycle_edges, kicked_out_edges

    def _contract_cycle(self, graph, cycle, cycle_node):
        cycle_nodes = set([e.src for e in cycle])
        non_cycle_nodes = set([v for v in graph.nodes if v not in cycle_nodes])
        non_cycle_edges = [edge.copy() for edge in graph.edges if not (edge.src in cycle_nodes or edge.dst in cycle_nodes)]
        edges_from_cycle = self._get_outgoing_edges_from_cycle(graph.edges, cycle_nodes, non_cycle_nodes, cycle_node)
        edges_to_cycle = self._get_incoming_edges_to_cycle(graph, cycle, cycle_node, cycle_nodes, non_cycle_nodes)
        non_cycle_nodes.add(cycle_node)
        all_edges = non_cycle_edges + edges_from_cycle + edges_to_cycle
        contracted_graph = DirectedGraph(non_cycle_nodes, all_edges)
        return contracted_graph

    def _expand_cycle(self, contracted_graph, cycle, cycle_node):
        expanded_nodes = self._get_nodes_in_expanded_graph(contracted_graph, cycle, cycle_node)
        non_cycle_edges, kicked_out_edges = self._get_expanded_non_cycle_edges(contracted_graph, cycle_node)
        cycle_edges = self._get_expanded_cycle_edges(cycle, kicked_out_edges)
        all_edges = cycle_edges + non_cycle_edges
        return DirectedGraph(expanded_nodes, all_edges)

    def find_msa(self, graph, cycle_count=0):
        max_edges_graph = self._get_max_edges_graph(graph)
        cycle = max_edges_graph.detect_cycle()
        if cycle:
            cycle_node = self.cycle_node_prefix + str(cycle_count)
            contracted_graph = self._contract_cycle(graph, cycle, cycle_node)
            max_edges_contracted_graph = self.find_msa(contracted_graph, cycle_count+1)
            expanded_graph = self._expand_cycle(max_edges_contracted_graph, cycle, cycle_node)
            return expanded_graph
        else:
            return max_edges_graph

if __name__ == "__main__":
    graph = {
        "root":{"john":{"weight":9}, "saw":{"weight":10}, "mary":{"weight":9}},
        "john":{"saw":{"weight":20}, "mary":{"weight":3},"john":{"weight":0}},
        "saw":{"john":{"weight":30}, "mary":{"weight":30},"saw":{"weight":0}},
        "mary":{"saw":{"weight":0}, "john":{"weight":11},"mary":{"weight":0}}
    }
    graph1 = DirectedGraph.from_dict(graph)
    graph2 = {
        "root":{"v1":{"weight":5}, "v2":{"weight":1}, "v3":{"weight":1}},
        "v1":{"v2":{"weight":11}, "v3":{"weight":4},"v1":{"weight":0}},
        "v2":{"v1":{"weight":10}, "v3":{"weight":5},"v2":{"weight":0}},
        "v3":{"v2":{"weight":8}, "v1":{"weight":9},"v3":{"weight":0}}        
    }
    graph2 = DirectedGraph.from_dict(graph2)
    out_graph = ChuLiuEdmonds().find_msa(graph2)
    print(out_graph.detect_cycle())
    print(out_graph.edges)