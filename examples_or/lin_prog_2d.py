#!/usr/bin/python

# Operations Research, Uebungsblatt 2, Aufgabe 2

from casadi import *

x = SX.sym("x", 2)

f = -(x[0] + x[1])

g = vertcat([
    4*x[0] + x[1],
    4*x[1],
    2*x[0] + 3*x[1]
])

lbx = [0, 0]
ubg = [20, 10, 12]

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
