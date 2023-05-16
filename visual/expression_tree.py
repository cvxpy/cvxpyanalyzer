import re


class Node:
    # Each node has a unique name because an operator can appear more than once
    uniqNameForTree = 0
    count_curvature = 0
    count_sign = 0

    def __init__(self, node, expr: str, flag=0):
        # The father of this node - for every operator the father is of type expression
        # and for every expression the father is of type operator
        self.father = node
        # A list of the children of the node -
        # each expression has a single child (the operator with the highest priority)
        # and each operator has several children
        self.sons = []
        # the value of the node
        self.expr = expr
        # flag = 1 ->operator , flag = 0 ->expression
        self.flag = flag
        self.name = self.uniqNameForTree
        Node.uniqNameForTree += 1
        self.curvature = None
        self.sign = None

        self.c_curvature = self.count_curvature
        Node.count_curvature += 1

        self.c_sign = self.count_sign
        Node.count_sign += 1

    # ---for test---
    def checkin_sons(self, expr: str):
        for s in self.sons:
            expression = expr.split(' ')
            bool = True
            for e in expression:
                if not s.expr.__contains__(e):
                    bool = False
                    break
            if bool:
                return True
        return False

    def node_son(self, expr: str):
        if not self.sons:
            return None
        for s in self.sons:
            if s.expr == expr:
                return s
        return None

    # ---for test---

    def insert(self, op: str):
        """
        This function get an operator and uses it to split the expression and create new nodes

        """
        # create a new node of type operator
        if op not in self.expr:
            return
        node = Node(self, op, 1)
        self.sons.append(node)
        # We will look for the first position of the operator that is not inside parentheses and inside a matrix
        count = -1
        check1 = False
        check2 = False
        for i in self.expr:
            count += 1
            if i == '[':
                check2 = True
                continue
            if i == ']':
                check2 = False
                continue
            if i == '(':
                check1 = True
                continue
            if i == ')':
                check1 = False
                continue
            if i == op and not check1 and not check2:
                break

        ans = [self.expr[:count], self.expr[count + 1:]]
        for i in range(len(ans)):
            node.sons.append(Node(node, ans[i], 0))

    def insert_func(self, op: str):
        """
          This function inserts a function type operator and
          this means that the expression should be split according to the number of parameters the function accepts
        """
        index_first = op.index('(')
        index_sec = op.rfind(')')
        newExpr = op[index_first + 1: index_sec]
        # the operator is the name of the function
        node = Node(self, op.split('(')[0], 1)
        self.sons.append(node)
        param = re.split(r',(?![^()]*\))', newExpr)
        # The children of a function type operator are the parameters it accepts
        for p in param:
            node.sons.append(Node(node, p, 0))

    def print_tree(self, spaces=0, counter=0):
        """
        This function prints the tree recursively
        """
        for i in range(spaces):
            print("   ", end="")
        if self.flag == 0:
            # Print the child's number
            print(counter, ".expression:", self.expr)
            s = spaces + 1
            c = 1
            for e in self.sons:
                e.print_tree(s, c)
                c += 1
                for i in range(spaces + 1):
                    print("   ", end="")
                print("]")
        else:
            print("operator:", self.expr)
            for i in range(spaces):
                print("   ", end="")
            print("[")
            s = spaces + 1
            c = 1
            for e in self.sons:
                e.print_tree(s, c)
                c += 1
        s += 1
