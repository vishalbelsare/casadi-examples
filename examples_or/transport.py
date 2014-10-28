#!/usr/bin/python

# Operations Research, Uebungsblatt 5, Aufgabe 1

from casadi import *
from numpy import ones, zeros

# Problemdefinition (Kosten"matrix", Angebote, Bedarfe)

c = [630, 150, 320, 310, 710, 380, 600, 400, 340, 250, 170, 420]
a = [75, 125, 100]
b = [80, 65, 70, 85]

# Transport"matrix"

x = SX.sym("x", len(c))

# Zielfunktion

f = mul(x.T,c)

# Nebenbedingungen erstellen

g =[]

# Nebenbedingungen a

for i in xrange(len(a)):
    g = vertcat([
            g,
            mul(x[i*len(b):(i+1)*len(b)].T, ones(len(b)))
        ])

# Nebenbedingungen b

for i in xrange(len(b)):

    index = []
    count = i
    while len(index) < len(a):
        index = index + [count]
        count += len(b)

    g = vertcat([
            g,
            mul(x[index].T, ones(len(a)))
        ])

# Constraints festlegen, Problem loesen

lbx = zeros(len(c))
lbg = a + b
ubg = lbg

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
print solver.getOutput("f")
print solver.getOutput("g")