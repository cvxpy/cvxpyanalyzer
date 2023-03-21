from graphviz import Digraph

dot = Digraph()
dot.node('A', 'Node A')
dot.node('B', 'Node B')
dot.edge('A', 'B', "f")
dot.render('graph.gv', view=True)