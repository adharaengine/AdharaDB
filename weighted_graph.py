from db import Graph, Element, Node, Edge

class WeightedGraph(Graph):
    '''
    This class implements a weighted graph
    In addition to the traditional weighting of edges,
    we also store weights for nodes!
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.weight_store = self.backend.weight_store
        self.node_type = WeightedNode
        self.edge_type = WeightedEdge

    def add_node(self, *args, **kwargs):
        node = super().add_node(*args, **kwargs)
        self.weight_store[node] = kwargs.get('weight', 0)

        return node

    def add_edge(self, *args, **kwargs):
        edge = super().add_edge(*args, **kwargs)
        self.weight_store[edge] = kwargs.get('weight', 0)

        return edge

class WeightedElement(Element):
    '''
    Implements a WeightedElement
    '''

    @property
    def weight(self):
        return self.graph.weight_store.get(self)

    def __setattr__(self, name, value):
        if name == 'weight':
            self.graph.weight_store[self] = value
        else:
            raise TypeError("'" + self.__class__.__name__ + "' objects are immutable")


class WeightedNode(WeightedElement, Node):
    '''
    creates a weighted node
    '''
    pass


class WeightedEdge(WeightedElement, Edge):
    '''
    creates a weighted edge
    '''
    pass
