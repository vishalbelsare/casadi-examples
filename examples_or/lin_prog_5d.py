#!/usr/bin/python

# Operations Research, Uebungsblatt 2, Aufgabe 5

from casadi import *

x = SX.sym("x", 5)

f = -(2*x[0] + x[1] + x[2] + 2*x[3] + 2*x[4])

g = vertcat([
    x[0] + 2*x[2] + x[3] + 2*x[4],
    2*x[0] + 2*x[1] + x[2] + x[4],
    x[0] + 2*x[1] + 2*x[3] + x[4]
])

lbx = [0, 0, 0, 0, 0]
ubg = [4, 6, 8]

lp = SXFunction(nlpIn(x=x), nlpOut(f=f, g=g))

solver = NlpSolver("ipopt", lp)
solver.setOption("tol", 1e-10)
solver.init()

solver.setInput(lbx, "lbx")
solver.setInput(ubg, "ubg")

solver.evaluate()

print "\nOptimal solution:"
print solver.getOutput("x")
print -solver.getOutput("f")
