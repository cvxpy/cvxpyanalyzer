import cvxpy as cp
import cvxopt
from cvxpy import Minimize, Variable, quad_form, Problem
from cvxpy.problems.objective import Maximize
from Visual.visual import Visual

if __name__ == '__main__':
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1
    x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))

    x1 = Variable(n)
    y1 = Variable()
    x2 = Variable()
    y2 = Variable()
    z1 = Variable(n)

    objective = Minimize(-1 * (y2) ** 2 + 2 * y2)
    constraints = [y2 >= 1]
    v = Visual(objective)
    print(v.expr)
    v.draw_graph()

    objective1 = Minimize((x2 - y2) ** 2)
    objective2 = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)
    objective3 = Maximize(3 * cp.sum(x2 - y2) + (x2 - y2) ** 2 + quad_form(z1, P))

    # examples for show_digraph:

    v = Visual(objective1)
    v.show_digraph()

    v2 = Visual(objective2)
    v2.show_digraph()

    v3 = Visual(objective3)
    v3.show_digraph()

    # examples for print_tree:

    print("---objective 1 ---")
    v = Visual(objective1)
    print(v.curvature_sign_list)
    print("---objective 1 ---")

    v.root.print_tree()

    print("---objective 2 ---")
    v2 = Visual(objective2)
    print(v2.curvature_sign_list)
    print("---objective 2 ---")

    v2.root.print_tree()

    print("---objective 3 ---")
    v3 = Visual(objective3)
    print(v3.curvature_sign_list)
    print("---objective 3 ---")

    v3.root.print_tree()

