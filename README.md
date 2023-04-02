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
During the development process, we have created three different functions that allow to visualize the Problem expressions in a more accessible and clear way for library users. <br />
As you can see in the file:  ``examples.py`` <br />
You can see several examples of how to run expressions using the different functions we created.

## v.draw_graph():
A function that graphically displays all the solutions of a specific expression where the variable is represented as X and the equation as Y.

Here you can see the results:
As you can see for the phrase: `Minimize(-1 * (y2) ** 2 + 2 * y2)` <br />
with the constraints `[y2 >= 1]` <br />

```
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1
    x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))

    x1 = Variable(n)
    y1 = Variable()
    x2 = Variable()
    y2 = Variable()
    z1 = Variable(n)

    objective = Minimize(-1 * (y2) ** 2 + 2 * y2)
    constraints = [y2 >= 1]
    v = Visual(objective)
    print(v.expr)
    v.draw_graph()
```
by running `v.draw_graph()` you will get the following graph:
![3](https://user-images.githubusercontent.com/93201414/229357160-6517dcca-fcb7-4257-b145-400c084bf853.png)

It displays all the solutions of the equation that we want to see when substituting variable values between -10 to 10.

## v.show_digraph():
We created this function to enable viewing the expression in a graph format with nodes, which will allow for visual and clear representation. <br />
For each expression you choose, the function's output is a PDF file named "tree.gv", which is very similar to the DCP Analyzer. https://dcp.stanford.edu/analyzer <br />

Here too it was important for us to present for all: Parameters , Variables <br />
Which `Sing` is of a type of `Positive` , `Negative`, `Unknown` and Which `Curvature` is of a type of `Constant`,`Affine`,`Convex`,`Concave`,`Unknown`. <br />

In the ``example.py`` file you can run several expressions on this function.

```
    n = 3
    P = cvxopt.matrix([13, 12, -2,
                       12, 17, 6,
                       -2, 6, 12], (n, n))
    q = cvxopt.matrix([-22, -14.5, 13], (n, 1))
    r = 1
    x_star = cvxopt.matrix([1, 1 / 2, -1], (n, 1))

    x1 = Variable(n)
    y1 = Variable()
    x2 = Variable()
    y2 = Variable()
    z1 = Variable(n)
    
    objective1 = Minimize((x2 - y2) ** 2)
    objective2 = Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)
    objective3 = Maximize(3 * cp.sum(x2 - y2) + (x2 - y2) ** 2 + quad_form(z1, P))

    # examples for show_digraph:

    v = Visual(objective1)
    v.show_digraph()

    v2 = Visual(objective2)
    v2.show_digraph()

    v3 = Visual(objective3)
    v3.show_digraph()
```
**for the first expression**
1. Minimize((x2 - y2) ** 2)

<img width="158" alt="two" src="https://user-images.githubusercontent.com/93201414/224012647-01a514f1-dbfc-4aad-97bb-25d76964750f.PNG">

2. Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)

<img width="392" alt="One1" src="https://user-images.githubusercontent.com/93201414/224955840-f8e2bebe-2035-4f0d-81d3-1b2b714bef01.png">

3. Maximize(3 * cp.sum(x2 - y2) + (x2 - y2) ** 2 + quad_form(z1, P))

<img width="436" alt="tree1" src="https://user-images.githubusercontent.com/93201414/224955914-73524744-96e6-49a5-9153-11c7d5eb7219.png">
