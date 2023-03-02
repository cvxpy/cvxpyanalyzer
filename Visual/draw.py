import tkinter as tk

from future.moves.tkinter import ttk

# Create a window
window = tk.Tk()
window.title("My GUI")

# Create a Treeview widget
tree = ttk.Treeview(window)

# Define the tree structure
tree.insert("", "0", "parent", text="Parent")
tree.insert("parent", "0", "child1", text="Child 1")
tree.insert("parent", "1", "child2", text="Child 2")

# Pack the Treeview widget
tree.pack()

# Run the event loop
window.mainloop()
