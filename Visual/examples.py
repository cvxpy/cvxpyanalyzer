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

    objective = Minimize(-1*y2**2+2*y2)
    objective1 = Minimize((x2 - y2) ** 2)
    objective2 = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)

    print("----objective----")
    v = Visual(objective)
    v.show()
    v.show_and_save("file_name")
    v.draw_graph()
    v.print_expr()
    print("----objective----")

    print("----objective1----")
    v = Visual(objective1)
    v.show()
    v.show_and_save("file_name1")
    v.draw_graph()
    v.print_expr()
    print("----objective1----")

    print("----objective2----")
    v = Visual(objective2)
    v.show()
    v.show_and_save("file_name2")
    v.draw_graph()
    v.print_expr()
    print("----objective2----")

