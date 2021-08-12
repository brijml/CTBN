    #     parent_node, edge_to_node = parents_path[curr_node]
    #     cycle = [edge_to_node.copy()]
    #     while parent_node:
    #         parent_node, edge_to_node = parents_path[parent_node]
    #         cycle.append(edge_to_node.copy())
    #     return cycle

    # def _dfs(self, adjacency_dict, curr_node, all_nodes, visited, currently_being_visited, parents_path):
    #     all_nodes.remove(curr_node); currently_being_visited.add(curr_node)
    #     adjacent_nodes = adjacency_dict[curr_node]
    #     for node in adjacent_nodes.keys():
    #         if node in visited:
    #             continue
    #         if node in currently_being_visited:
    #             parents_path[node] = (None, adjacent_nodes[node])
    #             return self._get_cycle(parents_path, curr_node)
    #         parents_path[node] = (curr_node, adjacency_dict[curr_node][node])
    #         cycle = self._dfs(adjacency_dict, node, all_nodes, visited, currently_being_visited, parents_path)
    #         if cycle:
    #             return cycle
    #     currently_being_visited.remove(curr_node); visited.add(curr_node)
    #     return None
        # edges_dict = self.as_adjacency_dict()
        # all_nodes = set(edges_dict.keys())
        # visited = set()
        # currently_being_visited = set()
        # while all_nodes:
        #     curr_node = next(iter(all_nodes))
        #     parents_path = {curr_node:(None, None)}
        #     cycle = self._dfs(edges_dict, curr_node, all_nodes, visited, currently_being_visited, parents_path)
        #     if cycle:
        #         return cycle
    # def _get_cycle(self, f_edges, b_edges):
    #     backward_edge = b_edges[0]
    #     cycle = [backward_edge.copy()]

    #     start_edge = backward_edge
    #     src, dst = start_edge.src, start_edge.dst
    #     for fe in f_edges:
    #         if start_edge.dst == fe.src:
    #             start_edge = fe 

    # def _get_cycle(self, edge_classification):
    #     for e, cls_ in edge_classification.items():
    #         if cls_ == "backward_edge":
    #             src, dst = e
    #             break
                
    #     cycle = [backward_edge.copy()]
        # edge_classification = self._classify_edges(start_times, end_times)
        # if self._has_backward_edge(edge_classification):

        # edge_classification = {}
        # for edge in self.edges:
        #     src, dst = edge.src, edge.dst
        #     if start_times[src] < start_times[dst] and end_times[src] > end_times[dst]:
        #         edge_classification[(edge.src, edge.dst)] = "forward_edge"
        #     elif start_times[src] > start_times[dst] and end_times[src] < end_times[dst]:
        #         edge_classification[(edge.src, edge.dst)] = "backward_edge"
        #     else:
        #         edge_classification[(edge.src, edge.dst)] = "cross_edge"
        # return edge_classification

    # def _has_backward_edge(self, edge_classification):
    #     return [edge for edge, cls_ in edge_classification.items() if cls_ == "backward_edge"]



    # def as_adjacency_list(self, skip_self_loops=True):
    #     adjacency_list = {node:[] for node in self.nodes}
    #     for edge in self.edges:
    #         if not (skip_self_loops and edge.src == edge.dst):
    #             adjacency_list[edge.src].append(edge.dst)
    #     return adjacency_list

# graph3 = {'1': {'2': {'weight': -58.65629316222538}, '3': {'weight': -134.56882257247685}, '4': {'weight': -110.3930713117349}, '5': {'weight': -312.0222429082561}, '6': {'weight': -244.4097418512252}}, '2': {'1': {'weight': -223.02416192140183}, '3': {'weight': -86.39640480251575}, '4': {'weight': -120.73261413670014}, '5': {'weight': -326.32313224028184}, '6': {'weight': -250.2735473716017}}, '3': {'1': {'weight': -219.21184737175884}, '2': {'weight': -38.1170799691337}, '4': {'weight': -114.00167061838843}, '5': {'weight': -334.8652821721504}, '6': {'weight': -257.1289241877284}}, '4': {'1': {'weight': -180.73127942073825}, '2': {'weight': -58.152744438124586}, '3': {'weight': -125.16216782794595}, '5': {'weight': -321.30412777040976}, '6': {'weight': -257.6065658892938}}, '5': {'1': {'weight': -197.74116330060207}, '2': {'weight': -54.31058099811656}, '3': {'weight': -140.8360393775281}, '4': {'weight': -112.79096037476734}, '6': {'weight': -172.32179905339314}}, '6': {'1': {'weight': -207.02193893318284}, '2': {'weight': -54.82387973443662}, '3': {'weight': -137.28158772329357}, '4': {'weight': -119.23067486219821}, '5': {'weight': -251.8923419857573}}, 'root': {'1': {'weight': -225.36645581157322}, '2': {'weight': -58.76487839368517}, '3': {'weight': -143.25069583543956}, '4': {'weight': -122.25165643864727}, '5': {'weight': -335.3360393605773}, '6': {'weight': -263.2931668173251}}}
# graph3 = DirectedGraph.from_dict(graph3)
