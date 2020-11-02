import cvxpy as cp
import numpy as np

from cvxpy.problems.objective import Minimize, Maximize


def might_be_convex(problem, niter=100, tol=1e-8):
    def get_values(problem):
        var_values = []
        for var in problem.variables():
            if var.is_nonneg():
                value = np.random.rand(*var.shape)
            elif var.is_nonpos():
                value = -np.random.rand(*var.shape)
            elif var.is_nsd():
                value = np.random.randn(*var.shape)
                value = -value @ value.T
            elif var.is_psd():
                value = np.random.randn(*var.shape)
                value = value @ value.T
            else:
                value = np.random.randn(*var.shape)
            var_values.append(value)
        return var_values

    def set_values(problem, var_values):
        for var, var_value in zip(problem.variables(), var_values):
            var.value = var_value

    def get_objective_constraint_values(problem, maximize=False):
        if maximize:
            return np.concatenate(
                [np.array([-problem.objective.value])]
                + [np.atleast_1d(c.expr.value) for c in problem.constraints]
            )
        else:
            return np.concatenate(
                [np.array([problem.objective.value])]
                + [np.atleast_1d(c.expr.value) for c in problem.constraints]
            )

    maximize = isinstance(problem.objective, Maximize)
    might_be_convex = True
    for _ in range(niter):
        values1 = get_values(problem)
        values2 = get_values(problem)

        set_values(problem, values1)
        f1 = get_objective_constraint_values(problem, maximize)
        set_values(problem, values2)
        f2 = get_objective_constraint_values(problem, maximize)
        set_values(problem, [(v1 + v2) / 2 for v1, v2 in zip(values1, values2)])
        f12 = get_objective_constraint_values(problem, maximize)

        if not ((f1 + f2) / 2 - f12 >= -tol).all():
            might_be_convex = False
            break

    return might_be_convex


if __name__ == "__main__":
    x = cp.Variable(5)
    prob = cp.Problem(cp.Minimize(cp.sqrt(x.T @ x)), [-1 <= x, x <= 1])
    try:
        prob.solve()
    except:
        print("Might be convex: ", might_be_convex(prob))

    prob = cp.Problem(cp.Minimize(-cp.sqrt(x.T @ x)), [-1.0 <= x, x <= 1])
    try:
        prob.solve()
    except:
        print("Might be convex: ", might_be_convex(prob))
