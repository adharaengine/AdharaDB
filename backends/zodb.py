import uuid, itertools

from ZODB import FileStorage, DB
from BTrees import OOBTree
import transaction

from adhara_db import Graph


class ZODBGraph(Graph):
    '''
    A ZODB backed graph object.
    '''

    def __init__(self, storage=None, path=None):
        '''
        We store our data in a ZODB database, using BTrees
        '''
        if storage:
            db = DB(storage(path))
        else:
            db = DB(path)

        connection = db.open()
        root = connection.root

        root.node_store = OOBTree.BTree()
        root.attribute_store = OOBTree.BTree()
        root.edge_store = OOBTree.BTree()

        self.node_store = root.node_store
        self.attribute_store = root.attribute_store
        self.edge_store = root.edge_store

    def commit(self):
        '''Simply commits the transaction'''
        transaction.commit()
        
    def abort(self):
        '''Simply aborts the transaction'''
        transaction.abort()
