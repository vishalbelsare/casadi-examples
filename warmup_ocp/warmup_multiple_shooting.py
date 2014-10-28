#!/usr/bin/python

from casadi import *
from numpy import *
from pylab import *

OPTIM = 1

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
K = x + (1. / 6.) * (K1 + 2 * K2 + 2 * K3 + K4) * dt

rk4 = SXFunction([x, u], [K])
rk4.setOption("name", "rk4")
rk4.init()

# stage_cost = SXFunction([x,u],[x[0]**2 + x[1]**2 + u**2])
# stage_cost.init()

Nv = Nk + 2 * (Nk + 1)
V = MX.sym("V", Nv)

U = V[0 : Nk]
X0 = V[Nk : Nv : 2]
X1 = V[Nk + 1 : Nv : 2]

Vmin = -inf * ones(Nv)
Vmax = inf * ones(Nv)

Vmin[Nk] = Vmax[Nk] = 0.7
Vmin[Nk + 1] = Vmax[Nk + 1] = 0

Vinit = zeros(Nv)

g = []
gmin = []
gmax = []

# cost = 0


for k in xrange(Nk):

    Xk = vertcat((X0[k], X1[k]))
    Xkn = vertcat((X0[k + 1], X1[k + 1]))

    Xke = rk4([Xk, U[k]])[0]

    # cost += stage_cost([Xk,U[k]])[0]

    g.append(Xkn - Xke)
    gmin.append(zeros(Xk.size()))
    gmax.append(zeros(Xk.size()))


if OPTIM:

    f = mul(V.T, V)
    # f = cost

    g = vertcat(g)

    nlp = MXFunction(nlpIn(x = V), nlpOut(f = f, g = g))
    solver = NlpSolver("ipopt", nlp)
    solver.init()

    solver.setInput(Vmin, "lbx")
    solver.setInput(Vmax, "ubx")
    solver.setInput(Vinit, "x0")
    solver.setInput(concatenate(gmin), "lbg")
    solver.setInput(concatenate(gmax), "ubg")

    solver.evaluate()

    Vopt = solver.getOutput("x")

    plot(linspace(tstart, tend, Nk + 1), Vopt[Nk : Nv : 2],
         linspace(tstart, tend, Nk + 1), Vopt[Nk + 1 : Nv : 2],
         linspace(tstart, tend, Nk), Vopt[0 : Nk])

    show()
