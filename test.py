import unittest
import tempfile

from tempfile import NamedTemporaryFile
from ZODB import DB, config
from ZODB.FileStorage import FileStorage

from db import Graph, Element, Edge, Node
from weighted_graph import WeightedGraph, WeightedElement, WeightedNode, WeightedEdge
from backends import DictionaryBackend, ZODBBTreeBackend


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph(DictionaryBackend())

    def test_iter_(self):
        elements = self.g.add_nodes(4)
        elements.append(self.g.add_edge(elements[0], elements[1],{'keye':'valuee'}))
        elements.append(self.g.add_edge(elements[0], elements[2],{'keye':'valuee'}))

        self.assertEqual(len(elements),6)
        for n in self.g:
            self.assertIsInstance(n, Element)
            self.assertIn(n, elements)

    def test_getersetter_(self):
        node = self.g.add_node({'keyn':'valuen'})
        self.g[node] = {'keyn2':'valuen2'}
        self.assertEqual(self.g[node], {'keyn':'valuen','keyn2':'valuen2'})

    def test_add_node(self):
        n = self.g.add_node()
        self.assertIsInstance(n, Element)
        for node in self.g.nodes:
            self.assertIsInstance(node, Element)
        self.assertIn(n, self.g.nodes)

    def test_add_nodes(self):
        nodes = self.g.add_nodes(4)
        self.assertIsInstance(nodes,list)
        self.assertEqual(len(nodes),4)
        for n in nodes:
            self.assertIsInstance(n, Element)

    def test_nodes(self):
        self.g.add_nodes(5)
        for n in self.g.nodes:
            self.assertIsInstance(n, Element)

    def test_add_edge(self):
        nodes = self.g.add_nodes(5)
        for idx, val in enumerate(nodes):
            try:
                self.g.add_edge(val,nodes[idx+1])
            except IndexError:
                pass
        for e in self.g.edges:
            self.assertIsInstance(e, Element)
            self.assertFalse(e.directed)

    def test_add_directed_edge(self):
        nodes = self.g.add_nodes(5)
        for idx, val in enumerate(nodes):
            try:
                self.g.add_edge(val,nodes[idx+1],directed=True)
            except IndexError:
                pass
        for e in self.g.edges:
            self.assertIsInstance(e, Element)
            self.assertTrue(e.directed)

    def test_add_edges(self):
        nodes = self.g.add_nodes(5)
        edge_list = []
        for idx, val in enumerate(nodes):
            try:
                edge_list.append((val,
                                  nodes[idx+1],
                                  {'test':1, 't':'test'}))
            except IndexError:
                pass

        edges = self.g.add_edges(edge_list)

        for e in edges:
            self.assertIsInstance(e, Element)

    def test_get_attributes(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        edge = self.g.add_edge(node,node2,{'keye':'valuee'})

        self.assertEqual(self.g[node],{'keyn':'valuen'})
        self.assertEqual(self.g[node2],{'keyn2':'valuen2'})
        self.assertEqual(self.g[edge],{'keye':'valuee'})

    def test_add_attributes(self):
        node = self.g.add_node({'keyn':'valuen'})
        self.g[node] = {'keyn2':'valuen2'}
        self.assertEqual(self.g[node], {'keyn':'valuen','keyn2':'valuen2'})

    def test_del_node(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        self.g.del_node(node2)
        for n in self.g.nodes:
            self.assertEqual(n,node)
        for a in self.g.attribute_store:
            self.assertEqual(a,node)

    def test_del_edge(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        node3 = self.g.add_node({'keyn3':'valuen3'})
        edge = self.g.add_edge(node,node2,{'keye':'valuee'})
        edge2 = self.g.add_edge(node,node3,{'keye':'valuee'})
        edge3 = self.g.add_edge(node2,node3)
        self.g.del_edge(edge2)

        for e in self.g.edges:
            self.assertIn(e,[edge,edge3])

        for a in self.g.attribute_store:
            self.assertIn(e,[node,node2,node3,edge,edge3])

    def test_graph(self):
        n1 = self.g.add_node()
        n2 = self.g.add_node()
        n3 = self.g.add_node()
        e1 = self.g.add_edge(n1,n2)
        e2 = self.g.add_edge(n1,n3)
        self.assertIn(e1,self.g.edges)
        self.assertIn(e2,self.g.edges)
        self.assertIn(n2, n1.neighbors)
        self.assertIn(n1, n2.neighbors)
        self.assertIn(n3, n1.neighbors)

class TestGraphZODB(TestGraph):

    def setUp(self):

        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = Graph(backend=ZODBBTreeBackend(root))

class TestElement(unittest.TestCase):

    def setUp(self):
        self.g = Graph(DictionaryBackend())

    def test_eq_ne_(self):
        e = Element(self.g)
        if e == e:
            pass
        else:
            self.fail('Element object does not compare equal to itself!')
        e2 = Element(self.g)
        if e != e2:
            pass
        else:
            self.fail('Two different Element objects compare equal!')
        self.assertNotEqual(e, e2)
        self.assertEqual(e, e)

    def test_lt_gt_le_ge_(self):
        e = Element(self.g)
        e2 = Element(self.g)

        #we don't know wether e2 will be less or greater than e, so test is limited
        if e > e2:
            pass
        if e >= e2:
            pass
        if e < e2:
            pass
        if e <= e2:
            pass

    def test_hash_(self):
        e = Element(self.g)
        e2 = Element(self.g)
        self.assertTrue(e.__hash__() != e2.__hash__())

    def test_repr_(self):
        e = Element(self.g)
        self.assertIsInstance(e.__repr__(), str)

    def test_setattr_(self):
        e = Element(self.g)
        with self.assertRaises(TypeError):
            e.id = 3

    def test_str_(self):
        e = Element(self.g)
        self.assertIsInstance(str(e), str)

class TestElementZODB(TestElement):

    def setUp(self):
        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = Graph(backend=ZODBBTreeBackend(root))

class TestNode(TestElement):

    def test_delete(self):
        n = self.g.add_node()
        n.delete()
        self.assertNotIn(n, self.g)

    def test_neighbors(self):
        nodes = self.g.add_nodes(3)
        self.g.add_edge(nodes[0], nodes[1])
        self.g.add_edge(nodes[0], nodes[2])
        self.assertIn(nodes[1], nodes[0].neighbors)
        self.assertIn(nodes[2], nodes[0].neighbors)

    def test_edges(self):
        nodes = self.g.add_nodes(3)
        e1 = self.g.add_edge(nodes[0], nodes[1])
        e2 = self.g.add_edge(nodes[0], nodes[2])
        self.assertIn(e1, nodes[0].edges)
        self.assertIn(e2, nodes[0].edges)
        for e in nodes[0].edges:
            self.assertIsInstance(e, Edge)

    def test_iter_(self):
        nodes = self.g.add_nodes(3)
        e1 = self.g.add_edge(nodes[0], nodes[1])
        e2 = self.g.add_edge(nodes[0], nodes[2])
        self.assertIn(e1, nodes[0])
        self.assertIn(e2, nodes[0])
        self.assertIn(nodes[1], nodes[0])
        self.assertIn(nodes[2], nodes[0])

    def test_getitem_setitem_(self):
        node = self.g.add_node({'keyn':'valuen'})
        node['keyn2'] = 'valuen2'
        self.assertEqual(node['keyn'],'valuen')
        self.assertEqual(node['keyn2'],'valuen2')

class TestNodeZODB(TestNode):

    def setUp(self):
        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = Graph(backend=ZODBBTreeBackend(root))

class TestEdge(TestElement):

    def test_delete(self):
        n1 = self.g.add_node()
        n2 = self.g.add_node()
        e = self.g.add_edge(n1, n2)
        e.delete()
        self.assertNotIn(e, self.g)

    def test_nodes(self):
        nodes = self.g.add_nodes(2)
        e1 = self.g.add_edge(nodes[0], nodes[1])
        for n in e1.nodes:
            self.assertIsInstance(n, Node)
            self.assertIn(n, nodes)

    def test_iter_(self):
        nodes = self.g.add_nodes(2)
        e1 = self.g.add_edge(nodes[0], nodes[1])
        for n in e1:
            self.assertIsInstance(n, Node)
            self.assertIn(n, nodes)

    def test_getitem_setitem_(self):
        nodes = self.g.add_nodes(2)
        e1 = self.g.add_edge(nodes[0], nodes[1])
        e1['key2'] = 'value2'
        self.assertEqual(e1['key2'],'value2')

class TestEdgeZODB(TestEdge):

    def setUp(self):
        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = Graph(backend=ZODBBTreeBackend(root))

class TestWeightedGraph(TestGraph):

    def setUp(self):
        self.g = WeightedGraph(DictionaryBackend())

    def test_add_weighted_node(self):
        n = self.g.add_node(weight=7)
        self.assertIsInstance(n, Element)
        for node in self.g.nodes:
            self.assertIsInstance(node, Element)
        self.assertIn(n, self.g.nodes)
        self.assertEqual(n.weight, 7)

class TestWeightedGraphZODB(TestWeightedGraph):

    def setUp(self):
        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = WeightedGraph(backend=ZODBBTreeBackend(root))


class TestWeightedElement(TestElement):

    def setUp(self):
        self.g = WeightedGraph(DictionaryBackend())

    def test_weight(self):
        e = WeightedElement(self.g)
        e.weight = 9
        self.assertEqual(e.weight, 9)

class TestWeightedElementZODB(TestWeightedElement):

    def setUp(self):

        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = WeightedGraph(backend=ZODBBTreeBackend(root))

    def test_weight(self):
        e = WeightedElement(self.g)
        e.weight = 9
        self.assertEqual(e.weight, 9)

class TestWeightedNode(TestNode):

    def setUp(self):
        self.g = WeightedGraph(DictionaryBackend())

class TestWeightedNodeZODB(TestWeightedNode):

    def setUp(self):

        storage = FileStorage(NamedTemporaryFile().name)
        db = DB(storage)
        connection = db.open()
        root = connection.root
        self.g = WeightedGraph(backend=ZODBBTreeBackend(root))
