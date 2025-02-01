def threesat_to_sat(
    clauses: list[tuple[str]],
) -> list[tuple[str]]:
    r"""Convert a 3SAT problem to a SAT problem.

    3SAT is a special case of the SAT problem where each clause has exactly
    three literals. 3SAT is already in conjunctive normal form, so the
    reduction is not necessary. This function simply returns the input
    clauses. This function is included for completeness.
    """
    return clauses
