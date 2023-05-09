A toolkit for analyzing CVXPY problems.

Install via ``pip install cvxpyanalyzer``.

Example usage:
```
from analyzer import tech_support

# Construct CVXPY problem.
...

# Analyze the problem.
tech_support(problem)
```


# Visual:
The Purpose of our project is to visualize the Problem expressions which can be found in CVXPY library. <br /> 
During the development process, we have created four different functions that allow to visualize the Problem expressions in a more accessible and clear way for library users. <br />
As you can see in the file:  ``examples.py`` <br />
You can see several examples of how to run expressions using the different functions we created.

## v.draw_graph(xmin, xmax):
A function that graphically displays all the solutions of a specific expression where the variable is represented as X and the equation as Y.
If a function is called without any arguments, the default value will be xmin=-10 xmax=10.

Here you can see the results:
As you can see for the phrase: `Minimize(-1 * (y2) ** 2 + 2 * y2)` <br />
with the constraints `[y2 >= 1]` <br />

```

    y2 = Variable()
    
    objective = Minimize(-1 * (y2) ** 2 + 2 * y2)
    constraints = [y2 >= 1]
    v = Visual(objective)
    print(v.expr)
    v.draw_graph()
```
by running `v.draw_graph()` you will get the following graph:<br />
![3](https://user-images.githubusercontent.com/93201414/229357160-6517dcca-fcb7-4257-b145-400c084bf853.png)

It displays all the solutions of the equation that we want to see when substituting variable values between -10 to 10.

## v.show_and_save():
We created this function to enable viewing the expression in a graph format with nodes, which will allow for visual and clear representation. <br />
For each expression you choose, the function's output is a PDF file named "file_name.pdf", which is very similar to the DCP Analyzer. https://dcp.stanford.edu/analyzer <br />

Here too it was important for us to present for all: Parameters , Variables <br />
Which `Sing` is of a type of `Positive` , `Negative`, `Unknown` and Which `Curvature` is of a type of `Constant`,`Affine`,`Convex`,`Concave`,`Unknown`. <br />

In the ``example.py`` file you can run several expressions on this function.

```
    x2 = Variable()
    y2 = Variable()
    objective1 = Minimize((x2 - y2) ** 2)
    v = Visual(objective1)
    v.show_and_save("file_name")
```

Minimize((x2 - y2) ** 2) <br />

You will get the following graph: <br />

<img width="300" alt="4" src="https://user-images.githubusercontent.com/93201414/229358362-0c92af7f-3ebc-4dd5-85d1-46b82e1aafcd.PNG">
<br />

**Please note that you can run only one example at a time and not all of them together. If you run all of them together, the output file will show only the graph of the last example that was executed** <br />


## v.root.print_tree():
This function prints the expression in the structure of a tree in the RUN window.

```
    x2 = Variable()
    y2 = Variable()
    
    objective1 = Minimize((x2 - y2) ** 2)
    
    # examples for print_tree:

    print("---objective 1 ---")
    v = Visual(objective1)
    print(v.curvature_sign_list)
    print("---objective 1 ---")

    v.print_expr()
```
For each expression, you can run the following function,<br />
This will produce a graph that will be displayed in the runtime window.

For example **for the first expression** 
1. Minimize((x2 - y2) ** 2) <br />

you will get : 
![image](https://user-images.githubusercontent.com/93201414/229359112-bc30b68a-bcd8-4739-b302-0d96932c2b8f.png)

## v.show():
The function uses the library tkinter <br />
The output shows the tree in a way that opens and closes according to the user <br />
Unlike show_and_save() the output is not saved but opens in a pop-up window <br />

```
    x2 = Variable()
    y2 = Variable()
    objective1 = Minimize((x2 - y2) ** 2)
    v = Visual(objective1)
    v.show()
```

<img width="158" alt="two" src="https://user-images.githubusercontent.com/93201414/237039372-d6d79c0c-d564-467d-ba21-b5290e7873ba.PNG">


