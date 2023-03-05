"""
>>> A_wall = 100
>>> A_flr = 10
>>> alpha = 0.5
>>> beta = 2
>>> gamma = 0.5
>>> delta = 2

>>> h = cp.Variable(pos=True, name="h")
>>> w = cp.Variable(pos=True, name="w")
>>> d = cp.Variable(pos=True, name="d")

>>> volume = h * w * d
>>> wall_area = 2 * (h * w + h * d)
>>> flr_area = w * d
>>> hw_ratio = h/w
>>> dw_ratio = d/w
>>> constraints = [wall_area <= A_wall,flr_area <= A_flr,hw_ratio >= alpha,hw_ratio <= beta,w_ratio >= gamma,dw_ratio <= delta]
>>> objective=cp.Maximize(volume), constraints)
>>> v = Visual(objective)
>>> stri=str(objective.expr).replace("+ -", " - ")
>>>print(stri)
True
>>> stri==v.root.expr
True
"""