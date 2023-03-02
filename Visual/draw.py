import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

# Add nodes
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)

# Add edges with weights
G.add_edge(1, 2, weight=0.5)
G.add_edge(1, 3, weight=1.0)
G.add_edge(2, 4, weight=2.2)
G.add_edge(3, 4, weight=3.5)

# Draw the graph
pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()
