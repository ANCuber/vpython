from vpython import *
import numpy as np
import random

# Constants
g = 9.8  # gravitational acceleration (m/s^2)
k = 0.002  # air drag coefficient (arbitrary unit)
dt = 0.01  # time step (s)

# Parameters of pendulums
m1, m2, m3 = 1.0, 1.0, 1.0  # masses (kg)
L1, L2, L3 = 2*random.random(), 2*random.random(), 2*random.random() # lengths (m)
radii = 0.05  # radius of pendulum bobs

# Initial angles (in radians)
theta1, theta2, theta3 = np.pi / 4, np.pi / 6, np.pi / 3
omega1, omega2, omega3 = 11, -7, 3 # angular velocities

# Create the scene
scene = canvas(title="Triple Pendulum Simulation with Energy Tracking", width=800, height=600, align = 'left')
ceiling = box(pos=vector(0, 0, 0), size=vector(0.1, 0.1, 0.1), color=color.gray(0.5))

# Pendulum components
bob1 = sphere(radius=radii, color=color.red)
bob2 = sphere(radius=radii, color=color.green)
bob3 = sphere(radius=radii, color=color.blue)
rod1 = cylinder(radius=0.02, color=color.white)
rod2 = cylinder(radius=0.02, color=color.white)
rod3 = cylinder(radius=0.02, color=color.white)

# Trails for bobs
trail1 = curve(color=color.red, radius=0.005)
trail2 = curve(color=color.green, radius=0.005)
trail3 = curve(color=color.blue, radius=0.005)

# Graph for energies
energy_graph = graph(title="Energies vs. Time", width=500, height=300, align = 'right')
ke_curve = gcurve(color=color.cyan, label="Kinetic Energy")
pe_curve = gcurve(color=color.magenta, label="Potential Energy")
me_curve = gcurve(color=color.yellow, label="Total Mechanical Energy")

# Initial positions of bobs
def get_positions(theta1, theta2, theta3):
    x1, y1 = L1 * sin(theta1), -L1 * cos(theta1)
    x2, y2 = x1 + L2 * sin(theta2), y1 - L2 * cos(theta2)
    x3, y3 = x2 + L3 * sin(theta3), y2 - L3 * cos(theta3)
    return vector(x1, y1, 0), vector(x2, y2, 0), vector(x3, y3, 0)

# Update positions
def update_positions():
    pos1, pos2, pos3 = get_positions(theta1, theta2, theta3)
    bob1.pos = pos1
    bob2.pos = pos2
    bob3.pos = pos3
    rod1.pos, rod1.axis = ceiling.pos, pos1 - ceiling.pos
    rod2.pos, rod2.axis = bob1.pos, pos2 - bob1.pos
    rod3.pos, rod3.axis = bob2.pos, pos3 - bob2.pos
    return pos1, pos2, pos3

update_positions()

# Energy calculations
def calculate_energies(pos1, pos2, pos3):
    # Heights relative to the ceiling
    h1 = -pos1.y
    h2 = -pos2.y
    h3 = -pos3.y
    
    # Speeds of the bobs
    v1 = mag(L1 * omega1 * vector(-cos(theta1), -sin(theta1), 0))
    v2 = mag(L2 * omega2 * vector(-cos(theta2), -sin(theta2), 0))
    v3 = mag(L3 * omega3 * vector(-cos(theta3), -sin(theta3), 0))
    
    # Kinetic energy
    ke1 = 0.5 * m1 * v1**2
    ke2 = 0.5 * m2 * v2**2
    ke3 = 0.5 * m3 * v3**2
    kinetic_energy = ke1 + ke2 + ke3
    
    # Potential energy
    pe1 = m1 * g * h1
    pe2 = m2 * g * h2
    pe3 = m3 * g * h3
    potential_energy = pe1 + pe2 + pe3
    
    # Total mechanical energy
    total_energy = kinetic_energy + potential_energy
    
    return kinetic_energy, potential_energy, total_energy

# Simulate dynamics
time = 0
while True:
    rate(100)
    
    # Forces and accelerations
    alpha1 = (-g * (2 * m1 + m2) * sin(theta1) - m2 * g * sin(theta1 - 2 * theta2) - 
              2 * sin(theta1 - theta2) * m2 * (omega2 ** 2 * L2 + omega1 ** 2 * L1 * cos(theta1 - theta2))) / (
                 L1 * (2 * m1 + m2 - m2 * cos(2 * theta1 - 2 * theta2)))
    
    alpha2 = (2 * sin(theta1 - theta2) * (omega1 ** 2 * L1 * (m1 + m2) + g * (m1 + m2) * cos(theta1) + 
                                          omega2 ** 2 * L2 * m2 * cos(theta1 - theta2))) / (
                 L2 * (2 * m1 + m2 - m2 * cos(2 * theta1 - 2 * theta2)))
    
    alpha3 = (-g * sin(theta3) - k * omega3 / m3) / L3
    
    # Update angular velocities and positions
    omega1 += alpha1 * dt
    omega2 += alpha2 * dt
    omega3 += alpha3 * dt
    
    omega1 *= (1 - k * dt)
    omega2 *= (1 - k * dt)
    omega3 *= (1 - k * dt)
    
    theta1 += omega1 * dt
    theta2 += omega2 * dt
    theta3 += omega3 * dt
    
    # Update graphics
    pos1, pos2, pos3 = update_positions()
    
    # Append to trails
    trail1.append(pos1)
    trail2.append(pos2)
    trail3.append(pos3)
    
    # Calculate and plot energies
    kinetic_energy, potential_energy, total_energy = calculate_energies(pos1, pos2, pos3)
    ke_curve.plot(time, kinetic_energy)
    pe_curve.plot(time, potential_energy)
    me_curve.plot(time, total_energy)
    
    time += dt

