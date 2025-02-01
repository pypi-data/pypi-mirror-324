from npycomp.problems._problem import Problem


class ThreeSAT(Problem):
    r"""A SAT Problem with at most three literals per clause.

    3-SAT is a special case of the `SAT problem`_ where each clause has at most
    three literals. Like the SAT, The 3-SAT probleom asks whether there exists
    an assignment of variables that satisfies a given Boolean formula.

    Formally, a 3-SAT problem is defined by a formula, :math:`\varphi`, over a
    set of boolean variables, :math:`X = \{x_1, x_2, \ldots, x_n\}`. A formula
    is said  to be satisfiable if there exists an assignment of truth values
    (TRUE or FALSE) to :math:`X` such that the formula evaluates to TRUE. A SAT
    formula, :math:`\varphi`, is typically given in `Conjunction Normal Form
    (CNF)`_. A formula is considered to be CNF if it is a `conjunction`_
    (logical AND, :math:`\land`) of clauses,

    .. math::

        \varphi = C_i \land C_{i+1} \land \ldots \land C_m,

    where each clause :math:`C_i` is a `disjunction`_ (logical OR,
    :math:`\lor`) of at most three literals. A literal is either a variable
    :math:`x_j` or its negation :math:`\neg x_j`. Concretely,

    .. math::

        C_i = (l_{i1} \lor l_{i2} \lor l_{i3})

    The 3-SAT problem asks whether there exists an assignment of truth values
    (True or False) to the variables :math:`x_1, x_2, \ldots, x_n` such that
    the entire formula :math:`\varphi` evaluates to True. When such an
    assignment exists, the formula is said to be *satisfiable*.

    .. _SAT Problem: https://en.wikipedia.org/wiki/Boolean_satisfiability_problem
    .. _Conjunction Normal Form (CNF): https://en.wikipedia.org/wiki/Conjunctive_normal_form
    .. _conjunction: https://en.wikipedia.org/wiki/Logical_conjunction
    .. _disjunction: https://en.wikipedia.org/wiki/Logical_disjunction

    Parameters
    ----------
    clauses : list
        A list of clauses in conjunctive normal form.

    Attributes
    ----------
    formula : str
        The formula of the problem.

    See Also
    --------
    SAT: A general SAT problem.
    """

    def __init__(self, clauses: list):
        self._formula = clauses
        if not all(len(clause) <= 3 for clause in clauses):
            raise ValueError("All clauses must have exactly three literals.")
        Problem.__init__(self, "3SAT", clauses)

    @property
    def formula(self):
        return " ∧ ".join(
            [self._clause_to_string(clause) for clause in self._clauses]
        )

    def _literal_to_string(self, literal: int):
        """Convert a literal to a string.

        Parameters
        ----------
        literal : int
            A literal.
        """
        sign = "¬" if literal & 1 else ""
        return sign + self._variables[literal >> 1]

    def _clause_to_string(self, clause: tuple[int]):
        """Convert a clause to a string.

        Parameters
        ----------
        clause : tuple[int]
            A clause.
        """
        return (
            "(" + " ∨ ".join(self._literal_to_string(l) for l in clause) + ")"
        )

    def _model_to_string(self, model):
        """Convert a model to a string.

        Parameters
        ----------
        model : list
            A list of variable assignments.
        """
        output = []
        for i, assignment in enumerate(model):
            if assignment is None:
                output.append(f"{self._variables[i]} ∈ {{0, 1}}")
            else:
                output.append(f"{self._variables[i]} = {assignment}")

        return ", ".join(output)

    def reconstruct(self, solution):
        """Reconstruct the solution."""
        return solution

    @classmethod
    def from_dimacs(cls, path: str):
        """Load a SAT instance from a DIMACS file.

        Parameters
        ----------
        path: str
            Path to DIMACS-format file describing a SAT instance.

        Returns
        -------
        SAT
            An instance of the SAT class with clauses built from the file.
        """
        clauses = []
        with open(path, "r") as file:
            for line in file:
                line = line.strip()

                if line.startswith("c") or line.startswith("p"):
                    continue

                if line:
                    literals = line.split()
                    clause = []

                    for literal in literals:
                        # End of clause marker
                        if literal == "0":
                            break
                        # Negated literal
                        if literal.startswith("-"):
                            clause.append(f"~{literal[1:]}")
                        # Positive literal
                        else:
                            clause.append(literal)

                    if clause:
                        clauses.append(tuple(clause))
        return cls(clauses)
