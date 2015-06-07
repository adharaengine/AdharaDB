class DictionaryBackend():
    '''
    we use an dict to store our adjacency lists
    see https://www.python.org/doc/essays/graphs/
    '''

    def __init__(self):
        '''
        We store our data in a dictionary
        '''
        
        self.node_store = {}
        self.attribute_store = {}
        self.edge_store = {}
        self.weight_store = {}
        self.direction_store = []

    def commit(self):
        '''Simply commits the transaction'''
        pass

    def abort(self):
        '''Simply aborts the transaction'''
        pass
