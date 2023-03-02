import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph


class Edge:
    def __init__(self, obj: str, father, flag=0):
        self.expr = obj
        self.father = father
        self.son = None
        self.flag = flag

    def print_tree(self):
        if self.son:
            self.son.print_tree()


class Node:
    def __init__(self, edge: Edge, op: str):
        self.father = edge
        self.sons = []
        self.value = op

    def insert(self):
        op = self.value
        if self.value == '-':
            op = "+ -"
        ans = self.father.expr.split(op, 1)
        for i in range(len(ans)):
            self.sons.append(Edge(ans[i], self))
        self.father.son = self

    def print_tree(self):
        print("expression:", self.father.expr)
        print("operator:", self.value, "[")
        for e in self.sons:
            if e.son:
                e.son.print_tree()
            else:
                print(e.expr)
        print("]")



