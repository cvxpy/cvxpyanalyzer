import cvxpy as cp
import random


def get_convex():
    """Return a random convex atom.
    """
    return random.choice([cp.abs, cp.square, cp.max])


def get_concave():
    """Return a random concave atom.
    """
    return random.choice([cp.entr, cp.sqrt, cp.min])


def randint():
    """Return a random pleasing integer.
    """
    return random.randint(0, 100)


EQUIVALENCIES = {
    cp.constraints.Equality: lambda con: [
        con.args[0] <= con.args[1],
        con.args[0] >= con.args[1],
    ],
    cp.constraints.Inequality: lambda con: [con, 0 <= con.args[1] - con.args[0]],
    cp.Minimize: lambda obj: cp.Minimize(get_convex()(obj.expr) + randint()),
    cp.Maximize: lambda obj: cp.Maximize(get_concave()(obj.expr) + randint()),
}


def obfuscate(prob, reps=25):
    for i in range(reps):
        if random.randint(0, 1):
            obj = prob.objective
            obj = EQUIVALENCIES[type(obj)](obj)
            prob = cp.Problem(obj, prob.constraints)
        else:
            idx = random.randint(0, len(prob.constraints) - 1)
            new_cons = prob.constraints[:idx] + prob.constraints[idx + 1 :]
            con = prob.constraints[idx]
            new_cons += EQUIVALENCIES[type(con)](con)
            prob = cp.Problem(prob.objective, new_cons)
    return prob


if __name__ == "__main__":
    import cvxpy as cp

    x = cp.Variable(5, name='x')
    prob = cp.Problem(cp.Minimize(cp.norm2(x)), [-1 <= x, x <= 1])
    print("Original problem:")
    print(prob)
    print()
    print("Obfuscated problem:")
    print(obfuscate(prob))
