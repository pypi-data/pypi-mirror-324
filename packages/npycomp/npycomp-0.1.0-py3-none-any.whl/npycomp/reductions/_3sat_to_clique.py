from collections import defaultdict

from npycomp._include._graph import _Graph


def threesat_to_clique(
    clauses: list[tuple[str]],
) -> tuple[list[list[int]], int]:
    r"""Convert a 3SAT problem to a clique problem.

    Consider a 3-SAT formula with :math:`n` clauses :math:`\phi = C_1 \land C_2
    \land C_n`, where :math:`C_i` is a clause consisting of the disjunction of
    at most three literals: :math:`C_i = (l_1^i \lor l_2^i \lor l_3^i)`. The
    reduction to a clique problem is as follows.

    Construct a graph :math:`G(V, E)` with a vertex for each literal
    :math:`l_i^j` in each clause :math:`j`. For every pair of vertices, and an
    edge between them if they are (i) not part of the same clause, and (ii) are
    not in contradiction, i.e., they either refer to different variables, or
    refer to the same variable but are not complements of each other.

    The resulting graph :math:`G` has a clique of size :math:`n` if and only if
    the 3-SAT formula :math:`\phi` is satisfiable, where :math:`n` is the
    number of clauses in the formula.

    Parameters
    ----------
    clauses : list
        A list of clauses in conjunctive normal form. Each clause is a tuple
        of at most three literals.

    Returns
    -------
    tuple
        The adjacency matrix of the graph and the number of clauses.
    """
    nodes = []
    for i, clause in enumerate(clauses):
        for literal in clause:
            nodes.append((i, literal))

    n = len(nodes)
    A = [[0] * n for _ in range(n)]
    for i, (clause_i, literal_i) in enumerate(nodes):
        literal_i_negated = True if literal_i.startswith("~") else False
        for j, (clause_j, literal_j) in enumerate(nodes):
            literal_j_negated = True if literal_j.startswith("~") else False
            if (clause_i != clause_j) and (
                literal_i != literal_j
                or literal_i_negated == literal_j_negated
            ):
                A[i][j] = 1
                A[j][i] = 1

    return A, len(clauses)
