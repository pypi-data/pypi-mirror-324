"""Implementations of reductions between NP-complete problems.

NPyComp ``reductions`` provides implementations of reductions between
NP-complete problems. Each reduction in this module is a function that
transforms an instance of one problem into an instance of another problem.

Reductions
--------
.. autosummary::
   :toctree: reductions

   clique_to_sat - Reduce a Clique problem to a SAT problem.
   threesat_to_clique - Reduce a 3-SAT problem to a Clique problem.
   threesat_to_sat - Reduce a 3-SAT problem to a SAT problem.
"""

from npycomp.reductions._3sat_to_clique import threesat_to_clique
from npycomp.reductions._3sat_to_sat import threesat_to_sat
from npycomp.reductions._clique_to_sat import clique_to_sat
