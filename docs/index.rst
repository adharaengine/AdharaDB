.. AdharaGraph documentation master file, created by
   sphinx-quickstart on Sat Jun  6 20:07:18 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AdharaGraph's documentation!
=======================================

Contents:

.. toctree::
   :maxdepth: 2

   graph
   elements

AdharaGraph is a library for working with `graph structures <https://en.wikipedia.org/wiki/Graph_%28abstract_data_type%29>`_ in Python.

AdharaGraph provides pluggable backends that allow you to store your graph in different ways.

The two current built-in backends are the in-memory DictionaryBackend and the ZODB ZODBBTreeBackend, which allows you to store your graph in a ZODB datastore, opening the possiblity to use any storage system offered by `ZODB <http://www.zodb.org>`_!

The ZODB backend supports transactions and if you use `ZEO <http://www.zodb.org/en/latest/documentation/guide/zeo.html>`_ scalability.

Alternative backends are easy to develop and I plan to create in the future!

Introduction
============

Install AdharaGraph using pip::

  pip install AdharaGraph

If you want to use ZODB/ZEO for storage, install them too!

Now you can create a simple graph::


  from adhara_graph.db import Graph

  g = Graph() #creates a graph using the in-memory backend for storage
  n1 = g.add_node() # creates a node
  n2 = g.add_node() #creates another node
  g.add_edge(n1, n2) # creates an edge connecting our two nodes!


That was pretty simple!  Read on to learn about adding multiple nodes and edges at once,
adding attributes, weights, and direction to nodes, and searching the graph!

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
