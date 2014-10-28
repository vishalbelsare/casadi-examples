#!/usr/bin/python

# Operations Research, Uebungsblatt 3, Aufgabe 3

from casadi import *

x = SX.sym("x", 3)

f = -(4*x[0] + 5*x[1] + 9*x[2])

g = vertcat([
    x[0] + x[1] - 3*x[2],
    -x[0] + 3*x[1] - x[2],
    3*x[0] - x[1] - x[2],
    3+x[0] - 5*x[1] + 3*x[2],
    -5*x[1] + 3*x[1] + 3*x[2],
    x[0] + x[1] + x[2]
])

lbx = [0, 0, 0]
lbg = [-inf, -inf, -inf, -inf, -inf, 1]
ubg = [1, 3, 3, 3, 3, inf]

lp = SXFunction(nlpIn(x=x), nlpOut(f=f, g=g))

solver = NlpSolver("ipopt", lp)
solver.setOption("tol", 1e-10)
solver.init()

solver.setInput(lbx, "lbx")
solver.setInput(lbg, "lbg")
solver.setInput(ubg, "ubg")

solver.evaluate()

print "\nOptimal solution:"
print solver.getOutput("x")
print -solver.getOutput("f")
