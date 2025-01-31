import matplotlib.pyplot as plt
import networkx as nx

class Visualizer:
    def __init__(self, layer_sizes):
        self.layer_sizes = layer_sizes
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        positions = {}
        node_counter = 0
        for layer, num_nodes in enumerate(self.layer_sizes):
            for node in range(num_nodes):
                self.graph.add_node(node_counter, layer=layer)
                positions[node_counter] = (layer, -node)
                node_counter += 1

        prev_layer_start = 0
        for i in range(len(self.layer_sizes) - 1):
            curr_layer_start = prev_layer_start + self.layer_sizes[i]
            for j in range(self.layer_sizes[i]):
                for k in range(self.layer_sizes[i + 1]):
                    self.graph.add_edge(prev_layer_start + j, curr_layer_start + k)
            prev_layer_start = curr_layer_start

        self.positions = positions

    def draw(self):
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos=self.positions, with_labels=True, node_size=700, node_color="skyblue", edge_color="gray")
        plt.title("Artificial Neural Network Visualization")
        plt.show()
