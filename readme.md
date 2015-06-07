This is an implementation of a Graph DB System in Python.  It is very early and may change significantly.  Check it out and file issues with your feedback!

- Requires Python 3.4
- Designed to be general purpose.
- Supports in memory or persisted graphs
- Persist graphs to any storage backend supported by ZODB
- Each Node or Edge is identified by a UUID
- Nodes and Edges can have an unlimited number of Attributes
- Supports directed or undirected edges
- Optional weighted graphs (May merge to make all graphs weighted?)
- Only Supports undirected graphs at this time

What it is missing (for now!)
- No fancy Graph processing algorithms (yet- contributions welcome, see below :)
- it has not been tested for performance or really big graphs, though the ZODB backend should provide decent support for it!
- Documentation (This is what I am working on right now!)


#Road Map#
- Documentation
- An ORM with constraint support for graph models
- Implementations of basic graph algorithms (Perhaps I can port these from NetworkX?)
- More, better unit tests

#Contributing#
- All code is Apache 2 licensed
- Currently this library is in its infancy.  Please open an issue before you begin work on any contributions so that we can properly plan together and save a ton of potentially wasted time :)

#Usage#
I really should write some documentation here :)
