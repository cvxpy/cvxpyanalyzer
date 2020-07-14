from analyzer.convexity_checker import might_be_convex
from analyzer.solvers import get_solvers
from analyzer.version import check_version
import cvxpy as cp
import sys


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def tech_support(problem):
    """Debug the problem.
    """
    # Check that CVXPY is up-to-date.
    latest = check_version()
    if latest:
        print("You have the latest version of CVXPY.")
    else:
        print(
            "You have an out-of-date version of CVXPY.",
            "If you installed CVXPY via conda, upgrade CVXPY by running the command 'conda update -c conda-forge cvxpy'.",
            "If you installed CVXPY via pip, upgrade CVXPY by running the command 'pip install --upgrade cvxpy'.",
        )
        if not query_yes_no("Continue debugging?"):
            return

    # Check that the problem is DCP/convex.
    if not prob.is_dcp():
        print(
            "The problem is not DCP. You must write the problem so it follows the DCP rules."
        )
        print("Learn more about the DCP rules at https://dcp.stanford.edu")
        convexish = might_be_convex(problem)
        if not convexish:
            print("The problem is not convex either. Only convex problems can be DCP.")
        print()
        return

    # Check that the user has tried all the available solvers.
    try:
        problem.solve()
    except cp.SolverError:
        print("The default solver cannot solve your problem.")

    if problem.status not in [
        cp.OPTIMAL,
        cp.INFEASIBLE,
        cp.UNBOUNDED,
    ] or not query_yes_no("Are you satisfied with the solution returned by CVXPY?"):
        print("Try solving your problem with a different solver.")
        print()
        installed = get_solvers(problem)
        print()
        print(
            "Instructions for using non-default solvers are here:\n"
            "https://cvxpy.org/tutorial/advanced/index.html#choosing-a-solver\n"
            "Instructions for installing new solvers are here:\n"
            "https://cvxpy.org/install/index.html"
        )
    print()


if __name__ == "__main__":
    print("Not DCP.\n")
    x = cp.Variable(5)
    prob = cp.Problem(cp.Minimize(cp.sqrt(x.T @ x)), [-1 <= x, x <= 1])
    tech_support(prob)

    print("Not convex.\n")
    prob = cp.Problem(cp.Minimize(-cp.sqrt(x.T @ x)), [-1 <= x, x <= 1])
    tech_support(prob)

    print("DCP.\n")
    x = cp.Variable(5)
    prob = cp.Problem(cp.Minimize(cp.sum_squares(x)), [-1 <= x, x <= 1])
    tech_support(prob)

    print("Not feasible.\n")
    x = cp.Variable(5)
    prob = cp.Problem(cp.Minimize(cp.sum_squares(x)), [2 <= x, x <= 1])
    tech_support(prob)
