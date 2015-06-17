#!/usr/bin/python

# Operations Research, Uebungsblatt 3, Aufgabe 3

import optoy

x = optoy.var(3)

cost = optoy.minimize( \

    # objective function

    -(4*x[0] + 5*x[1] + 9*x[2]), \

    # constraints

    [x[0] + x[1] - 3 * x[2] <= 1, \

    -x[0] + 3*x[1] - x[2] <= 3, \

    3 * x[0] - x[1] - x[2] <= 3, \

    3 + x[0] - 5 * x[1] + 3 * x[2] <= 3, \

    -5*x[1] + 3*x[1] + 3*x[2] <= 3, \

    x[0] + x[1] + x[2] >= 1, \

    x >= 0])


print x.sol
print - cost
