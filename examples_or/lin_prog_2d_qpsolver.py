#!/usr/bin/python

# Operations Research, Uebungsblatt 2, Aufgabe 2

from casadi import *
from numpy import zeros

c = DMatrix([-1, -1])

A = DMatrix([
    [4, 1],
    [0, 4],
    [2, 3]
    ])

lbx = [0, 0]
uba = [20, 10, 12]

# no LP-solvers installed, using QP-solver with empty H instead

H = zeros((2, 2))
H = DMatrix(H)

lp = qpStruct(h=H.sparsity(),a=A.sparsity())

solver = QpSolver("nlp",lp)
solver.setOption("nlp_solver","ipopt")

solver.init()

solver.setInput(H,"h")
solver.setInput(c,"g")
solver.setInput(A,"a")

solver.setInput(lbx,"lbx")
solver.setInput(uba,"uba")

solver.evaluate()

print "\nOptimal solution:"
print solver.getOutput("x")
print -solver.getOutput("cost")
