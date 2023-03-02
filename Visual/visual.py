import tkinter as tk
from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import font, ttk

from future.moves.tkinter import ttk
import cvxpy as cp
import cvxopt
from cvxpy import Minimize, Problem, Variable, quad_form
from cvxpy.problems.objective import Objective
import operator

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
        self.root = Node(None, self.expr, 0, 0)
        self.create_lists(self.expr)
        self.split_expr(self.root)
        self.root.print_tree()
        self.show()

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
        window = tk.Tk()
        window.title("My GUI")

        # Create a Treeview widget
        tree = ttk.Treeview(window)
        self.create_tree_r(tree, self.root)
        font = tk.font.Font()

        # Use the font object to measure the width of the text
        width = font.measure(self.root.expr)

        # Set the width of the first column to the measured width
        tree.column("#0", width=width)
        tree.configure(height=1000)
        # Pack the Treeview widget
        tree.pack()
        # Run the event loop
        window.mainloop()

    def create_tree_r(self, tree: Treeview, node: Node):
        # Define the tree structure
        if node.father:
            if node.sons:
                tree.insert(node.father.name, node.number, node.name, text=node.expr)
                tree.insert(node.name, node.sons[0].number, node.sons[0].name, text=node.sons[0].expr)
                for son in node.sons[0].sons:
                    self.create_tree_r(tree, son)
            else:
                tree.insert(node.father.name, node.number, node.name, text=node.expr)
        else:
            tree.insert("", "end", "root", text=node.expr)
            tree.insert("root", node.number, node.sons[0].name, text=node.sons[0].expr)
            for son in node.sons[0].sons:
                self.create_tree_r(tree, son)

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

    def draw_graph(self):
        pass

    def draw_constrain(self):
        pass

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
