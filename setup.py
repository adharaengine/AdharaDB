from setuptools import setup, find_packages
setup(
    name = "AdharaDB",
    version = "0.02",
    description = "A simple Graph Database",
    author = "James Lee Vann",
    py_modules = ['adhara_db']
    extras_require = {
        'ZODB Storage':  ["ZODB"],
    }
)
