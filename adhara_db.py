
import uuid, itertools

from backends.in_memory import DictionaryBackend

class Graph():
    '''
    A graph object.
    backend is a backend class
    '''
#To Do: Make more methods into properties.

    def __init__(self, backend=DictionaryBackend):
        '''
        We setup our graph object to use the storage backend
        '''
        #we have to create our backend object
        self.backend = backend()

        self.node_store = self.backend.node_store
        self.attribute_store = self.backend.attribute_store
        self.edge_store = self.backend.edge_store
        self.commit_func = self.backend.commit
        self.abort_func = self.backend.abort
        self.direction_store = self.backend.direction_store
        #the default node and edge types
        self.node_type = Node
        self.edge_type = Edge


    def __iter__(self):
        '''
        By iterating over our graph, we get both nodes and edges.
        To get just nodes or edges, use the nodes or edges properties.
        '''
        #The attribute_store contains an entry for every node and edge in the graph
        return iter(self.attribute_store.keys())


    def __getitem__(self, element):
        '''
        Retrieves the attribute dictionary of the node or edge represented by key
        '''
        return self.attribute_store[element]

    def __setitem__(self, element, item):
        '''
        Set attributes for a node or edge.  ::item:: should be a dictionary
        '''
        self.attribute_store[element].update(item)
        self.commit()

        return self.attribute_store[element]


    @property
    def nodes(self):
        '''
        Returns an iterable of all the nodes in the graph
        '''
        return self.node_store.keys()

    @property
    def edges(self):
        '''
        returns an iterable of all the edges in the graph
        '''
        return self.edge_store.keys()


    def add_node(self, attributes=None, *args, **kwargs):
        '''
        Creates a node.
        A UUID is generated and it becomes the node
        attributes is an optional dict with attributes
        of the node
        Returns the node (UUID).
        '''

        if not attributes:
            attributes = {}

        node = self.node_type(self)
        self.node_store[node] = {}
        self.attribute_store[node] = attributes
        self.commit()
        return node

    def add_nodes(self, num, attributes=None, *args, **kwargs):
        '''
        num is an int
        attributes is a dict of attributes to be applied to each node
        adds num nodes
        returns a list of the new nodes
        '''

        if not attributes:
            attributes = {}

        nodes = []

        for node in range(num):
            nodes.append(self.add_node({'test':1,'key':'value'}, *args, **kwargs))
        self.commit()
        return nodes


    def add_edge(self, node1, node2, attributes=None, directed=False, *args, **kwargs):
        '''
        Creates an edge between node1 and node2.
        attributes can be a dict of attributes to apply to the each edge
        returns the edge
        '''

        if not attributes:
            attributes = {}

        if not isinstance(attributes, dict):
            raise ValueError('attributes must be a dict')

        edge = self.edge_type(self)
        self.node_store[node1][edge] = node2
        if directed:
            self.direction_store.append(edge)
        else:
            self.node_store[node2][edge] = node1
        self.attribute_store[edge] = attributes
        self.edge_store[edge] = (node1, node2)
        self.commit()
        return edge

    def add_edges(self, edges):
        '''
        Takes an iterable of 2-tuples or 3-tuples where
        the first two elements of the tuples specify the nodes
        to connect, and if present, the third element is a dict of
        attributes for the edge
        returns a list of the edges
        '''
        keys = []
        for edge in edges:
            keys.append(self.add_edge(*edge))
        self.commit()
        return keys


    def del_node(self, node):
        '''
        deletes the node represented by node
        '''
        #Note: Must create shallow copy here with copy() method
        #because we are altering the attributes dict within the node_dict
        for edge in self.node_store[node].copy():
            self.del_edge(edge)
        del self.node_store[node]
        del self.attribute_store[node]
        self.commit()

    def del_edge(self, edge):
        '''
        deletes the edge represented by edge
        '''
        for node in self.edge_store[edge]:
            del self.node_store[node][edge]
        del self.attribute_store[edge]
        del self.edge_store[edge]
        self.commit()

    def commit(self):
        '''
        Calls the backend commit method (if supported)
        '''
        self.commit_func

    def abort(self):
        '''
        calls the backend abort function (if supported)
        '''
        self.abort_func


class Element():
    '''
    This is a a class for representing graph elements like nodes and edges
    It consists of an UUID as id, and behaves much like a UUID with a few
    methods for manipulating the graph

    You MUST specify the graph object that the element belongs to!

    The default Element object will use a UUID version 4.  You can use a different
    UUID version or specify a specific UUID by instantiating with the correct
    attributes (same as for a UUID object)
    '''

    def __init__(self, graph, hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None):

        if [hex, bytes, bytes_le, fields, int, version].count(None) == 6:
            id = uuid.uuid4()
        else:
            id = uuid.UUID(hex, bytes, bytes_le, fields, int)

        self.__dict__['graph'] = graph
        self.__dict__['id'] = id

    def __eq__(self, other):
        try:
            return self.id == other.id
        except ValueError:
            return NotImplemented
        except TypeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return self.id != other.id
        except ValueError:
            return NotImplemented
        except TypeError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self.id < other.id
        except ValueError:
            return NotImplemented
        except TypeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.id > other.id
        except ValueError:
            return NotImplemented
        except TypeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.id <= other.id
        except ValueError:
            return NotImplemented
        except TypeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.id >= other.id
        except ValueError:
            return NotImplemented
        except TypeError:
            return NotImplemented

    def __hash__(self):
        return self.id.__hash__()

    def __repr__(self):
        return 'Element(%r)' % str(self)

    def __setattr__(self, name, value):
        raise TypeError("'" + self.__class__.__name__ + "' objects are immutable")

    def __str__(self):
        return self.id.__str__()


class Node(Element):
    '''
    Implements a Node element
    '''

    def delete(self):
        self.graph.del_node(self)

    @property
    def neighbors(self):
        return self.graph.node_store[self].values()

    @property
    def edges(self):
        return self.graph.node_store[self].keys()

    def __iter__(self):
        '''
        By iterating over our node, we get both the node's neighbors and edges.
        To get just nodes or edges, use the neighbors or edges properties.
        '''
        return itertools.chain(self.neighbors, self.edges)


    def __getitem__(self, attribute):
        '''
        Retrieves the attribute attribute of the node
        '''
        return self.graph[self][attribute]

    def __setitem__(self, attribute, item):
        '''
        Set attribute for node  ::item:: should be a dictionary
        '''
        self.graph[self] = {attribute:item}

        return self.graph[self][attribute]


class Edge(Element):
    '''
    Implements a Edge element
    '''

    def delete(self):
        self.graph.del_edge(self)

    @property
    def nodes(self):
        return self.graph.edge_store[self]

    @property
    def directed(self):
        if self in self.graph.direction_store:
            return True
        else:
            return False

    def __iter__(self):
        '''
        By iterating over our edge, we get the nodes the edge connects to.
        Same as if we called the nodes() method.
        '''
        return iter(self.nodes)

    def __getitem__(self, attribute):
        '''
        Retrieves the attribute attribute of the edge
        '''
        return self.graph[self][attribute]

    def __setitem__(self, attribute, item):
        '''
        Set attribute for edge.  ::item:: should be a dictionary
        '''
        self.graph[self] = {attribute:item}

        return self.graph[self][attribute]
