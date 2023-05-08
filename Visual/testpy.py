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
    x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))
    x = Variable(n)
    y = Variable()
    z = Variable(n)
    objective = Minimize(0.5 * quad_form(x, P) - cp.sum_squares(x) + q.T @ x + r + y)
    v = Visual(objective)
    stri = str(objective.expr).replace("+ -", " - ")
    assert stri == v.root.expr
    assert not v.root.checkin_sons('@')
    assert v.root.checkin_sons('-')
    n = v.root.node_son('-')
    assert n.checkin_sons('0.5 @ QuadForm(var1, [[13. 12. -2.] [12. 17.  6.] [-2.  6. 12.]])')
    n = n.sons[0]
    assert n.checkin_sons('@')
    n = n.sons[0]
    assert n.checkin_sons('0.5')
    assert n.checkin_sons('QuadForm(var1, [[13. 12. -2.] [12. 17.  6.] [-2.  6. 12.]])')
    n = n.sons[1]
    assert not n.checkin_sons('var1')
    assert n.checkin_sons('QuadForm')



def test_create_lists():
    pass


def test_curvature_sign():
    pass


# --------------visual--------------

# --------------expression_tree--------------
def test_insert():
    pass


def test_insert_func():
    pass


# --------------expression_tree--------------


def test_code():
    # n = 3
    # P = cvxopt.matrix([13, 12, -2, 12, 17, 6, -2, 6, 12], (n, n))
    # q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    # r = 1
    # x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))
    # x = Variable(n)
    # y = Variable()
    # z = Variable(n)
    # objective = Minimize(0.5 * quad_form(x, P) - cp.sum_squares(x) + q.T @ x + r + y)
    # v = Visual(objective)
    # stri = str(objective.expr).replace("+ -", " - ")
    # assert stri == v.root.expr
    # assert v.root.checkin_sons('-')
    # n = v.root.node_son('-')
    # assert n.checkin_sons('0.5 @ QuadForm(var1, [[13. 12. -2.] [12. 17.  6.] [-2.  6. 12.]])')
    # A_wall = 100
    # A_flr = 10
    # alpha = 0.5
    # beta = 2
    # gamma = 0.5
    # delta = 2
    # h = cp.Variable(pos=True, name="h")
    # w = cp.Variable(pos=True, name="w")
    # d = cp.Variable(pos=True, name="d")
    # volume = h * w * d
    # wall_area = 2 * (h * w + h * d)
    # flr_area = w * d
    # hw_ratio = h / w
    # dw_ratio = d / w
    # constraints = [wall_area <= A_wall, flr_area <= A_flr, hw_ratio >= alpha, hw_ratio <= beta, dw_ratio >= gamma,
    #                dw_ratio <= delta]
    # objective = cp.Maximize(volume)
    # v = Visual(objective)
    # stri = str(objective.expr).replace("+ -", " - ")
    # assert stri == v.root.expr
    # assert v.root.checkin_sons('@')
    # assert not v.root.checkin_sons('h')
    # n = v.root.node_son('@')
    # assert n.checkin_sons('h')
    # assert n.checkin_sons(n.sons[0].expr)
    # assert not n.checkin_sons('c')
    # assert n.checkin_sons(n.sons[1].expr)
    # n = n.node_son(n.sons[1].expr)
    # assert n.checkin_sons('@')
    # n = n.node_son('@')
    # assert n.checkin_sons(n.sons[0].expr)
    # assert n.checkin_sons(n.sons[1].expr)
    # assert not n.checkin_sons('x')
    # #still need to split the object to the other tests
    # objective = cp.Maximize(h)
    # v = Visual(objective)
    # assert not v.root.checkin_sons('+')
    # assert len(v.root.sons) == 0
    # objective = Minimize(quad_form(x, P))
    # stri = str(objective.expr).replace("+ -", " - ")
    # v = Visual(objective)
    # assert v.root.checkin_sons('QuadForm')
    # assert not v.root.checkin_sons('var1')
    # n = v.root.node_son('QuadForm')
    # assert n.checkin_sons('var1')
    # assert n.checkin_sons(str(P))
    # volume = h * w + d
    # objective = cp.Maximize(volume)
    # v = Visual(objective)
    # assert not v.root.checkin_sons('@')
    # assert v.root.checkin_sons('+')
    # n = v.root.node_son('+')
    # assert n.checkin_sons('d')
    # assert n.checkin_sons('h @ w')
    # x = Variable()
    # exp = -quad_form(x, P)
    # op = "quad_form(x, P)"
    # assert v.check_func(exp, op)
    pass



