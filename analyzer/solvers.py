from cvxpy.reductions.solvers.defines import (
    CONIC_SOLVERS,
    QP_SOLVERS,
    INSTALLED_CONIC_SOLVERS,
    INSTALLED_QP_SOLVERS,
)


def try_all_solvers():
    """Try all solvers and report results.
    """
