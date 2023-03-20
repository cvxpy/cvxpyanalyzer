"""
    >>> from Visual.visual import *
    >>> import numpy as np
    >>> from Visual import binary_tree
    >>> from tkinter.ttk import Treeview
    >>> import tkinter as tk
    >>> from tkinter import font, ttk

    >>> import cvxpy as cp
    >>> import cvxopt
    >>> from cvxpy import Minimize, Problem, Variable, quad_form
    >>> from cvxpy.problems.objective import Objective
    >>> import operator

    >>> from Visual.binary_tree import Node
    >>> n = 3
    >>> P = cvxopt.matrix([13, 12, -2,12, 17, 6,-2, 6, 12], (n, n))
    >>> q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    >>> r = 1
    >>> x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))
    >>> x = Variable(n)
    >>> y = Variable()
    >>> z = Variable(n)
    >>> objective = Minimize(0.5 * quad_form(x, P) - cp.sum_squares(x) + q.T @ x + r + y)
    >>> v = Visual(objective)
    >>> stri=str(objective.expr).replace("+ -", " - ")
    >>> print(str(objective.expr).replace("+ -", " - "))
    True
    >>> stri==v.root.expr
    True
    >>> v.root.checkin_sons('-')
    True
    >>> n=v.root.node_son('-')
    >>> n.checkin_sons('0.5 @ QuadForm(var1, [[13. 12. -2.][12. 17.  6.][-2.  6. 12.]])')
    True
    >>> A_wall = 100
    >>> A_flr = 10
    >>> alpha = 0.5
    >>> beta = 2
    >>> gamma = 0.5
    >>> delta = 2

    >>> h = cp.Variable(pos=True, name="h")
    >>> w = cp.Variable(pos=True, name="w")
    >>> d = cp.Variable(pos=True, name="d")

    >>> volume = h * w * d
    >>> wall_area = 2 * (h * w + h * d)
    >>> flr_area = w * d
    >>> hw_ratio = h/w
    >>> dw_ratio = d/w
    >>> constraints = [wall_area <= A_wall,flr_area <= A_flr,hw_ratio >= alpha,hw_ratio <= beta,dw_ratio >= gamma,dw_ratio <= delta]
    >>> objective=cp.Maximize(volume)
    >>> v = Visual(objective)
    >>> stri=str(objective.expr).replace("+ -", " - ")
    >>> stri==v.root.expr
    True
    >>> v.root.checkin_sons('@')
    True
    >>> v.root.checkin_sons('h')
    False
    >>> n = v.root.node_son('@')
    >>> n.checkin_sons('h')
    True
    >>> n.checkin_sons(n.sons[0].expr)
    True
    >>> n.checkin_sons('c')
    False
    >>> n.checkin_sons(n.sons[1].expr)
    True
    >>> n=n.node_son(n.sons[1].expr)
    >>> n.checkin_sons('@')
    True
    >>> n=n.node_son('@')
    >>> n.checkin_sons(n.sons[0].expr)
    True
    >>> n.checkin_sons(n.sons[1].expr)
    True
    >>> n.checkin_sons('x')
    False

    >>> objective=cp.Maximize(h)
    >>> v = Visual(objective)
    >>> v.root.checkin_sons('+')
    False
    >>> len(v.root.sons)
    0
    >>> objective=Minimize(quad_form(x, P))
    >>> stri=str(objective.expr).replace("+ -", " - ")
    >>> v = Visual(objective)
    >>> v.root.checkin_sons('QuadForm')
    True
    >>> v.root.checkin_sons('var1')
    False
    >>> n=v.root.node_son('QuadForm')
    >>> n.checkin_sons('var1')
    True
    >>> n.checkin_sons(str(P))
    True
    >>> volume = h * w + d
    >>> objective=cp.Maximize(volume)
    >>> v = Visual(objective)
    >>> v.root.checkin_sons('@')
    False
    >>> v.root.checkin_sons('+')
    True
    >>> n=v.root.node_son('+')
    >>> n.checkin_sons('d')
    True
    >>> n.checkin_sons('h @ w')
    True

    # test for check_func
    >>> x = Variable()
    >>> exp = -quad_form(x, P)
    >>> op = "quad_form(x, P)"
    >>>v.check_func(exp,op)
    True

"""
if __name__ == '__main__':
    import doctest
    doctest.testmod()