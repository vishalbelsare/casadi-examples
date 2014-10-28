#!/usr/bin/python

# ASDS, Kapitel 5

from casadi import *
from pylab import *
from numpy import linspace, squeeze

phi = SX.sym("phi", 1)
omega = SX.sym("omega", 1)
x = vertcat([phi, omega])

g = 9.81
l = 2
omega_0 = sqrt(g/l)

phidot = omega
omegadot = - omega_0**2 * sin(phi)
f = vertcat([phidot, omegadot])

phi_t0 = pi/4
omega_t0 = 0

t0 = 0
dt = 0.1
tend = 5 * pi

ode = SXFunction(daeIn(x=x), daeOut(ode=f))

integrator = Integrator("cvodes", ode)

tgrid = linspace(t0, tend, (tend-t0)/dt )

simulator = Simulator(integrator, tgrid)
simulator.init()

simulator.setInput([phi_t0, omega_t0], "x0")
simulator.evaluate()

for i in xrange(0, x.size1()):
    plot(tgrid, squeeze(simulator.getOutput("xf")[i,:]))
grid()
show()
