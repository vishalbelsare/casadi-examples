#!/usr/bin/python

# Operations Research, Uebungsblatt 2, Aufgabe 2

import optoy

x = optoy.var(2)

cost = optoy.minimize( \

    # objective function

    -(x[0] + x[1]), \

    # constraints

    [4*x[0] + x[1] <= 20, \

    4*x[1] <= 10, \

    2*x[0] + 3*x[1] <= 12, \

    x >= 0])


print x.sol
print - cost
