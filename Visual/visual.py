from tkinter.ttk import Treeview
import tkinter as tk
from tkinter import font, ttk
import matplotlib.pyplot as plt
import numpy as np

from cvxpy.problems.objective import Objective
import operator
from Visual.binary_tree import Node

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


class Visual:

    def __init__(self, obj: Objective):
        """
         >>> import cvxpy as cp
         >>> import cvxopt
         >>> from cvxpy import Minimize, Problem, Variable, quad_form
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
         >>> stri==v.root.expr
         True
         >>> h = cp.Variable(pos=True, name="h")
         >>> w = cp.Variable(pos=True, name="w")
         >>> d = cp.Variable(pos=True, name="d")
         >>> volume = h * w * d
         >>> objective=cp.Maximize(volume)
         >>> v = Visual(objective)
         >>> stri=str(objective.expr).replace("+ -", " - ")
         >>> stri==v.root.expr
         True
        """
        self.ob = obj
        # Minimize/Maximize
        self.name = obj.NAME
        # converts the expression to a string and replaces + - with '-' to make it clearer
        self.expr = str(obj.expr).replace("+ -", " - ")
        # creating 4 lists so that each one represents a different type of character
        self.parameters = []
        self.variables = []
        self.operators = []
        # function is a type of operator
        self.func = []
        # create the first node, it has no father and brothers,
        # its type is an expression and its value is the expression that the class received
        self.root = Node(None, self.expr, 0)
        # split the expression
        self.split_expr(self.root)




    def split_expr(self, exp: Node):
        """
         This function divides the expression recursively,
         each node of type expression has a single child which is the operator with the highest priority
         and each node of type operator has children which are the division of the previous expression
         according to the operator
         >>> import cvxpy as cp
         >>> import cvxopt
         >>> from cvxpy import Minimize, Problem, Variable, quad_form
         >>> from cvxpy.problems.objective import Objective
         >>> h = cp.Variable(pos=True, name="h")
         >>> w = cp.Variable(pos=True, name="w")
         >>> d = cp.Variable(pos=True, name="d")
         >>> volume = h * w * d
         >>> objective=cp.Maximize(volume)
         >>> n = Node(None,str(objective.expr).replace("+ -", " - "),0)
         >>> len(n.sons)==0
         True
         >>> v = Visual(objective)
         >>> n=v.root
         >>> len(n.sons) != 0
         True
         >>> n.sons[0].expr.__contains__('@')
         True
         >>> n.sons[0].sons[0].expr.__contains__('h')
         True
         >>> n = 3
         >>> P = cvxopt.matrix([13, 12, -2,12, 17, 6,-2, 6, 12], (n, n))
         >>> q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
         >>> r = 1
         >>> x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))
         >>> x = Variable(n)
         >>> y = Variable()
         >>> z = Variable(n)
         >>> objective = Minimize(0.5 * quad_form(x, P) - cp.sum_squares(x) + q.T @ x + r + y)
         >>> n = Node(None,str(objective.expr).replace("+ -", " - "),0)
         >>> len(n.sons)==0
         True
         >>> n=Visual(objective).root
         >>> len(n.sons) != 0
         True
         >>> n.sons[0].expr.__contains__('@')
         False
         >>> n.sons[0].expr.__contains__('-')
         True
         >>> n.sons[0].sons[0].expr.__contains__('0.5 @ QuadForm(var1, [[13. 12. -2.][12. 17.  6.][-2.  6. 12.]])')
         True

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

    """
    This function takes the expression and looks for the operator with the highest priority
    """

    def priority(self, exp):
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
                return o
            if o in priority1:
                # now we can know that the operator with the highest priority is not a function
                pr = 1
                ans = o
            elif pr == 0:
                ans = o
        return ans

    """
    This function creating the four lists based on the expression she get
    """

    def create_lists(self, exp):
        # Reset the lists
        self.parameters = []
        self.variables = []
        self.operators = []
        self.func = []
        isFunc = False
        isMatrix = False
        func_string = ""
        matrix_string = ""
        # we will go through all the characters in the string
        for s in exp.split():
            # --------variables---------
            if "var" in s:
                self.variables.append(s)
            # --------variables---------

            # --------function---------
            # The expression of the function is over
            if ')' in s:
                isFunc = False
                func_string += " " + s
                # We will put the expression of the function in the list of functions
                # and also in the list of operators because it is a type of operator
                self.func.append(func_string)
                self.operators.append(func_string)
                func_string = ""
                continue
            if isFunc:
                func_string += " " + s
                continue
            # The expression of the function is start
            if '(' in s:
                isFunc = True
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

    """
    The purpose of this function is to visually show the created tree using tkinter
    """

    def show(self):
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

    """
    This function recursively creates the tree using Treeview
    """

    def create_tree(self, tree: Treeview, node: Node, count):
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

    """
    This function checks whether it is possible to draw the expression in a graph with two axes
    """

    def check_2_dimensions(self):
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

    """
    The two lower functions are still unimplemented
    """

    def plot_function(expr, xmin, xmax, num_points=1000):
        x_vals = np.linspace(xmin, xmax, num_points)
        func = lambda x: eval(expr)
        y_vals = func(x_vals)
        plt.plot(x_vals, y_vals)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Graph of Function')
        plt.show()

    def draw_graph(self):
         if self.check_2_dimensions():
             self.plot_function(self.expr, -10, 10)


    def draw_constrain(self):
        pass
