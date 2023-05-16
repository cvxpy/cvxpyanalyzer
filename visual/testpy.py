import cvxpy as cp
import cvxopt
import numpy as np
from cvxpy import Minimize, Variable, quad_form
import pytest

from visual.expression_tree import Node
from visual.visual_expression import Visual


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


def test_create_lists():
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1

    x1 = Variable(n, name='var3')
    y1 = Variable(name='y1')
    x2 = Variable(name='var1')
    y2 = Variable(name='var2')

    objective = Minimize(-1 * ((y2) ** 2) + 2 * y2)
    objective1 = Minimize((x2 - y2) ** 2)
    objective2 = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)
    v = Visual(objective)
    rightOperators = ['@', '+']
    rightVaribale = ['var2']
    rightFunc = ['power(var2, 2.0)']
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
    rightVaribale = ['var1', 'var2']
    rightFunc = ['power(var1 - var2, 2.0)']
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
    rightVaribale = ['var3']
    rightFunc = ['QuadForm(var3, [[13. 12. -2.] [12. 17. 6.] [-2. 6. 12.]])', 'quad_over_lin(var3, 1.0)']
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
    x = Variable(name='var1')
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1
    x1 = Variable(n, name='var2')
    y1 = Variable(name='var3')
    objective = Minimize(-1 * x ** 2 + 2 * x)
    v = Visual(objective)
    rightCurvature_sign = [['-1.0 @ power(var1, 2.0) + 2.0 @ var1', 'CONCAVE', 'UNKNOWN'],
                           ['-1.0 @ power(var1, 2.0)', 'CONCAVE', 'NEGATIVE'], ['2.0 @ var1', 'AFFINE', 'UNKNOWN'],
                           ['-1.0', 'CONSTANT', 'NEGATIVE'], ['power(var1, 2.0)', 'CONVEX', 'POSITIVE'],
                           ['var1', 'AFFINE', 'UNKNOWN'], [' 2.0', 'CONSTANT', 'POSITIVE'],
                           ['2.0', 'CONSTANT', 'POSITIVE'], ['var1', 'AFFINE', 'UNKNOWN']]
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
                           ['1.0', 'CONSTANT', 'POSITIVE'], ['var3', 'AFFINE', 'UNKNOWN']]
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
    assert str(n.sons[0].sons[0].expr).__contains__('h')
    assert str(n.sons[0].sons[1].expr).__contains__('w @ x')
    assert not str(n.sons[0].sons[1].expr).__contains__('h @ x')
    assert len(n.sons[0].sons[1].sons) == 0
    n.sons[0].sons[1].insert('@')
    assert len(n.sons[0].sons[1].sons) == 1
    n = Node(None, 'h', 0)
    n.insert('@')
    assert len(n.sons) == 0
    n = Node(None, 'h @ w @ s', 0)
    n.insert('+')
    assert len(n.sons) == 0
    s = 4
    P = cvxopt.matrix([1, -2, 10, 17,
                       4, 12, 99, 13,
                       0, 1, 6, 73,
                       43, 100, 54, 2], (s, s))
    WorngP = '[[  1.   4.   0.  43.]\n [ -2.  12.   1. 100.]\n [ 10.  99.   6.  54.]\n [ 17.  13.  73.   1.]] '
    x1 = Variable(s, name='var9')
    x2 = Variable((s, s), symmetric=True, name='var10')
    objective = P @ x1
    y = Node(None, str(objective), 0)
    y.insert('+')
    assert len(y.sons) == 0
    y.insert('@')
    assert len(y.sons) == 1
    z = '[[  1.   4.   0.  43.]\n [ -2.  12.   1. 100.]\n [ 10.  99.   6.  54.]\n [ 17.  13.  73.   2.]] '
    assert y.sons[0].sons[0].expr.__contains__(z)
    assert not y.sons[0].sons[0].expr.__contains__(WorngP)
    assert y.sons[0].sons[1].expr.__contains__('var9')
    objective = P + x2
    y = Node(None, str(objective), 0)
    y.insert('@')
    assert len(y.sons) == 0
    y.insert('+')
    assert len(y.sons) == 1
    assert y.sons[0].sons[0].expr.__contains__(z)
    assert not y.sons[0].sons[0].expr.__contains__(WorngP)
    assert y.sons[0].sons[1].expr.__contains__('var10')
    objective = (P + x2) @ x1
    y = Node(None, str(objective), 0)
    # y.insert('+')
    # assert len(y.sons) == 0
    y.insert('@')
    assert len(y.sons) == 1
    assert y.sons[0].sons[1].expr.__contains__('var9')
    assert y.sons[0].sons[0].expr.__contains__(
        '([[  1.   4.   0.  43.]\n [ -2.  12.   1. 100.]\n [ 10.  99.   6.  54.]\n [ 17.  13.  73.   2.]] + var10) ')


def test_insert_func():
    n = Node(None, 'h + w @ x', 0)
    s = 2
    P = cvxopt.matrix([1, -2,
                       4, 12], (s, s))
    x1 = Variable(s)
    objective = P @ x1
    y = Node(None, 'power(' + str(objective) + ',2.0)', 0)
    y.insert_func('power(' + str(objective) + ',2.0)')
    assert y.sons[0].expr == 'power'
    assert y.sons[0].sons[0].expr.__contains__(str(objective))
    n.insert_func('quad_over_lin(var2, 1.0)')
    assert n.sons[0].sons[0].expr.__contains__('var2')
    n = Node(None, 'h + w @ x', 0)
    # create a variable
    # define the objective as a quadratic form
    s = 10
    P = np.random.randn(s, s)
    P = P.T @ P
    x1 = Variable(s)
    objective = cp.quad_form(x1, P)
    # create a node for the objective squared
    y = Node(None, 'power(' + str(objective) + ',2.0)', 0)
    # test that the power function is inserted correctly
    y.insert_func('power(' + str(objective) + ',2.0)')
    assert y.sons[0].expr == 'power'
    assert y.sons[0].sons[0].expr.__contains__(str(objective))

    # create another node
    n2 = Node(None, 'max(a, b)', 0)
    # insert a new function into the node
    n2.insert_func('exp(c)')
    # test that the function is inserted correctly
    assert n2.sons[0].expr == 'exp'
    assert n2.sons[0].sons[0].expr == 'c'

    # create a node with a variable
    n3 = Node(None, 'x', 0)
    # insert a new function into the node
    n3.insert_func('abs(var1)')
    # test that the function is inserted correctly
    assert n3.sons[0].expr == 'abs'
    assert n3.sons[0].sons[0].expr == 'var1'


# --------------expression_tree--------------

pytest.main()
