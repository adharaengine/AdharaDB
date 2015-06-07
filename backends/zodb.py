from BTrees import OOBTree
import transaction


class ZODBBTreeBackend():
    '''
    A ZODB backed graph object.
    '''

    def __init__(self, root):
        '''
        We store our data in a ZODB database, using BTrees
        '''
        root.node_store = OOBTree.BTree()
        root.attribute_store = OOBTree.BTree()
        root.edge_store = OOBTree.BTree()
        root.weight_store = OOBTree.BTree()
        root.direction_store = TreeSet()

        self.node_store = root.node_store
        self.attribute_store = root.attribute_store
        self.edge_store = root.edge_store
        self.weight_store = root.weight_store
        self.direction_store = root.direction_store

    def commit(self):
        '''Simply commits the transaction'''
        transaction.commit()

    def abort(self):
        '''Simply aborts the transaction'''
        transaction.abort()


class TreeSet(OOBTree.TreeSet):
    '''
    The provided TreeSet does not support append, so I have added
    it here :)
    '''

    def append(self, key):
        self.add(key)
