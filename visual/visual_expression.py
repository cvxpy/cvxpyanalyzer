from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import font, ttk

import numpy as np
from cvxpy.problems.objective import Objective, Minimize
import operator
import re
from graphviz import Digraph
from matplotlib import pyplot as plt
from visual.expression_tree import Node

"""
first we split the expression according to the high priority
and then according to the low priority
"""
# low priority
priority1 = ['@', '*', '/']
# high priority
priority2 = ['+', '-']
# all operators
op = ['@', '*', '/', '+', '-']


# This function checks if the character is of type operator
def is_operator(s):
    try:
        return hasattr(operator, s)
    except TypeError:
        return False


# This function checks if the character is a number
def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_matrix(s):
    if len(s) > 2 and s[0] == '[' and s[-1] == "]":
        return True
    else:
        return False


class Visual:

    def __init__(self, obj: Objective):
        self.ob = obj
        # Minimize/Maximize
        self.name = obj.NAME
        # converts the expression to a string and replaces + - with '-' to make it clearer
        self.expr = str(obj.expr).replace("+ -", " - ")
        # creating 4 lists so that each one represents a different type of character
        self.parameters = []
        self.variables = []
        self.operators = []
        # List of operators ordered by priority
        self.priority_op = []
        # function is a type of operator
        self.func = []
        # create the first node, it has no father and brothers,
        # its type is an expression and its value is the expression that the class received
        self.root = Node(None, self.expr, 0)
        # split the expression
        self.split_expr(self.root)
        self.left = True
        # create a list that contain the expression ,the curvature and the sign of the expression
        self.curvature_sign_list = [[str(self.expr), self.ob.expr.curvature, self.ob.expr.sign]]
        # the index of priority_op
        self.index = 0
        # create again all the lists
        self.create_lists(self.expr)
        # create curvature_sign_list
        self.curvature_sign(self.ob.expr)
        self.order_curvature_sign_list()
        self.curvature_sign_node(self.root)
        self.index = 0

    def split_expr(self, exp: Node):
        """
         This function divides the expression recursively,
         each node of type expression has a single child which is the operator with the highest priority
         and each node of type operator has children which are the division of the previous expression
         according to the operator
        """
        # Finding the highest priority operator in the current expression
        o = self.priority(exp.expr)
        # There are no more operators in the current expression
        # and therefore the expression is either a variable or a parameter
        if o is None:
            return
        # If the operator is a function, this means that the expression needs to be divided
        # in a different way to find all the parameters inside the function
        if o in self.func:
            # create a new Node and insert into the tree
            exp.insert_func(o)
        # If the operator is not a function type, that means it will have two children
        else:
            exp.insert(o)
        # After creating the new nodes we will go through the children of the child (single child)
        # of the current node and call this function
        for p in exp.sons[0].sons:
            self.split_expr(p)

    def priority(self, exp):
        """
        This function takes the expression and looks for the operator with the highest priority
        """
        # pr = 0 if the highest priority is a function
        pr = 0
        ans = ''
        # call to the function that creates the lists of the class
        self.create_lists(exp)
        # There are no more operators in the current expression
        # and therefore the expression is either a variable or a parameter
        if not self.operators:
            return None
        for o in self.operators:
            if o in priority2:
                # priority2 is the highest priority so we can stop here
                self.priority_op.append(o)
                return o
            if o in priority1:
                # now we can know that the operator with the highest priority is not a function
                pr = 1
                ans = o
            elif pr == 0:
                ans = o
        self.priority_op.append(ans)
        return ans

    def create_lists(self, exp):
        """
        This function creating the four lists based on the expression she gets
        """
        # Reset the lists
        self.parameters = []
        self.variables = []
        self.operators = []
        self.func = []
        isFunc = False
        isMatrix = False
        func_string = ""
        matrix_string = ""
        counter1 = 0
        # we will go through all the characters in the string
        for s in exp.split():
            # --------variables---------
            if "var" in s:
                index = s.index("var")
                new_var = "var"
                for char in s[index + 3:]:
                    if char.isdigit():
                        new_var += char
                    else:
                        break
                if new_var not in self.variables:
                    self.variables.append(new_var)
            # --------variables---------

            # --------function---------
            # The expression of the function is over
            if ')' in s:
                counter1 += s.count('(')
                counter1 -= s.count(')')
                if counter1 == 0:
                    isFunc = False
                    func_string += " " + s
                    # We will put the expression of the function in the list of functions
                    # and also in the list of operators because it is a type of operator
                    self.func.append(func_string)
                    self.operators.append(func_string)
                    func_string = ""
                    continue
                if counter1 != 0:
                    func_string += s
                    continue
                isFunc = False
                func_string += " " + s
                # We will put the expression of the function in the list of functions
                # and also in the list of operators because it is a type of operator
                self.func.append(func_string)
                self.operators.append(func_string)
                func_string = ""
                continue
            if isFunc:
                counter1 += s.count('(')
                func_string += " " + s
                continue
            # The expression of the function is start
            if '(' in s:
                isFunc = True
                counter1 += s.count('(')
                counter1 -= s.count(')')
                if counter1 == 0:
                    isFunc = False
                    func_string += " " + s
                    # We will put the expression of the function in the list of functions
                    # and also in the list of operators because it is a type of operator
                    self.func.append(func_string)
                    self.operators.append(func_string)
                    func_string = ""
                    continue
                func_string += s
                continue
            # --------function---------

            # --------parameter---------
            # We will insert a parameter into the list only if it is not inside a matrix
            if is_float(s) and not isMatrix:
                self.parameters.append(s)
                continue
            # The expression of the matrix is over
            if ']' in s:
                isMatrix = False
                matrix_string += " " + s
                # We will put the expression of the matrix in the list of parameter
                self.parameters.append(matrix_string)
                matrix_string = ""
                continue
            if isMatrix:
                matrix_string += " " + s
                continue
            # The expression of the matrix is start
            if '[' in s:
                isMatrix = True
                matrix_string += s
                continue
            # --------parameter---------

            # --------operators---------
            if s in op:
                self.operators.append(s)
            # --------operators---------

    def show_and_save(self, file_name):
        """
        The purpose of this function is to visually show the created tree using graphiz
        """
        dot = Digraph()
        self.create_digraph(dot, self.root, 0, "")
        dot.render(file_name, view=True)

    def create_digraph(self, dot: Digraph, node: Node, count, expr2: str):
        # if the node is not the root
        if node.father:
            # insert the expression of the current node
            y = str(node.name)
            dot.node(y, node.expr)
            dot.edge(expr2, y)

            if node.curvature != 'CONSTANT':
                z = 'C' + str(node.c_curvature)
                dot.node(z, node.curvature, color='#40e0d0', shape='box', style='filled', fillcolor='#40e0d0')
                dot.edge(z, y)

            if node.sign is not None:
                p = 'B' + str(node.c_sign)
                dot.node(p, node.sign, color='#ff000042', shape='box', style='filled', fillcolor='#ff000042')
                dot.edge(p, y)

            if node.sons:
                x = node.sons[0].name
                dot.node(str(x), node.sons[0].expr)  # -
                dot.edge(y, str(x))

                c = 0
                for son in node.sons[0].sons:
                    self.create_digraph(dot, son, c, str(x))
                    c += 1
        # the node is the root
        else:
            y = str(node.name)
            dot.node(y, node.expr)

            z = 'C' + str(node.c_curvature)
            dot.node(z, node.curvature, color='#40e0d0', shape='box', style='filled', fillcolor='#40e0d0')
            dot.edge(z, y)

            p = 'B' + str(node.c_sign)
            dot.node(p, node.sign, color='#ff000042', shape='box', style='filled', fillcolor='#ff000042')
            dot.edge(p, y)

            if node.sons:
                x = str(node.sons[0].name)
                dot.node(x, node.sons[0].expr)
                dot.edge(y, x)

                c = 0
                for son in node.sons[0].sons:
                    self.create_digraph(dot, son, c, str(x))
                    c += 1

    def show(self):
        """
        The purpose of this function is to visually show the created tree using tkinter
        """
        window = tk.Tk()
        window.title("My GUI")
        # Create a Treeview widget
        tree = ttk.Treeview(window)
        self.create_tree(tree, self.root, 0)
        style = ttk.Style()
        style.configure("Treeview", rowheight=50, font=('Arial', 10))
        # Use the font object to measure the width of the text
        width = tk.font.Font().measure(self.root.expr)

        # Set the width of the first column to the measured width
        tree.column("#0", width=width)
        tree.configure(height=1000)
        # Pack the Treeview widget
        tree.pack()
        # Run the event loop
        window.mainloop()

    def create_tree(self, tree: Treeview, node: Node, count):
        """
        This function recursively creates the tree using Treeview
        """
        # if the node is not the root
        if node.father:
            # insert the expression of the current node
            tree.insert(node.father.name, count, node.name, text=node.expr)
            # if the node have children (not a parameter)
            if node.sons:
                # insert the next operator
                tree.insert(node.name, count, node.sons[0].name, text=node.sons[0].expr)
                # The brother's number
                c = 0
                # we will go through the children of the child (single child)
                # of the current node and call this function
                for son in node.sons[0].sons:
                    self.create_tree(tree, son, c)
                    c += 1
        # the node is the root
        else:
            # insert the expression of the root
            tree.insert("", "end", "root", text=node.expr)
            if node.sons:
                # insert the next operator
                tree.insert("root", 0, node.sons[0].name, text=node.sons[0].expr)
                # The brother's number
                c = 0
                # we will go through the children of the child (single child)
                # of the root and call this function
                for son in node.sons[0].sons:
                    self.create_tree(tree, son, c)
                    c += 1

    def check_2_dimensions(self):
        """
        This function checks whether it is possible to draw the expression in a graph with two axes
        """
        self.create_lists(self.expr)
        # We will check that the only function in the expression is power
        if self.func:
            for f in self.func:
                if "power" not in f:
                    return False
        # We will check that there is no more than one variable
        if len(self.variables) > 1:
            return False
        # We will check that the variable is not a matrix
        if self.ob.variables() and self.ob.variables()[0].shape != ():
            return False
        # We will check that the parameters are not of matrix type
        for parm in self.parameters:
            if '[' in parm:
                return False
        return True

    def check(self, exp):
        """
        The two lower functions are still unimplemented
        """
        if not is_float(str(exp)) and not is_matrix(str(exp)) and not str(exp) in self.variables \
                and not str(exp).replace('-', '') in self.variables:
            return True
        return False

    def check_func(self, exp, curr_op):
        if str(exp)[0] == '-':
            curr_op = '-' + curr_op
        new_exp = str(exp).replace(' + -', ' - ').replace('\n', ' ').replace(' ', '')
        new_op = str(curr_op).replace(' + -', ' - ').replace('\n', ' ').replace(' ', '')
        if new_exp.__eq__(new_op) or str(exp).replace(' + -', ' - ') in self.func:
            return True
        else:
            return False

    def curvature_sign(self, exp):
        """
        This function matches each cvxpy expression its sign and its curvature
        """
        # Stopping conditions: If we have finished going through the list we will return
        if self.index > len(self.priority_op) - 1 and self.index >= 2:
            # If the last operator is a function, you should first check its arguments and only then finish
            if self.check_func(exp, self.priority_op[self.index - 2]):
                self.index -= 2
            else:
                return
        if len(self.priority_op) >= 0 and self.index < len(self.priority_op):
            curr_op = self.priority_op[self.index]
            bool_op = False
            bool_pow = False
            param = ' '
            # If the expression is a variable or a parameter or a matrix there is nothing more to analyze,
            # if it is a function then we will check its arguments
            if is_float(str(exp)) or is_matrix(str(exp)) or str(exp) in self.variables \
                    or str(exp).replace('-', '') in self.variables or self.check_func(exp, curr_op):
                if self.check_func(exp, curr_op) and self.check(exp):
                    # If the function is a power, we need to see what the power number is
                    if "power" in str(exp) and str(curr_op).replace(' ', '')[0:5].__eq__("power"):
                        str_exp = str(exp)
                        index_first = str_exp.index('(')
                        index_sec = str_exp.rfind(')')
                        newExpr = str_exp[index_first + 1: index_sec]
                        param = re.split(r',(?![^()]*\))', newExpr)
                        bool_pow = True
                    # If the sign of the function is negative, then the argument is the function itself,
                    # so we need to check the arguments of the argument
                    if str(exp.expr)[0] == '-':
                        for arg in exp.args[0].args:
                            # If the argument is a variable or a parameter or a matrix there is nothing more to analyze
                            if not self.check(arg):
                                self.curvature_sign_list.append([str(arg), arg.curvature, arg.sign])
                                # if the function is a power
                                if bool_pow:
                                    if str(param[1][1]).__eq__('-'):
                                        s = 'NEGATIVE'
                                    else:
                                        s = 'POSITIVE'
                                    self.curvature_sign_list.append([str(param[1]), 'CONSTANT', s])
                            else:
                                self.index += 1
                                self.curvature_sign_list.append([str(arg), arg.curvature, arg.sign])
                                if bool_pow:
                                    if str(param[1][1]).__eq__('-'):
                                        s = 'NEGATIVE'
                                    else:
                                        s = 'POSITIVE'
                                    self.curvature_sign_list.append([str(param[1]), 'CONSTANT', s])
                                self.curvature_sign(arg)
                    # If the sign of the function is not negative
                    else:
                        for arg in exp.args:
                            # If the argument is a variable or a parameter or a matrix there is nothing more to analyze
                            if not self.check(arg):
                                self.curvature_sign_list.append([str(arg), arg.curvature, arg.sign])
                                # if the function is a power
                                if bool_pow:
                                    if str(param[1][1]).__eq__('-'):
                                        s = 'NEGATIVE'
                                    else:
                                        s = 'POSITIVE'
                                    self.curvature_sign_list.append([str(param[1]), 'CONSTANT', s])
                            else:
                                self.index += 1
                                self.curvature_sign_list.append([str(arg), arg.curvature, arg.sign])
                                if bool_pow:
                                    if str(param[1][1]).__eq__('-'):
                                        s = 'NEGATIVE'
                                    else:
                                        s = 'POSITIVE'
                                    self.curvature_sign_list.append([str(param[1]), 'CONSTANT', s])
                                self.curvature_sign(arg)
                    self.index += 1
            # If the expression is not a variable or a parameter or a matrix or a function
            else:
                if not exp.args:
                    return
                cp_expr1 = exp.args[0]
                bool_first = False
                cp_expr2 = exp.args[0]
                # if the operator is in priority1 = ['@', '*', '/'] this means that the expression is divided into two
                if curr_op in priority1:
                    cp_expr1 = exp.args[0]
                    cp_expr2 = exp.args[1]
                # if the operator is in priority2 = ['+', '-'] this means that the expression can be divided
                # into more than two
                else:
                    for term in exp.args:
                        # the first argument is cp_expr1 and the rest is cp_expr2
                        if not bool_first:
                            bool_first = True
                            continue
                        elif not bool_op:
                            bool_op = True
                            cp_expr2 = term
                        elif bool_op:
                            cp_expr2 += term
                new_cp1 = cp_expr1
                new_cp2 = cp_expr2
                # If the sign of the expression is negative multiply by minus 1 to get its true value
                if str(cp_expr1.expr)[0] == '-' and not self.left:
                    new_cp1 = cp_expr1 * (-1)
                if str(cp_expr2.expr)[0] == '-':
                    new_cp2 = cp_expr2 * (-1)
                self.left = False
                self.curvature_sign_list.append([str(cp_expr1.expr), new_cp1.curvature, new_cp1.sign])
                self.curvature_sign_list.append([str(cp_expr2.expr), new_cp2.curvature, new_cp2.sign])
                self.index += 1
                self.curvature_sign(cp_expr1)
                self.curvature_sign(cp_expr2)

    def curvature_sign_node(self, node: Node):
        """
        This function uses the list we created in the curvature_sign function
        and matches each node its appropriate sign
        """
        # If the value of the node is an expression
        if node.expr is not None and node.expr is not False and node.flag == 0:
            # We will go through the list and look for the value of the current node
            for arg in self.curvature_sign_list:
                node_exp = node.expr
                if str(arg[0])[0] == '-' and node_exp[0] != '-':
                    node_exp = '-' + node.expr
                node_exp = node_exp.replace(' + -', ' - ').replace('\n', ' ').replace(' ', '')
                arg_exp = str(arg[0]).replace(' + -', ' - ').replace('\n', ' ').replace(' ', '')
                # If we found the value then we will insert the corresponding values into the node
                if node_exp.__eq__(arg_exp):
                    node.curvature = arg[1]
                    if is_float(arg[0]):
                        if float(arg[0]) < 0:
                            node.sign = "NEGATIVE"
                        else:
                            node.sign = "POSITIVE"
                    else:
                        # To present things more clearly
                        if str(arg[2]).__eq__("NONNEGATIVE"):
                            arg[2] = "POSITIVE"
                        if str(arg[2]).__eq__("NONPOSITIVE"):
                            arg[2] = "NEGATIVE"
                        node.sign = arg[2]
                    break
        # We will go over the children of the node and do the same
        for child in node.sons:
            self.curvature_sign_node(child)

    def order_curvature_sign_list(self):
        for arg in self.curvature_sign_list:
            if arg[2] == "NONNEGATIVE":
                arg[2] = "POSITIVE"
            elif arg[2] == "NONPOSITIVE":
                arg[2] = "NEGATIVE"
            elif arg[2] != "NEGATIVE" and arg[2] != "POSITIVE":
                arg[2] = "UNKNOWN"
            if is_float(arg[0]):
                if float(arg[0]) < 0:
                    arg[2] = "NEGATIVE"
                else:
                    arg[2] = "POSITIVE"

    def plot_function(self, expr, xminr, xmaxr, num_points=1000):
        func = self.string_to_plot(self.expr)
        x_vals = np.linspace(xminr, xmaxr, num_points)
        y_vals = func(x_vals)
        plt.plot(x_vals, y_vals)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Graph of Function')
        plt.show()

    def string_to_plot(self, s):
        # Extract the variable name and expression from the string
        # Replace power(var, n) with var^n
        expr = re.sub(r'power\((\w+),\s*([\d\.]+)\)', r'\1**\2', s)

        # Replace '@' with '*'
        expr = expr.replace('@', '*')

        expr = expr.replace(self.variables[0], 'x')

        # Replace the variable name in the expression with 'x'

        # Replace '^' with '**'

        # Construct the lambda function and return the input for plot_function
        func = lambda x: eval(expr)
        return func

    def draw_graph(self, xmin=-10, xmax=10):
        if self.check_2_dimensions():
            self.plot_function(self.expr, xmin, xmax)
        else:
            False

    def print_expr(self):
        self.root.print_tree()
