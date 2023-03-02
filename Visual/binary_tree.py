import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph


class Node:
    def __init__(self, node, expr: str, flag=0):
        self.father = node
        self.sons = []
        self.expr = expr
        self.flag = flag  # flag = 1 ->operator , flag = 0 ->expr

    def insert(self, op: str):
        new_op = op
        if op == '-':
            new_op = "+ -"
        node = Node(self, op, 1)
        self.sons.append(node)
        ans = self.expr.split(new_op, 1)
        for i in range(len(ans)):
            node.sons.append(Node(node, ans[i], 0))

    def insert_func(self, op: str):
        index_first = op.index('(')
        index_sec = op.index(')')
        newExpr = op[index_first + 1: index_sec]
        node = Node(self, op.split('(')[0], 1)
        self.sons.append(node)
        param = newExpr.split(',')
        for p in param:
            node.sons.append(Node(node, p, 0))

    def print_tree(self):
        if self.flag == 0:
            print("expression:", self.expr)
            for e in self.sons:
                e.print_tree()
                print("]")
        else:
            print("operator:", self.expr, "[")
            for e in self.sons:
                e.print_tree()
