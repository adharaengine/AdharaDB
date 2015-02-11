import unittest
import uuid
import tempfile

from adharadb import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph()

    def test_add_node(self):
        n = self.g.add_node()
        self.assertIsInstance(n, type(uuid.uuid4()))

    def test_add_nodes(self):
        nodes = self.g.add_nodes(4)
        self.assertIsInstance(nodes,list)
        self.assertEqual(len(nodes),4)
        for n in nodes:
            self.assertIsInstance(n, type(uuid.uuid4()))

    def test_nodes(self):
        self.g.add_nodes(5)
        for n in self.g.nodes():
            self.assertIsInstance(n, type(uuid.uuid4()))

    def test_edges(self):
        nodes = self.g.add_nodes(5)
        for idx, val in enumerate(nodes):
            try:
                self.g.add_edge(val,nodes[idx+1])
            except IndexError:
                pass
        for e in self.g.edges():
            self.assertIsInstance(e, type(uuid.uuid4()))

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
            self.assertIsInstance(e, type(uuid.uuid4()))

    def test_get_neighbors(self):
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

        for node in nodes:
            for n in self.g.get_neighbors(node):
                self.assertIsInstance(n, type(uuid.uuid4()))

    def test_get_attributes(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        edge = self.g.add_edge(node,node2,{'keye':'valuee'})

        self.assertEqual(self.g.get_attributes(node),{'keyn':'valuen'})
        self.assertEqual(self.g.get_attributes(node2),{'keyn2':'valuen2'})
        self.assertEqual(self.g.get_attributes(edge),{'keye':'valuee'})

    def test_add_attributes(self):
        node = self.g.add_node({'keyn':'valuen'})
        self.g.add_attributes(node,keyn2='valuen2')
        self.assertEqual(self.g.get_attributes(node),
                                            {'keyn':'valuen','keyn2':'valuen2'})
    def test_del_node(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        self.g.del_node(node2)

        for n in self.g.nodes():
            self.assertEqual(n,node)

        for a in self.g.node_dict['attributes']:
            self.assertEqual(a,node)

    def test_del_edge(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        node3 = self.g.add_node({'keyn3':'valuen3'})
        edge = self.g.add_edge(node,node2,{'keye':'valuee'})
        edge2 = self.g.add_edge(node,node3,{'keye':'valuee'})
        edge3 = self.g.add_edge(node2,node3)
        self.g.del_edge(edge2)

        for e in self.g.edges():
            self.assertIn(e,[edge,edge3])

        for a in self.g.node_dict['attributes']:
            self.assertIn(e,[node,node2,node3,edge,edge3])

    def test_export_load(self):
        node = self.g.add_node({'keyn':'valuen'})
        node2 = self.g.add_node({'keyn2':'valuen2'})
        node3 = self.g.add_node({'keyn3':'valuen3'})
        edge = self.g.add_edge(node,node2,{'keye':'valuee'})
        edge2 = self.g.add_edge(node,node3,{'keye':'valuee'})
        edge3 = self.g.add_edge(node2,node3)
        #I really need to get this test to use a proper temp file
        temp = open('temp.p','w+b')
        self.g.export(temp)
        temp.close()
        self.g.del_edge(edge2)
        self.g.del_node(node2)
        temp = open('temp.p','r+b')
        self.g.load(temp)
        temp.close()
        self.assertEqual(self.g.get_attributes(node2),{'keyn2':'valuen2'})
        self.assertEqual(self.g.get_attributes(edge2),{'keye':'valuee'})
