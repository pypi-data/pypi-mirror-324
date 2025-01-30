# Module for the creation of Pyrea structures using graphs

import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from PIL import Image
import pydot
import random
from networkx.readwrite.text import generate_network_text  # For generating text outputs

def print_graph(G):
    im_name = 'output.png'
    
    write_dot(G, 'out.dot')

    #graphs = pydot.graph_from_dot_data(file_object.getvalue())
    graphs = pydot.graph_from_dot_file('out.dot')
    graph = graphs[0]

    graph.write_png(im_name)
    return Image.open(im_name)

class MultiView():
    def __init__(self, n) -> None:
        self.n = n
        # Get some random bits, format it to hex, and take 5 chars
        self._random_names = [("%032x" % random.getrandbits(128))[:5] for _ in range(self.n)]
        self._graph = nx.DiGraph()
        self._graph.add_nodes_from(["view_%s_%s" % ((i+1), self._random_names[i]) for i in range(self.n)])

    def cluster_views(self, *args):
        
        for idx in range(self.n):
            self._graph.add_nodes_from(["clusterer_%s_%s" %((i+1), self._random_names[i]) for i in range(self.n)])
            self._graph.add_edges_from([("view_%s_%s" % ((i+1), self._random_names[i]), "clusterer_%s_%s" % ((i+1), self._random_names[i])) for i in range(self.n)])

    def fuse_views(self, *args):
        # Get a random name, save it to a variable as we need it later.
        f_rand_name = "fusion_%s" % (("%032x" % random.getrandbits(128))[:5])
        self._graph.add_node(f_rand)

        # Add edges from all leaf nodes to this node
        leaf_nodes = [x for x in self._graph.nodes() if self._graph.out_degree(x)==0 and self._graph.in_degree(x)!=0]
        self._graph.add_edges_from([(leaf_node, f_rand_name) for leaf_node in leaf_nodes])

    def print(self):
        print_graph(self._graph)


def merge(multiViews):
    # Merge all MultiViews, add new fusion node
    # TODO: Check rename parameter: https://networkx.org/documentation/stable/_modules/networkx/algorithms/operators/all.html#compose_all
    G = nx.compose_all([multiView._graph for multiView in multiViews])

    f_rand_name = "fusion_%s" % (("%032x" % random.getrandbits(128))[:5])
    G.add_node(f_rand_name)

    # Get the leaf nodes for each of the MulitViews, add edges to fusion node
    for i in range(len(multiViews)):
        leaf_nodes = [x for x in multiViews[i]._graph.nodes() if multiViews[i]._graph.out_degree(x)==0 and multiViews[i]._graph.in_degree(x)!=0]  # was in_degree(x)==0
        G.add_edges_from([(leaf_node, f_rand_name) for leaf_node in leaf_nodes])

    return G