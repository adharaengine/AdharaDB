Elements (Nodes and Edges)
==========================

In Adhara DB, Nodes and Edges are immutable objects.  They are similar to
(and currently contain, as th id attribute) UUIDs.  They do have some added
conveniance methods that will be documented here.

Notes::

  You may be thinking that elements can't be immutable, because you can set
  attributes on them!  Well, that is one of the conveniance methods!  The Graph
  object stores attributes in a seperate container, so you are not actually
  changing the element at all!

Warning::

  You should not ever create an element object directly from the Element, Node,
  or Edge classes!  You should always use the graph methods (add_node, add_nodes,
  add_edge, etc.) to do this for you!  Otherwise, they won't properly register
  in the Graph structure!
_____
Nodes
_____


_____
Edges
_____
