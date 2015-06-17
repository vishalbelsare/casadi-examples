#!/usr/bin/python

# Operations Research, Uebungsblatt 2, Aufgabe 5

import optoy

x = optoy.var(5)

cost = optoy.minimize( \

    # objective function

    -(2*x[0] + x[1] + x[2] + 2*x[3] + 2*x[4]), \

    # constraints

    [x[0] + 2*x[2] + x[3] + 2*x[4] <= 4, \

    2*x[0] + 2*x[1] + x[2] + x[4] <= 6, \

    x[0] + 2*x[1] + 2*x[3] + x[4] <= 8, \

    x >= 0])


print x.sol
print - cost
