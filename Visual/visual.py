import re
from email.headerregistry import Group
import cvxpy as cp
import networkx as nx
from cvxpy import Expression

import cvxopt

from cvxpy import Minimize, Problem, Variable, quad_form
from cvxpy.problems.objective import Objective

import operator

from matplotlib import pyplot as plt
from networkx import Graph

from Visual.binary_tree import Node

priority1 = ['@', '*', '/']
priority2 = ['+', '-']
op = ['**', '@', '*', '/', '+', '-']


def is_operator(s):
    try:
        return hasattr(operator, s)
    except TypeError:
        return False


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Visual:
    def __init__(self, obj: Objective):
        self.name = obj.NAME
        self.expr = str(obj.expr)
        self.parameters = []
        self.variables = []
        self.operators = []
        self.func = []
        self.root = Node(None, self.expr, 0)
        self.create_lists(self.expr)
        self.split_expr(self.root)
        self.root.print_tree()
        # self.create_tree()

    def create_lists(self, exp):
        isFunc = False
        isMatrix = False
        func_string = ""
        matrix_string = ""
        list_op = []
        exp2 = exp.replace("+ -", " - ")
        for s in exp2.split():
            # --------func---------
            if ')' in s:
                isFunc = False
                func_string += " " + s
                self.func.append(func_string)
                self.operators.append(func_string)
                list_op.append(func_string)
                func_string = ""
                continue
            if isFunc:
                func_string += " " + s
                continue
            if '(' in s:
                isFunc = True
                func_string += s
                continue
            # --------func---------

            # --------parameter---------
            if is_float(s) and not isMatrix:
                self.parameters.append(s)
                continue
            if ']' in s:
                isMatrix = False
                matrix_string += " " + s
                self.parameters.append(matrix_string)
                matrix_string = ""
                continue
            if isMatrix:
                matrix_string += " " + s
                continue
            if '[' in s:
                isMatrix = True
                matrix_string += s
                continue
            # --------parameter---------

            # --------variables---------
            if "var" in s:
                self.variables.append(s)
                continue
            # --------variables---------

            if s in op:
                self.operators.append(s)
                list_op.append(s)
        return list_op

    def split_expr(self, exp: Node):
        o = self.priority(exp.expr)
        if o is None:
            return
        if o in self.func:
            exp.insert_func(o)
        else:
            exp.insert(o)
        for p in exp.sons[0].sons:
            self.split_expr(p)

    def show(self):
        pass

    def create_tree(self):
        g = nx.Graph()
        g.add_node("first")
        g.add_node(self.root.son.value)
        g.add_edge("first", self.root.son.value, label=self.root.expr)
        self.create_tree_r(g, self.root.son)
        pos = nx.spring_layout(g)
        edge_labels = nx.get_edge_attributes(g, 'label')
        nx.draw(g, pos, with_labels=True)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
        plt.show()

    def create_tree_r(self, g: Graph, node: Node):
        for s in node.sons:
            if s.son:
                g.add_node(s.son.value)
                g.add_edge(s.son, node.value, label=s.expr)
                self.create_tree_r(g, s.son)
            else:
                g.add_node("end")
                g.add_edge("end", node.value)

    def priority(self, exp):
        pr = 0
        ans = ''
        ops = self.create_lists(exp)
        if not ops:
            return None
        for o in ops:
            if o in priority2:
                return o
            if o in priority1:
                pr = 1
                ans = o
            elif pr == 0:
                ans = o
        return ans


n = 3
P = cvxopt.matrix([13, 12, -2,
                   12, 17, 6,
                   -2, 6, 12], (n, n))
q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
r = 1
x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))

# Frame and solve the problem

x = Variable(n)
y = Variable()
objective = Minimize(0.5 * quad_form(x, P) - cp.sum_squares(x) + q.T @ x + r)
# objective = cp.Minimize((x - y) ** 2)
constraints = [x >= -1, x <= 1]

# p = Problem(objective, constraints)
# # The optimal objective is returned by p.solve().
# result = p.solve()
print(str(objective.expr))

# expression = "2 * math.pow(3, 2) + math.sqrt(16)"
# tokens = re.findall('[\d\.]+|\(|\)|\+|\-|\@|\/|\^|\w+\(', str(objective.expr))
#
# print(tokens)

# for s in str(objective.expr).split():
#     print("s= ", s)

v = Visual(objective)
# print(v.func)
# print(v.parameters)
# print(v.variables)
