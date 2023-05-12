from Visual import *
import numpy as np
from Visual import expression_tree, visual
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import font, ttk
import cvxpy as cp
import cvxopt
from cvxpy import Minimize, Problem, Variable, quad_form
from cvxpy.problems.objective import Objective
import operator
from Visual.expression_tree import Node
from Visual.visual import Visual


# --------------visual--------------
def test_split_expr():
    A_wall = 100
    A_flr = 10
    alpha = 0.5
    beta = 2
    gamma = 0.5
    delta = 2
    h = cp.Variable(pos=True, name="h")
    w = cp.Variable(pos=True, name="w")
    d = cp.Variable(pos=True, name="d")
    volume = h * w * d
    wall_area = 2 * (h * w + h * d)
    flr_area = w * d
    hw_ratio = h / w
    dw_ratio = d / w
    constraints = [wall_area <= A_wall, flr_area <= A_flr, hw_ratio >= alpha, hw_ratio <= beta, dw_ratio >= gamma,
                   dw_ratio <= delta]
    objective = cp.Maximize(volume)
    v = Visual(objective)
    stri = str(objective.expr).replace("+ -", " - ")
    assert stri == v.root.expr
    assert v.root.checkin_sons('@')
    assert not v.root.checkin_sons('h')
    n = v.root.node_son('@')
    assert n.checkin_sons('h')
    assert n.checkin_sons(n.sons[0].expr)
    assert not n.checkin_sons('c')
    assert n.checkin_sons(n.sons[1].expr)
    n = n.node_son(n.sons[1].expr)
    assert n.checkin_sons('@')
    n = n.node_son('@')
    assert n.checkin_sons(n.sons[0].expr)
    assert n.checkin_sons(n.sons[1].expr)
    assert not n.checkin_sons('x')


def test_priority():
    n = 3
    P = cvxopt.matrix([13, 12, -2, 12, 17, 6, -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1
    x = Variable(n)
    y = Variable()
    objective = Minimize(0.5 * quad_form(x, P) - cp.sum_squares(x) + q.T @ x + r + y)

    v = Visual(objective)
    assert '-' == v.priority(v.expr)
    assert not '@' == v.priority(v.expr)
    n = v.root.node_son('-')
    n = n.sons[0]
    assert '@' == v.priority(n.expr)
    assert not 'QuadForm' == v.priority(n.expr)
    n = v.root.node_son('-').sons[1]
    assert '+' == v.priority(n.expr)
    n = n.sons[0].sons[1]
    assert '+' == v.priority(n.expr)
    n = n.sons[0].sons[1]
    assert '+' == v.priority(n.expr)
    n = v.root.node_son('-').sons[1].sons[0].sons[1].sons[0].sons[0]
    assert '@' == v.priority(n.expr)
    # stri = str(objective.expr).replace("+ -", " - ")
    # assert stri == v.root.expr
    # assert not v.root.checkin_sons('@')
    # assert v.root.checkin_sons('-')
    # n = v.root.node_son('-')
    # assert n.checkin_sons('0.5 @ QuadForm(var1, [[13. 12. -2.] [12. 17.  6.] [-2.  6. 12.]])')
    # n = n.sons[0]
    # assert n.checkin_sons('@')
    # n = n.sons[0]
    # assert n.checkin_sons('0.5')
    # assert n.checkin_sons('QuadForm(var1, [[13. 12. -2.] [12. 17.  6.] [-2.  6. 12.]])')
    # n = n.sons[1]
    # assert not n.checkin_sons('var1')
    # assert n.checkin_sons('QuadForm')


def test_create_lists():
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1

    x1 = Variable(n)
    y1 = Variable()
    x2 = Variable()
    y2 = Variable()

    objective = Minimize(-1 * ((y2) ** 2) + 2 * y2)
    objective1 = Minimize((x2 - y2) ** 2)
    objective2 = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)
    v = Visual(objective)
    rightOperators = ['@', '+']
    rightVaribale = ['var97']
    rightFunc = ['power(var97, 2.0)']
    v.create_lists(v.expr)
    for e in rightFunc:
        assert e in v.func
    assert not 'QuardForm' in v.func
    for o in rightOperators:
        assert o in v.operators
    assert not '/' in v.operators
    for s in rightVaribale:
        assert s in v.variables
    assert not str(x1.expr) in v.variables
    v = Visual(objective1)
    v.create_lists(v.expr)
    rightOperators = ['power(var96 - var97, 2.0)']
    rightVaribale = ['var96', 'var97']
    rightFunc = ['power(var96 - var97, 2.0)']
    for e in rightFunc:
        assert e in v.func
    assert not 'QuardForm' in v.func
    assert not '/' in v.operators
    for s in rightVaribale:
        assert s in v.variables
    assert not str(x1.expr) in v.variables
    v = Visual(objective2)
    v.create_lists(v.expr)
    rightOperators = ['-', '+', '@']
    rightVaribale = ['var94']
    rightFunc = ['QuadForm(var94, [[13. 12. -2.] [12. 17. 6.] [-2. 6. 12.]])', 'quad_over_lin(var94, 1.0)']
    for e in rightFunc:
        assert e in v.func
    assert not 'power' in v.func
    for o in rightOperators:
        assert o in v.operators
    assert not '/' in v.operators
    for s in rightVaribale:
        assert s in v.variables
    assert not str(x2.expr) in v.variables


def test_curvature_sign():
    x = Variable()
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1
    x1 = Variable(n)
    y1 = Variable()
    objective = Minimize(-1 * x ** 2 + 2 * x)
    v = Visual(objective)
    rightCurvature_sign = [['-1.0 @ power(var1, 2.0) + 2.0 @ var1', 'CONCAVE', 'UNKNOWN'],
                           ['-1.0 @ power(var1, 2.0)', 'CONVEX', 'POSITIVE'], ['2.0 @ var1', 'AFFINE', 'UNKNOWN'],
                           ['-1.0', 'CONSTANT', 'POSITIVE'], ['power(var1, 2.0)', 'CONVEX', 'POSITIVE'],
                           ['var1', 'AFFINE', 'UNKNOWN'], [' 2.0', 'CONSTANT', 'POSITIVE'],
                           ['2.0', 'CONSTANT', 'NONNEGATIVE'], ['var1', 'AFFINE', 'UNKNOWN']]
    for c in rightCurvature_sign:
        assert c in v.curvature_sign_list

    objective = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)
    v = Visual(objective)
    rightCurvature_sign = [['0.5 @ QuadForm(var2, [[13. 12. -2.]\n [12. 17.  6.]\n [-2.  6. 12.]])  - '
                            'quad_over_lin(var2, 1.0) + [[-22.  -14.5  13. ]] @ var2 + 1.0 + var3', 'UNKNOWN',
                            'UNKNOWN']
        , ['0.5 @ QuadForm(var2, [[13. 12. -2.]\n [12. 17.  6.]\n [-2.  6. 12.]])', 'CONVEX', 'POSITIVE'],
                           ['-quad_over_lin(var2, 1.0) + [[-22.  -14.5  13. ]] @ var2 + 1.0 + var3', 'CONVEX',
                            'UNKNOWN'], ['0.5', 'CONSTANT', 'POSITIVE'],
                           ['QuadForm(var2, [[13. 12. -2.]\n [12. 17.  6.]\n [-2.  6. 12.]])', 'CONVEX', 'POSITIVE'],
                           ['var2', 'AFFINE', 'UNKNOWN'],
                           ['[[13. 12. -2.]\n [12. 17.  6.]\n [-2.  6. 12.]]', 'CONSTANT', 'UNKNOWN'],
                           ['-quad_over_lin(var2, 1.0)', 'CONVEX', 'POSITIVE'],
                           ['[[-22.  -14.5  13. ]] @ var2 + 1.0 + var3', 'AFFINE', 'UNKNOWN'],
                           ['var2', 'AFFINE', 'UNKNOWN'], ['1.0', 'CONSTANT', 'POSITIVE'],
                           ['[[-22.  -14.5  13. ]] @ var2', 'AFFINE', 'UNKNOWN'], ['1.0 + var3', 'AFFINE', 'UNKNOWN'],
                           ['[[-22.  -14.5  13. ]]', 'CONSTANT', 'UNKNOWN'], ['var2', 'AFFINE', 'UNKNOWN'],
                           ['1.0', 'CONSTANT', 'NONNEGATIVE'], ['var3', 'AFFINE', 'UNKNOWN']]
    for c in rightCurvature_sign:
        assert c in v.curvature_sign_list
    #
    objective = Minimize(x ** 3)
    v = Visual(objective)
    rightCurvature_sign = [['power(var1, 3.0)', 'CONVEX', 'POSITIVE'], ['var1', 'AFFINE', 'UNKNOWN'],
                           [' 3.0', 'CONSTANT', 'POSITIVE']]
    for c in rightCurvature_sign:
        assert c in v.curvature_sign_list

    objective = Minimize(cp.log(x))
    v = Visual(objective)
    rightCurvature_sign = [['log(var1)', 'CONCAVE', 'UNKNOWN'], ['var1', 'AFFINE', 'UNKNOWN']]
    for c in rightCurvature_sign:
        assert c in v.curvature_sign_list

    objective = Minimize(2 * cp.exp(-x) - cp.sqrt(cp.log(1 + x ** -2)))
    v = Visual(objective)
    rightCurvature_sign = [['2.0 @ exp(-var1)  - power(log(1.0 + power(var1, -2.0)), 0.5)', 'UNKNOWN', 'UNKNOWN'],
                           ['2.0 @ exp(-var1)', 'CONVEX', 'POSITIVE'],
                           ['-power(log(1.0 + power(var1, -2.0)), 0.5)', 'QUASILINEAR', 'POSITIVE'],
                           ['2.0', 'CONSTANT', 'POSITIVE'], ['exp(-var1)', 'CONVEX', 'POSITIVE'],
                           ['-var1', 'AFFINE', 'UNKNOWN'], ['log(1.0 + power(var1, -2.0))', 'QUASILINEAR', 'UNKNOWN'],
                           [' 0.5', 'CONSTANT', 'POSITIVE'], ['1.0 + power(var1, -2.0)', 'CONVEX', 'POSITIVE'],
                           ['1.0', 'CONSTANT', 'POSITIVE'], ['power(var1, -2.0)', 'CONVEX', 'POSITIVE'],
                           ['var1', 'AFFINE', 'UNKNOWN'], [' -2.0', 'CONSTANT', 'NEGATIVE']]
    for c in rightCurvature_sign:
        assert c in v.curvature_sign_list


# --------------visual--------------

# --------------expression_tree--------------
def test_insert():
    n = Node(None, 'h + w @ x', 0)
    assert len(n.sons) == 0
    n.insert('+')
    assert len(n.sons[0].sons) == 2
    assert n.sons[0].sons[0].expr.contain('h')
    assert n.sons[0].sons[1].expr.contain('w @ x')
    assert not n.sons[0].sons[1].expr.contain('h @ x')
    assert len(n.sons[0].sons[1].sons) == 0
    n.sons[0].sons[1].insert('@')
    assert len(n.sons[0].sons[1].sons) == 1
    n = Node(None, 'h', 0)
    n.insert('@')
    assert len(n.sons[0].sons) == 0
    n = Node(None, 'h @ w @ s', 0)
    n.insert('+')
    assert len(n.sons[0].sons) == 0







def test_insert_func():
    n = Node(None, 'h + w @ x', 0)
    s = 2
    P = cvxopt.matrix([1, -2,
                       4, 12], (s, s))
    x1 = Variable(s)
    objective= P @ x1
    y = Node (None,'power('+str(objective)+',2.0)',0)
    y.insert_func('power('+str(objective)+',2.0)')
    assert y.sons[0].expr == 'power'
    assert y.sons[0].sons[0].expr.__contains__(str(objective))
    n.insert_func('quad_over_lin(var2, 1.0)')
    assert n.sons[0].sons[0].expr.__contains__('var2')

# --------------expression_tree--------------

test_curvature_sign()
test_split_expr()
test_priority()
test_create_lists()
