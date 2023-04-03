import cvxpy as cp
import cvxopt
from cvxpy import Minimize, Variable, quad_form,Problem
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

    # for Niv
    # objective = Minimize(-1*(y2)**2+2*y2)
    # constraints = [y2 >= 1]
    # prob = Problem(objective, constraints)
    # print(constraints[0])
    # v = Visual(objective)
    # print(v.expr)
    # v.draw_graph()
    # print(objective.expr)

    # for bar and einav
    objective = Minimize((x2 - y2) ** 2)
    objective1 = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)
    objective2 = Maximize(3 * cp.sum(x2 - y2) + (x2 - y2) ** 2 + quad_form(z1, P))

    obj = Minimize((x2 - y2) ** 2)
    v = Visual(obj)
    print(v.curvature_sign_list)

    v = Visual(objective)
    # # v.show()
    v.show_digraph("file_name")
    # print("---objective---")
    # v.root.print_tree()
    # print("---objective---")

    # v = Visual(objective1)
    # # v.show()
    # v.show_digraph()
    # print("---objective1---")
    # v.root.print_tree()
    # print("---objective1---")
    #
    # v = Visual(objective2)
    # # v.show()
    # print("---objective2---")
    # v.root.print_tree()
    # print("---objective2---")
