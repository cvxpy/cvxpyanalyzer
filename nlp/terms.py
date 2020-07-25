from collections import defaultdict
import json


def process_problem(prob):
    """Get term dict for a problem.
    """
    term_dict = defaultdict(int)
    get_terms(prob.objective, term_dict)
    for con in prob.constraints:
        get_terms(con, term_dict)
    return term_dict


def get_terms(expr, term_dict):
    """Obtain a dict of term: count for elems in expr.
    """
    term_dict[str(type(expr))] += 1
    for arg in expr.args:
        get_terms(arg, term_dict)


def save_problem(prob, filename):
    """Save problem term data to a json file.
    """
    term_dict = process_problem(prob)
    with open(filename, "w") as outfile:
        json.dump(term_dict, outfile)


if __name__ == "__main__":
    import cvxpy as cp

    x = cp.Variable(5)
    prob = cp.Problem(cp.Minimize(cp.sum_squares(x)), [-1 <= x, x <= 1])
    print(process_problem(prob))

    save_problem(prob, "test.json")
