#!/usr/bin/python

from casadi import *
from numpy import *
from pylab import *

OPTIM = 1
MAXITER = 3000

x = SX.sym("x", 2)
u = SX.sym("u", 1)
xdot = SX.sym("xdot", 2)

xdot[0] = -x[1]
xdot[1] = -sin(x[0] + u) - 0.1 * x[1]**2

ode = SXFunction([x, u], [xdot])
ode.setOption("name", "ode")
ode.init()

tstart = 0.
tend = 10.
Nk = 100

dt = (tend - tstart) / Nk

K1 = ode([x, u])[0]
K2 = ode([x + 0.5 * K1 * dt, u])[0]
K3 = ode([x + 0.5 * K2 * dt, u])[0]
K4 = ode([x + K3 * dt, u])[0]
K = (1. / 6.) * (K1 + 2 * K2 + 2 * K3 + K4) * dt

rk4 = SXFunction([x, u], [K])
rk4.setOption("name", "rk4")
rk4.init()

X = SX.sym("X", 2, Nk + 1)
U = SX.sym("U", Nk)

X0 = [0.7, 0]
U0 = ones(Nk)

X[:, 0] = X0

for k in xrange(0, Nk):

    X[:, k + 1] = X[:, k] + rk4([X[:, k], U[k]])[0]


xtraj = SXFunction([U], [X])
xtraj.setOption("name", "xtraj")
xtraj.init()


if OPTIM:

    cost = sum(X**2) + sum(U**2)

    f = SXFunction(nlpIn(x=U), nlpOut(f=cost))

    solver = NlpSolver("ipopt", f)
    solver.setOption("max_iter", MAXITER)
    solver.init()

    solver.setInput(U0, "x0")
    solver.evaluate()

    Uopt = solver.getOutput()


else:

    Uopt = U0


xtraj.setInput(Uopt)
xtraj.evaluate()

xout = xtraj.getOutput()

plot(linspace(tstart, tend, Nk+1), squeeze(xout[0, :]),
     linspace(tstart, tend, Nk+1), squeeze(xout[1, :]),
     linspace(tstart, tend, Nk), Uopt)

show()    
