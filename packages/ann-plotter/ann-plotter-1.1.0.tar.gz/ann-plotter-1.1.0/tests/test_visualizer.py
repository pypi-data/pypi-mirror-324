import unittest
from ann_visualizer.visualizer import Visualizer

class TestVisualizer(unittest.TestCase):
    def test_layer_count(self):
        vis = Visualizer([2, 3, 1])
        self.assertEqual(len(vis.layer_sizes), 3)

    def test_node_count(self):
        vis = Visualizer([2, 3, 1])
        self.assertEqual(len(vis.graph.nodes), 6)

if __name__ == '__main__':
    unittest.main()
