import cvxpy as cp
import random

COUNTER = 0


def get_convex():
    """Return a random increasing convex atom.
    """
    return random.choice([cp.abs, cp.square, cp.max])


def get_concave():
    """Return a random increasing concave atom.
    """
    return random.choice([cp.log, cp.sqrt, cp.min])


def randint():
    """Return a random pleasing integer.
    """
    return random.randint(1, 10)


def slack():
    global COUNTER
    var = cp.Variable(name=random.choice(["x", "y", "z", "u", "v", "w"]) + str(COUNTER))
    COUNTER = COUNTER + 1
    return var


def constraint(con):
    var1 = slack()
    var2 = slack()
    return [con.copy([con.args[0] + var1, var2 + con.args[1]]), var1 == var2]


def objective(obj):
    if type(obj) == cp.Minimize:
        const = get_convex()(randint())
        if random.randint(0, 1):
            return cp.Minimize(get_convex()(obj.expr) + const)
        else:
            return cp.Minimize(const + get_convex()(obj.expr))
    else:
        const = get_convex()(randint())
        if random.randint(0, 1):
            return cp.Maximize(get_concave()(obj.expr) + const)
        else:
            return cp.Maximize(const + get_concave()(obj.expr))


EQUIVALENCES = {
    cp.constraints.Equality: [constraint],
    cp.constraints.Inequality: [constraint],
    cp.Minimize: [objective],
    cp.Maximize: [objective],
}


def obfuscate(prob, reps=25):
    for i in range(reps):
        if random.random() < 0.2:
            obj = prob.objective
            obj = random.choice(EQUIVALENCES[type(obj)])(obj)
            prob = cp.Problem(obj, prob.constraints)
        else:
            idx = random.randint(0, len(prob.constraints) - 1)
            new_cons = prob.constraints[:idx] + prob.constraints[idx + 1 :]
            cons = prob.constraints[idx]
            new_cons += random.choice(EQUIVALENCES[type(cons)])(cons)
            prob = cp.Problem(prob.objective, new_cons)
    return prob


if __name__ == "__main__":
    random.seed(2)
    import cvxpy as cp

    x = cp.Variable(5, name="x")
    prob = cp.Problem(cp.Minimize(cp.norm2(x)), [-1 <= x, x <= 1])
    print("Original problem:")
    print(prob)
    print()
    print("Obfuscated problem:")
    obs = obfuscate(prob)
    print(obs)

    # Check equality.
    prob.solve()
    x_val = x.value
    obs.solve(solver=cp.MOSEK)
    x_obs = x.value
    print("x residual:", cp.abs(x_val - x_obs).value)
