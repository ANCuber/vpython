from vpython import *
import numpy as np

# Parameters
g = 9.81              # gravitational acceleration (m/s^2)
L = 1.0               # length of pendulum (m)
b = 0.05              # air resistance coefficient
mass = 0.1            # mass of the bob (kg)
theta0 = np.radians(10) # initial angle of displacement (10 degrees)
escapement_force = 0.2 # increased force added by escapement mechanism
period = 2 * pi * sqrt(L / g) # theoretical period of the pendulum

# Pendulum and Escapement Initial Setup
pendulum = sphere(pos=vector(L * sin(theta0), -L * cos(theta0), 0), radius=0.05, color=color.blue)
rod = cylinder(pos=vector(0, 0, 0), axis=pendulum.pos, radius=0.01)

# Motion variables
theta = theta0
omega = 0             # initial angular velocity
dt = 0.01             # time step

# Graph setup
graph1 = graph(title="Pendulum Height vs Period", xtitle="Periods", ytitle="Height (m)")
height_plot = gcurve(color=color.cyan)

t = 0                 # Initialize time
period_count = 0      # Track number of periods

# Simulation loop
while period_count < 10:  # simulate for 10 periods
    rate(100)           # control simulation speed

    # Calculate forces
    gravitational_force = -mass * g * sin(theta)
    drag_force = -b * omega
    total_torque = L * (gravitational_force + drag_force)

    # Escapement mechanism: add energy near the equilibrium position
    if abs(theta) < 0.02 and omega < 0:  # conditions to mimic escapement near equilibrium
        total_torque += escapement_force * L

    # Update angular acceleration, velocity, and angle
    alpha = total_torque / (mass * L**2)
    omega += alpha * dt
    theta += omega * dt

    # Update positions
    pendulum.pos = vector(L * sin(theta), -L * cos(theta), 0)
    rod.axis = pendulum.pos

    # Record and plot the height (y-coordinate of the pendulum bob)
    if t >= period * period_count:  # plot at each full period interval
        height_plot.plot(period_count, pendulum.pos.y)
        period_count += 1

    # Update time
    t += dt

