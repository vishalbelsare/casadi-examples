Warm up OCP
===========

A simple example for solving optimal control problems with CasADi.

Settings
--------

**ODE with two states x1 and x2, one control u:**

x1dot = -x2

x2dot = -sin(x1 + u) - 0.1*x2^2


**Initial values:**

x10 = 0.7

x20 = 0

tstart = 0

tend = 10

**Control discretization:**

100 equidistant intervals

**Constraints:**

no constraints

**Objective function:**

integral of x1^2 + x2^2 + u^2


Tasks
-----

**1.)** Write a simulator in CasADi with an RK4-step per control interval, giving out the values of x1 and x2 for every time step. The aim is to get an function of the control trajectories w. r. t. the state strajectories, i. e. from 100 inputs to 200 output. The control trajectory will be called U.


**2.)** Evaluate the objective function at every discrete step and add the terms to get the objective function f(U).

**3.)** Call ipopt to minimize f(U) with initial value 1 for all elements of U.

**4.)** Plot the solution trajectories for controls and states.