import copy
from abc import ABC, abstractmethod

import npycomp.reductions._directory as directory
from npycomp.problems._sat_solver import _SATSolver


class Problem(ABC):
    """
    Abstract base class for computational problems.

    This class provides a common interface and workflow for all problems,
    including methods to reduce one problem to another, solve a problem, and
    reconstruct the solution from a solver's output. In practice, each concrete
    problem implementation (e.g., :class:`.SAT`) will subclass ``Problem`` and
    provide problem-specific details in its own methods.

    Parameters
    ----------
    name : str
        The canonical name of the problem (e.g., 'SAT', 'TSP', etc.).
    **kwargs : dict
        Additional keyword arguments needed by the problem, typically
        describing its specific parameters or instance data.

    Attributes
    ----------
    name : str
        The canonical name of the problem. Used to identify this problem type
        in reduction directories.
    """

    def __init__(self, name: str, *args):
        self._name = name
        self._args = args

    @property
    def name(self):
        """The canonical name of the problem."""
        return self._name

    def solve(self):
        """Solve the problem instance.

        Solve the problem instance by reducing it to a SAT problem and invoking
        a SAT solver.

        Returns
        -------
        bool or object
            A satisfying assignment to the problem instance, or ``False`` if no
            such assignment exists.
        """
        if self.name == "SAT":
            return _SATSolver(*self._args).solve()

        clauses = self.reduce("SAT")
        reduction = _SATSolver(clauses)
        solution = reduction.solve()
        return self.reconstruct(solution)

    def reconstruct(self, solution):
        """Reconstruct the solution."""
        # TODO: implement this method by defining reconstruction functions for
        # each reduction.
        return NotImplementedError

    def reduce(self, target):
        """Reduce the problem to a specified target problem.

        Consults a ``directory`` of known problems and reduction functions to
        traverse a path of problem transformations.  For example, if reducing
        from TSP to SAT is possible, this method  looks up the appropriate
        chain of reductions and applies them sequentially to transform the
        current problem's parameters.

        Parameters
        ----------
        target : str
            The name of the target problem (e.g., 'SAT', 'clique', etc.).

        Returns
        -------
        dict
            A dictionary of keyword arguments representing the target problem
            instance. This dictionary is typically consumed by the
            corresponding problem's constructor.

        Raises
        ------
        NotImplementedError
            If the target problem is unknown, or if there is a missing link in
            the chain of reduction functions required to reach the target.

        Examples
        --------
        To reduce a clique problem to SAT clauses:

        >>> from npycomp.problems import Clique
        >>>
        >>> A = [
        ...     [0, 1],
        ...     [1, 0],
        ... ]
        >>> k = 2
        >>> clique = Clique(A, k)
        >>> clique.reduce("SAT")
        [['y_0_0', 'y_1_0'],
        ['y_0_1', 'y_1_1'],
        ['~y_0_0', '~y_0_1'],
        ['~y_1_0', '~y_1_1']]

        These clauses can then be passed to a SAT solver to find a satisfying
        assignment.

        >>> from npycomp.problems import SAT
        >>> sat = SAT(clique.reduce("SAT"))
        >>> sat.solve()
        [1, 0, 0, 1]

        See Also
        --------
        npycomp.reductions: Directory of known reduction functions.
        """
        if target not in directory.PROBLEMS:
            raise NotImplementedError(
                f"'{target}' is not a valid problem. "
                "Must be one of {directory.PROBLEMS}"
            )

        path = directory.path(self.name, target)
        reduction_args = self._args
        current = self.name
        while path:
            next = path.pop(0)
            if (current, next) not in directory.INDEX:
                raise NotImplementedError(
                    f"Cannot reduce {self.name} to {target}. "
                    f"Missing reduction function."
                )
            reduction_func = directory.INDEX[(current, next)]
            reduction_args = reduction_func(*reduction_args)
            current = next

        return reduction_args

    @classmethod
    @abstractmethod
    def from_dimacs(cls, path: str, **kwargs):
        """Load a problem instance from a DIMACS file.

        Parameters
        ----------
        path : str
            The path to a DIMACS file.
        **kwargs
            Additional keyword arguments needed by the problem.

        Returns
        -------
        Problem
            A problem instance created from the DIMACS file.
        """
        pass
