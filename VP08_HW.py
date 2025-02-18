from vpython import *
import numpy as np

prob = 0.005
N, L = 400, 7E-9/2.0
E = 1000000
q, m, size = 1.6E-19, 1E-6/6E23, 0.1E-9 # artificial charge particle
t, dt, vrms = 0, 1E-16, 10000.0
atoms, atoms_v = [], []
total_collisions = 0  # Track total number of collisions

# Initialization
scene = canvas(width=600, height=600, align='left', background=vector(0.2, 0.2, 0))
scenev = canvas(width=600, height=600, align='left', range=4E4, background=vector(0.2, 0.2, 0))
container = box(canvas=scene, length=2*L, height=2*L, width=2*L, opacity=0.2, color=color.yellow)

pos_array = -L + 2*L*np.random.rand(N, 3)
X, Y, Z = np.random.normal(0, vrms, N), np.random.normal(0, vrms, N), np.random.normal(0, vrms, N)
v_array = np.transpose([X, Y, Z])

def a_to_v(a):  # Array to vector
    return vector(a[0], a[1], a[2])

for i in range(N):
    atom = sphere(canvas=scene, pos=a_to_v(pos_array[i]), radius=size, color=a_to_v(np.random.rand(3, 1)))
    atoms.append(atom)
    atoms_v.append(sphere(canvas=scenev, pos=a_to_v(v_array[i]), radius=vrms/30, color=a_to_v(np.random.rand(3, 1))))

# The average velocity and two axes in velocity space
vd_ball = sphere(canvas=scenev, pos=vec(0, 0, 0), radius=vrms/15, color=color.red)
x_axis = curve(canvas=scenev, pos=[vector(-2*vrms, 0, 0), vector(2*vrms, 0, 0)], radius=vrms/100)
y_axis = curve(canvas=scenev, pos=[vector(0, -2*vrms, 0), vector(0, 2*vrms, 0)], radius=vrms/100)
vv = vector(0, 0, 0)  # For calculating the average velocity

while True:
    t += dt
    rate(10000)
    v_array[:, 0] += q*E/m*dt  # Apply acceleration due to E-field
    pos_array += v_array * dt  # Update positions

    # Periodic boundary conditions
    outside = abs(pos_array) >= L
    pos_array[outside] = -pos_array[outside]
    
    # Collision handling
    collision_mask = np.random.rand(N) < prob  # Determine which particles collide
    total_collisions += np.sum(collision_mask)  # Count total collisions
    num_collisions = np.sum(collision_mask)
    
    if num_collisions > 0:
        new_velocities = np.random.normal(0, vrms, (num_collisions, 3))  # Randomize velocities
        v_array[collision_mask] = new_velocities  # Assign new velocities
    
    # Compute drift velocity
    vv += a_to_v(np.sum(v_array, axis=0) / N)
    
    if int(t/dt) % 2000 == 0:
        tau = (t * N) / total_collisions if total_collisions > 0 else 0  # Avoid division by zero
        vd_simulated = vv / (t / dt)
        vd_theoretical = q * E * tau / m
        print(f"tau: {tau:.3e}, vd_simulated: {mag(vd_simulated):.3e}, vd_theoretical: {vd_theoretical:.3e}")
    
    vd_ball.pos = vv / (t / dt)
    
    for i in range(N):
        atoms_v[i].pos, atoms[i].pos = a_to_v(v_array[i]), a_to_v(pos_array[i])

