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

1. Minimize(0.5 * quad_form(x1, P) - cp.sum_squares(x1) + q.T @ x1 + r + y1)

<img width="700" alt="One" src="https://user-images.githubusercontent.com/93201414/224012589-90977fc4-d339-4baa-b095-d03cc741d29f.PNG">

2. Minimize((x2 - y2) ** 2)

<img width="158" alt="two" src="https://user-images.githubusercontent.com/93201414/224012647-01a514f1-dbfc-4aad-97bb-25d76964750f.PNG">

3. Maximize(3 * cp.sum(x2 - y2) + (x2 - y2) ** 2 + quad_form(z1, P))

<img width="700" alt="tree" src="https://user-images.githubusercontent.com/93201414/224012685-aaa5f1cd-8596-46ab-ac53-afa325df818b.PNG">
