
import xpress as xp # use the Xpress python API

# define variables
x1 = xp.var(name = "x1", lb = 0, vartype = xp.continuous)
x2 = xp.var(name = "x2", lb = 0, vartype = xp.integer)
x3 = xp.var(name = "x3", lb = 0, vartype = xp.integer)
x4 = xp.var(name = "x4", lb = 0, vartype = xp.integer)
s1 = xp.var(name = "s1", lb = 0, vartype = xp.continuous)
s2 = xp.var(name = "s2", lb = 0, vartype = xp.continuous)
s3 = xp.var(name = "s3", lb = 0, vartype = xp.continuous)
s4 = xp.var(name = "s4", lb = 0, vartype = xp.continuous)

p = xp.problem() # instantiate the problem

p.addVariable(x1, x2, x3, x4, s1, s2, s3, s4) # add variables to the problem

obj = 1*x1 # objective function
# constraints
cons1 = 1*x1 -0.85*x2 - 0.7*x3 - 0.5*x4 - 1*s1 == 1050
cons2 = 0.08*x2 + 0.075*x3 + 1.024*s1 - 1*s2 == 1050
cons3 = 0.08*x2 + 1.075*x3 + 1.024*s2 - 1*s3 == 1050
cons4 = 1.08*x2 + 1.024*s3 - 1*s4 == 1050
cons5 = 1*x4 + 1.024*s4 == 1050
cons6 = -0.067*x2 + 0.005*x3 + 0.005*x4 + 0.005*s1 >= 0
cons7 = 0.005*x2 - 0.06*x3 + 0.005*x4 + 0.005*s1 >= 0
cons8 = 0.005*x2 + 0.005*x3 - 0.052*x4 + 0.005*s1 >= 0

p.setObjective(obj, sense = xp.minimize) # se the problem to minimize the objective function
p.addConstraint(cons1, cons2, cons3, cons4, cons5, cons6, cons7, cons8) # add contraints to the problem

p.solve() # solve the problem

print("solution:", p.getSolution()) # print out the result
