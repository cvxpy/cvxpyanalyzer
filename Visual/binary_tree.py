import networkx as nx
import matplotlib.pyplot as plt
from networkx import Graph


class Node:
    uniqName = 0

    def __init__(self, node, expr: str, number: int, flag=0):
        self.father = node
        self.sons = []
        self.expr = expr
        self.flag = flag  # flag = 1 ->operator , flag = 0 ->expr
        self.name = self.uniqName
        Node.uniqName += 1
        self.number = number
    def CheckinSons(self,expr: str):
        for s in self.sons:
            if s.expr.__contains__(expr):
                return True
        return False
    def NodeSon(self,expr: str):
        if not self.sons:
            return None
        for s in self.sons:
            if s.expr == expr:
                return s
        return None

    def insert(self, op: str):
        new_op = op
        if op == '+ -':
            new_op = "-"
        node = Node(self, new_op, 0, 1)
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
            if i == new_op and check1 == False and check2 == False:
                break

        self.sons.append(node)
        ans= [self.expr[:count], self.expr[count + 1:]]
        # ans = self.expr.split(op, count)
        j = 0
        for i in range(len(ans)):
            # print("ans[i]",ans[i])
            node.sons.append(Node(node, ans[i], j, 0))
            j += 1

    def insert_func(self, op: str):
        # print("op:", op)
        index_first = op.index('(')
        index_sec = op.index(')')
        newExpr = op[index_first + 1: index_sec]
        node = Node(self, op.split('(')[0], 0, 1)
        self.sons.append(node)
        param = newExpr.split(',')
        j = 0
        for p in param:
            node.sons.append(Node(node, p, j, 0))
            j += 1

    def print_tree(self):
        if self.flag == 0:
            # print("expression:", self.expr)
            for e in self.sons:
                e.print_tree()
                print("]")
        else:
            # print("operator:", self.expr, "[")
            for e in self.sons:
                e.print_tree()
