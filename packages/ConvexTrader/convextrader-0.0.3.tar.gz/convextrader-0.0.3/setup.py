import os
import setuptools
import re

NAME = "ConvexTrader"
AUTHOR = "Liam Davis, Tairan 'Ryan' Ji, Allison Klinger, Surya Rao"
AUTHOR_EMAIL = "ljdavis27@amherst.edu, tji26@amherst.edu, aklinger27@amherst.edu, srao28@amherst.edu"
DESCRIPTION = "A collection of SAT and SMT solvers for solving Sudoku puzzles"
LICENSE = "MIT"
URL = "https://acquantclub.com/ConvexTrader"
README = "README.md"
CLASSIFIERS = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
INSTALL_REQUIRES = [
    "cvxpy",
    "numpy",
]
ENTRY_POINTS = {}
SCRIPTS = []

HERE = os.path.dirname(__file__)


def read(file):
    with open(os.path.join(HERE, file), "r") as fh:
        return fh.read()


VERSION = re.search(
    r'__version__ = [\'"]([^\'"]*)[\'"]', read(NAME.replace("-", "_") + "/__init__.py")
).group(1)
LONG_DESCRIPTION = read(README)


if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        version=VERSION,
        packages=setuptools.find_packages(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        scripts=SCRIPTS,
        include_package_data=True,
        python_requires=">=3.9",
    )
