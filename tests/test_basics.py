from analyzer import check_version, might_be_convex
import cvxpy as cp
import numpy as np


def test_version():
    assert check_version()


def test_checker():
    """Test convexity checker.
    """
    x = cp.Variable(5)
    np.random.seed(1)
    prob = cp.Problem(cp.Minimize(cp.sqrt(x.T @ x)), [-1 <= x, x <= 1])
    assert might_be_convex(prob)

    prob = cp.Problem(cp.Minimize(-cp.sqrt(x.T @ x)), [-1.0 <= x, x <= 1])
    assert not might_be_convex(prob)
