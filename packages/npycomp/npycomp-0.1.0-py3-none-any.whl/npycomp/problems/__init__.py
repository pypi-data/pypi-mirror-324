"""Implementations of various NP-complete problems.

.. currentmodule:: npycomp.problems

NPyComp ``problems`` provides implementations of various NP-complete problems.
Each problem in this module can be reduced to any other problem in this module.

Problems
--------
.. autosummary::
   :toctree: problems

   SAT - A SAT problem defined by clauses in CNF form.
   Clique - A Clique problem defined by an adjacency matrix and a clique size.
"""

from npycomp.problems._clique import Clique
from npycomp.problems._sat import SAT
