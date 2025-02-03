import json
from collections import defaultdict
from scope.dtos import CallGraph

try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class FileGraph(object):
    def __init__(self, callgraph: CallGraph):
        self.filegraph = self._build(callgraph)

    def __str__(self):
        num_nodes = len(self.filegraph.keys())
        num_edges = sum([len(edges) for edges in self.filegraph.values()])
        return f"FileGraph(num_nodes={num_nodes}, num_edges={num_edges})"

    def _build(self, callgraph: CallGraph):
        filegraph = defaultdict(list)
        for defn in callgraph.definitions():
            referenced_by_paths = {ref.path for ref in defn.referenced_by}
            filegraph[defn.path].extend(referenced_by_paths)
        for path in filegraph.keys():
            # remove self-referencing nodes, for now
            unique_paths = list(set(filegraph[path]))
            unique_paths = [p for p in unique_paths if p != path]
            filegraph[path] = unique_paths
        return filegraph

    def graphviz(self):
        dot_elements = ["digraph FileGraph {", "    node [shape=box];"]
        # Add all edges
        for source_file, target_files in self.filegraph.items():
            # Clean file paths for graphviz labels
            source_node = source_file.replace("/", "_").replace(".", "_")
            # Add source node with label
            dot_elements.append(f'    {source_node} [label="{source_file}"];')
            # Add edges to all files that reference this one
            for target in target_files:
                target_node = target.replace("/", "_").replace(".", "_")
                dot_elements.append(f"    {source_node} -> {target_node};")
        dot_elements.append("}")
        return "\n".join(dot_elements)
    
    def cluster(self):
        if not HAS_NETWORKX:
            raise ImportError("FileGraph.cluster not supported. Please install scope extras w/ pip install codescope[extras].")
        adj_matrix = []
        for source, target_files in self.filegraph.items():
            adj_matrix.append([1 if target in target_files else 0 for target in target_files])
        adj_matrix = nx.from_numpy_array(adj_matrix)
        communities = nx.community.greedy_modularity_communities(adj_matrix)
        # TODO: revert back to original file paths
        return communities

    
    def mermaid(self):
        pass

    def to_dict(self):
        return self.filegraph

    def json(self):
        return json.dumps(self.to_dict())
