import re

import numpy as np
import matplotlib.pyplot as plt

def string_to_plot(s):
    # Extract the variable name and expression from the string


    # Replace power(var, n) with var^n
    expr = re.sub(r'power\((\w+),\s*([\d\.]+)\)', r'\1**\2', s)

    # Replace '@' with '*'
    expr = expr.replace('@', '*')

    expr = expr.replace('var3','x')


    # Replace the variable name in the expression with 'x'


    # Replace '^' with '**'

    # Construct the lambda function and return the input for plot_function
    func = lambda x: eval(expr)
    return (func, -10, 10)

# Get input for plot_function from string
s = "power(var3, 2.0) + 2.0 @ var3"
func, xmin, xmax = string_to_plot(s)

# Plot the function
x_vals = np.linspace(xmin, xmax, 1000)
y_vals = func(x_vals)
plt.plot(x_vals, y_vals)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Graph of Function')
plt.show()