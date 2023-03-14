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


## Visual:
Purpose of our project is adding visuals to the optimization problems that found in the CVXPY library.<br />
To see examples you can run the ``examples.py`` <br /> 
It will run you 3 phrases:

1. Minimize((x2 - y2) ** 2)

<img width="158" alt="two" src="https://user-images.githubusercontent.com/93201414/224012647-01a514f1-dbfc-4aad-97bb-25d76964750f.PNG">

2. Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)

<img width="392" alt="One1" src="https://user-images.githubusercontent.com/93201414/224955840-f8e2bebe-2035-4f0d-81d3-1b2b714bef01.png">

3. Maximize(3 * cp.sum(x2 - y2) + (x2 - y2) ** 2 + quad_form(z1, P))

<img width="436" alt="tree1" src="https://user-images.githubusercontent.com/93201414/224955914-73524744-96e6-49a5-9153-11c7d5eb7219.png">
