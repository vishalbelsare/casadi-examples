#!/usr/bin/python

# ASDS, Kapitel 6

from casadi import *
from pylab import *
from numpy import linspace, squeeze

phi = SX.sym("phi", 1)
omega_phi = SX.sym("omega_phi", 1)
psi = SX.sym("psi", 1)
omega_psi = SX.sym("omega_psi", 1)
x = vertcat([phi, omega_phi, psi, omega_psi])

c = 39.24
a = 0.5
m = 1
l = 1
omegasqrd_0 = (c * a**2) / (m * l**2)

phidot = omega_phi
omegadot_phi = omegasqrd_0 * \
    (-sin(phi) - sin(phi)*cos(phi) + cos(phi)*sin(psi))
psidot = omega_psi
omegadot_psi = omegasqrd_0 * \
    (-sin(psi) - sin(psi)*cos(psi) + cos(psi)*sin(phi))
f = vertcat([phidot, omegadot_phi, psidot, omegadot_psi])

phi_t0 = pi/10
omega_phi_t0 = 0
psi_t0 = 0
omega_psi_t0 = 0
x0 = vertcat([phi_t0, omega_phi_t0, psi_t0, omega_psi_t0])

t0 = 0
dt = 0.1
tend = 5 * pi

ode = SXFunction(daeIn(x=x), daeOut(ode=f))

integrator = Integrator("cvodes", ode)

tgrid = linspace(t0, tend, (tend-t0)/dt )

simulator = Simulator(integrator, tgrid)
simulator.init()

simulator.setInput(x0, "x0")
simulator.evaluate()

for i in xrange(0, x.size1()):
    plot(tgrid, squeeze(simulator.getOutput("xf")[i,:]))
grid()
show()
