
import uuid, itertools

class Graph():
    '''
    A base graph object.
    '''

    def __init__(self):
        '''
        we use an dict to store our adjacency lists
        see https://www.python.org/doc/essays/graphs/
        '''
        self.node_store = {}
        self.attribute_store = {}
        self.edge_store = {}

    def add_node(self, attributes=None):
        '''
        Creates a node.
        A UUID is generated and it becomes the node
        attributes is an optional dict with attributes
        of the node
        Returns the node (UUID).
        '''

        if not attributes:
            attributes = {}

        key = uuid.uuid4()
        self.node_store[key] = {}
        self.attribute_store[key] = attributes
        self.commit()
        return key

    def add_nodes(self, num, attributes=None):
        '''
        num is an int
        attributes is a dict of attributes to be applied to each node
        adds num nodes
        returns a list of the new nodes
        '''

        if not attributes:
            attributes = {}

        n = range(num)
        keys = []

        for node in n:
            keys.append(self.add_node({'test':1,'key':'value'}))
        self.commit()
        return keys

    def nodes(self):
        '''
        Returns an iterable of all the nodes in the graph
        '''
        #We don't want to return 'edges' and 'attributes',
        #as they are not in fact nodes
        nodes = itertools.filterfalse(
            #lambda n: n == 'attributes' or 'edges',
            lambda n: False == isinstance(n, type(uuid.uuid4())),
            self.node_store.keys())
        return nodes

    def edges(self):
        '''
        returns an iterable of all the edges in the graph
        '''
        return self.edge_store.keys()

    def add_edge(self, node1, node2, attributes=None):
        '''
        Creates an edge between node1 and node2.
        attributes can be a dict of attributes to apply to the each edge
        returns the edge key (a UUID)
        '''

        if not attributes:
            attributes = {}

        if not isinstance(attributes, dict):
            raise ValueError('attributes must be a dict')

        key = uuid.uuid4()
        self.node_store[node1][key] = node2
        self.node_store[node2][key] = node1
        self.attribute_store[key] = attributes
        self.edge_store[key] = (node1, node2)
        self.commit()
        return key

    def add_edges(self, edges):
        '''
        Takes an iterable of 2-tuples or 3-tuples where
        the first two elements of the tuples specify the node keys
        to connect, and if present, the third element is a dict of
        attributes for the edge
        returns a list of the edge keys
        '''
        keys = []
        for edge in edges:
            keys.append(self.add_edge(*edge))
        self.commit()
        return keys

    def get_neighbors(self, key):
        '''
        key is a node key
        returns iterable of the neighbors of key
        '''
        return self.node_store[key].values()

    def get_attributes(self, key):
        '''
        Takes key which is a node or edge and
        returns a dict of the node or edge attributes
        '''
        return self.attribute_store[key]

    def add_attributes(self, key, **kwargs):
        '''
        key is a node or edge
        **kwargs are key=value attributes to apply to key
        '''
        self.commit()
        self.attribute_store[key].update(kwargs)

    def del_node(self, key):
        '''
        key is a node key
        deletes the node represented by key
        '''
        #Note: Must create shallow copy here with copy() method
        #because we are altering the attributes dict within the node_dict
        for edge in self.node_store[key].copy():
            self.del_edge(edge)
        del self.node_store[key]
        del self.attribute_store[key]
        self.commit()

    def del_edge(self, key):
        '''
        key is an edge key
        deletes the edge represented by key
        '''
        for node in self.edge_store[key]:
            del self.node_store[node][key]
        del self.attribute_store[key]
        del self.edge_store[key]
        self.commit()

    def commit(self):
        '''
        Provides a hook for Transactional capable storage engines
        Over-ride this method to perform a proper commit
        '''
        pass

    def abort(self):
        '''
        Provides a hook for Transactional capable storage engines
        Over-ride this method to abort a transaction
        '''
        pass
