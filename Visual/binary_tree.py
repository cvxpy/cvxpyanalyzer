class Edge:
    def __init__(self, obj: str, father):
        self.expr = obj
        self.father = father
        self.son = None

    def print_tree(self):
        if self.son:
            self.son.print_tree()


class Node:
    def __init__(self, edge: Edge, op: str):
        self.father = edge
        self.right = None
        self.left = None
        self.value = op

    def insert(self):
        op = self.value
        if self.value == '-':
            op = "+ -"
        ans = self.father.expr.split(op, 1)
        self.right = Edge(ans[1], self)
        self.left = Edge(ans[0], self)
        self.father.son = self

    def print_tree(self):
        print(self.father.expr)
        print(self.value)
        if self.left.son:
            self.left.son.print_tree()
        else:
            print(self.left.expr)

        if self.right.son:
            self.right.son.print_tree()
        else:
            print(self.right.expr)


class BinaryTree:
    def __init__(self, root):
        self.root = root
        self.split_expr(root)

    def split_expr(self, exp):
        if exp in self.variables or exp in self.parameters:
            return
        else:
            op = self.priority()
            node = Node(exp, op)
            node.insert()
            self.split_expr(node.right)
            self.split_expr(node.left)
