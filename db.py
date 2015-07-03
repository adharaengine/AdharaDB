import uuid, itertools
from backends import DictionaryBackend

class Graph():
    """
    Create a graph object

    Args:
        backend (optional): Backend object.  Defaults to an im-memory
    DictionaryBackend.

    Note:
        The graph object is iterable!  Useing it as an iterator provides all the
        elements (nodes and edges) of the graph!

    Attributes:
        nodes: iterable of all the nodes in the graph
        edges: iterable of all the edges of the graph


    """
#To Do: Make more methods into properties.

    def __init__(self, backend=None):

        if backend == None:
            backend = DictionaryBackend()
        self.backend = backend
        self.node_store = backend.node_store
        self.attribute_store = backend.attribute_store
        self.edge_store = backend.edge_store
        self.weight_store = backend.weight_store
        self.commit_func = backend.commit
        self.abort_func = backend.abort
        self.direction_store = backend.direction_store
        #the default node and edge types
        self.node_type = Node
        self.edge_type = Edge


    def __iter__(self):
        """
        Returns:
            An iterator over all graph elements (nodes and edges).
        Note:
            To get just nodes or edges, use the nodes or edges properties.
        """
        #The attribute_store contains an entry for every node and edge in the graph
        return iter(self.attribute_store.keys())


    def __getitem__(self, element):
        """
        Returns:
            A dictionary containing all the attributes of element

        Args:
            element: An element(node or edge) object that belongs to the graph

        """
        return self.attribute_store[element]

    def __setitem__(self, element, attributes):
        """
        Set attributes for a node or edge.

        Args:
            element: An element (node or edge) object that belongs to the Graph
            items: A dictionary containing the attributes you want to set

        Returns:
            A dictionary containg all of the elements attributes after updating

        Note:
            The attributes in items are added with the update() method, so
            duplicate keys will be overwritten, and new keys added, but existing
            keys which aren't duplicated in item won't be overwritten.
        """
        self.attribute_store[element].update(attributes)
        self.commit()

        return self.attribute_store[element]


    @property
    def nodes(self):
        """
        Returns:
            an iterable of all the nodes in the graph
        """
        return self.node_store.keys()

    @property
    def edges(self):
        """
        Returns:
            an iterable of all the edges in the graph
        """
        return self.edge_store.keys()


    def add_node(self, attributes=None, weight=0, *args, **kwargs):
        """
        Create a node in the graph

        Args:
            attributes (optional): is an optional dict with attributes to assign to the node
            weight (optional): an integer specifying the nodes weight, defaults to 0

        Returns:
            the node object
        """

        if not attributes:
            attributes = {}

        node = self.node_type(self)
        self.node_store[node] = {}
        self.attribute_store[node] = attributes
        self.weight_store[node] = weight
        self.commit()
        return node

    def add_nodes(self, num, attributes=None, *args, **kwargs):
        """
        Adds number of nodes specified in num

        Args:
            num: is an int representing the number of nodes to add
            attributes (optional): is a dictionary of attributes to assign to each node

        Note:
            If you supply attributes, each node will have an identical copy of
            attributes applied to it.  You cannot use this method to specify
            different attributes for each node.

        returns:
            a list containing the new node objects
        """

        if not attributes:
            attributes = {}

        nodes = []

        for node in range(num):
            nodes.append(self.add_node(attributes.copy(), *args, **kwargs))
        self.commit()
        return nodes


    def add_edge(self, node1, node2, attributes=None, directed=False, weight=0, *args, **kwargs):
        """
        Creates an edge between node1 and node2.

        Args:
            node1: A node object
            node2: Another node object
            attributes (optional): dictionary of attributes to apply to the edge
            directed (optional): Boolean value, to create a directional edge,set True (False by default)
            weight (optional): an integer representing the edges initial weight

        Keyword Args:
            directional: Boolean value, to create a directional edge, you supply
            you set directional=True, this will create a directional edge from
            node1 to node2.  Node1 will be considered a neighbor (connected) of
            node2, but not vice-versa.

        returns:
            the edge object
        """

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
        self.attribute_store[edge] = attributes.copy()
        self.edge_store[edge] = (node1, node2)
        self.weight_store[edge] = weight
        self.commit()
        return edge

    def add_edges(self, edges):
        """
        Used to add multiple edges at once.

        Args:
            edges: A list of Tuples.  Each Tuple in the list contains the
            arguments to an add_edge() method call.  Thus each tuple must
            contain at least two elements- the nodes to connect, and any
            additional elements in the tuple, such as an attributes dictionary
            or directional keyword.

        returns: a list of the edges
        """
        keys = []
        for edge in edges:
            keys.append(self.add_edge(*edge))
        self.commit()
        return keys


    def del_node(self, node):
        """
        delete node

        Args:
            node: node object that is a member of the graph, to be deleted

        """
        #Note: Must create shallow copy here with copy() method
        #because we are altering the attributes dict within the node_dict
        for edge in self.node_store[node].copy():
            self.del_edge(edge)
        del self.node_store[node]
        del self.attribute_store[node]
        self.commit()

    def del_edge(self, edge):
        """
        delete edge

        Args:
            edge: edge object that is a member of the graph, to be deleted

        """
        for node in self.edge_store[edge]:
            del self.node_store[node][edge]
        del self.attribute_store[edge]
        del self.edge_store[edge]
        self.commit()

    def commit(self):
        """
        Calls the backend commit method

        Used as an integration point for transactional stores
        """
        self.commit_func

    def abort(self):
        """
        Used as an integration point for transactional stores
        """
        self.abort_func


class Element():
    """
    This is a a class for representing graph elements like nodes and edges
    It consists of an UUID as id, and behaves much like a UUID with a few
    methods for manipulating the graph

    You MUST specify the graph object that the element belongs to!

    The default Element object will use a UUID version 4.  You can use a different
    UUID version or specify a specific UUID by instantiating with the correct
    attributes (same as for a UUID object)
    """

    def __init__(self, graph, hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None):

        if [hex, bytes, bytes_le, fields, int, version].count(None) == 6:
            id = uuid.uuid4()
        else:
            id = uuid.UUID(hex, bytes, bytes_le, fields, int)

        self.__dict__['graph'] = graph
        self.__dict__['id'] = id

    def __setattr__(self, name, value):
        if name == 'weight':
            self.graph.weight_store[self] = value
        else:
            raise TypeError("'" + self.__class__.__name__ + "' objects are immutable")

    @property
    def weight(self):
        return self.graph.weight_store.get(self)

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

    def __setitem__(self, attribute, value):
        """
        Set attribute for edge.

        Args:
            attribute: the attribute to set
            value: the value to set attribute to

        """
        self.graph[self] = {attribute:value}

        return self.graph[self][attribute]
