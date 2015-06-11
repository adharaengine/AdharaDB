from setuptools import setup, find_packages
setup(
    name = "AdharaGraph",
    version = "0.03",
    description = "A simple Graph Processing System",
    author = "James Lee Vann",
    py_modules = ['db', 'backends', 'weighted_graph'],
    extras_require = {
        'ZODB Storage':  ["ZODB"],
    }
)
