from copy import deepcopy


class Node:

    def __init__(self, label):
        self.label = label

    def __eq__(self, other_node):
        return self.label == other_node.label

class Cycle(Node):

    def __init__(self, label, nodes, edges):
        super().__init__(label)
        self.nodes = nodes
        self.edges = edges


class DirectedEdge:

    def __init__(self, src, dst, **kwargs):
        self.src = src
        self.dst = dst
        self.weight = kwargs.get("weight", None)
        self.kicked_out_edge = kwargs.get("kicked_out_edge", None)
        self.original_edge = kwargs.get("original_edge", None)

    def __repr__(self):
        if self.weight:
            return "{0}-{1:.2f}->{2}".format(self.src, self.weight, self.dst)
        else:
            return "{0}--->{1}".format(self.src, self.dst)

    def __eq__(self, other_edge):
        return self.src == other_edge.src and self.dst == other_edge.dst

    def copy(self):
        return deepcopy(self)

class DirectedGraph:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        
    @classmethod
    def from_dict(cls, graph_as_dict):
        nodes = set(graph_as_dict.keys())
        edges = []
        for src, adjacent_nodes in graph_as_dict.items():
            if isinstance(adjacent_nodes, dict):
                for dst, attributes in adjacent_nodes.items():
                    edges.append(DirectedEdge(src, dst, **attributes))
            elif isinstance(adjacent_nodes, list):
                for dst in adjacent_nodes:
                    edges.append(DirectedEdge(src, dst))
        return cls(nodes, edges)

    def _get_empty_adjacency_dict(self):
        return {node:{} for node in self.nodes}
    
    def as_adjacency_dict(self, copy_edge=False):
        edge_dict = self._get_empty_adjacency_dict()
        for edge in self.edges:
            edge_dict[edge.src][edge.dst] = edge.copy() if copy_edge else edge
        return edge_dict
    
    def get_incident_view(self, copy_edge=False):
        incident_view = self._get_empty_adjacency_dict()
        for edge in self.edges:
            incident_view[edge.dst][edge.src] = edge.copy() if copy_edge else edge
        return incident_view

    def _get_cycle(self, b_edges, parents):
        b_edge = b_edges[0]
        cycle = [b_edge.copy()]
        edge_dict = self.as_adjacency_dict()
        start_node = b_edge.src
        while parents[start_node]:
            src, dst = parents[start_node], start_node
            cycle.append(edge_dict[src][dst].copy())
            start_node = parents[start_node]
        return cycle

    def detect_cycle(self):
        start_times, end_times, parents = self._get_dfs_forest()
        f_edges, b_edges, c_edges = self._classify_edges(start_times, end_times)
        if b_edges:
           cycle = self._get_cycle(b_edges, parents)
           return cycle
        else:
            return None
    
    def _dfs(self, edges_dict, curr_node, start_times, end_times, colours, parents, time):
        colours[curr_node] = "gray"
        time+=1
        start_times[curr_node] = time
        adjacent_nodes = edges_dict[curr_node]
        for node in adjacent_nodes.keys():
            if colours[node] == "white":
                parents[node] = curr_node
                time = self._dfs(edges_dict, node, start_times, end_times, colours, parents, time)
        time+=1
        end_times[curr_node] = time
        colours[curr_node] = "black"
        return time

    def _get_dfs_forest(self):
        start_times, end_times = {}, {}
        edges_dict = self.as_adjacency_dict()
        colours = {node:"white" for node in self.nodes}
        parents = {node:None for node in self.nodes}
        time = 0
        for node in edges_dict.keys():
            if colours[node] == "white":
                time = self._dfs(edges_dict, node, start_times, end_times, colours, parents, time)
        return start_times, end_times, parents

    def _classify_edges(self, start_times, end_times):
        forward_edges, backward_edges, cross_edges = [], [], []
        for edge in self.edges:
            src, dst = edge.src, edge.dst
            if start_times[src] < start_times[dst] and end_times[src] > end_times[dst]:
                forward_edges.append(edge)
            elif start_times[src] > start_times[dst] and end_times[src] < end_times[dst]:
                backward_edges.append(edge)
            else:
                cross_edges.append(edge)
        return forward_edges, backward_edges, cross_edges

    def _sort_nodes(self, end_times):
        return sorted(end_times, key=end_times.get, reverse=True)

    def _parents_from_edge_classification(self, f_edges, c_edges):
        parents = {n:None for n in self.nodes}
        for e in f_edges:
            parents[e.dst] = e.src
        
        for e in c_edges:
            parents[e.dst] = e.src
        return parents

    def get_topological_order(self):
        start_times, end_times, parents = self._get_dfs_forest()
        f_edges, b_edges, c_edges = self._classify_edges(start_times, end_times)
        if not b_edges:
            parents = self._parents_from_edge_classification(f_edges, c_edges)
            return self._sort_nodes(end_times), parents 
        else:
            raise Exception("The graph is not acyclic.")


if __name__ == "__main__":
    graph = {
        "1":["3","2"],
        "2":["3","4"],
        "3":["4"],
        "4":[]
    }
    graph = DirectedGraph.from_dict(graph)
    print(graph.detect_cycle())
    print(graph.get_topological_order())