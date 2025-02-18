import numpy as np

# Constants
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)
R = 0.12  # Radius of large loop (m)
r = 0.06  # Radius of small loop (m)
Height = 0.10  # Separation between loops (m)
num_points = 100000  # Discretization of loops

# Generate points along the large loop
theta = np.linspace(0, 2*np.pi, num_points, endpoint=False)
large_loop_x = R * np.cos(theta)
large_loop_y = R * np.sin(theta)
large_loop_z = np.zeros(num_points)

def magnetic_field_Bz(x, y, z, I, loop_x, loop_y, loop_z):
    """
    Compute the z-component of the magnetic field at (x, y, z) due to a current loop using Biot-Savart Law.
    """
    Bz_total = 0
    dtheta = 2 * np.pi / num_points
    
    for i in range(num_points):
        # Current element dL
        dx = -loop_y[i] * dtheta  # -R sin(theta) dtheta
        dy = loop_x[i] * dtheta  # R cos(theta) dtheta
        dz = 0
        
        # Position vector from source to field point
        rx = x - loop_x[i]
        ry = y - loop_y[i]
        rz = z - loop_z[i]
        r = np.sqrt(rx**2 + ry**2 + rz**2)
        
        if r == 0:
            continue  # Avoid singularity
        
        # Biot-Savart Law
        dBz = mu_0 * I / (4 * np.pi) * (dx * ry - dy * rx) / (r**3)
        Bz_total += dBz
    
    return Bz_total

# Compute mutual inductance M_21 (flux through small loop due to current in large loop)
I_large = 1  # Assume unit current in the large loop
flux_21 = 0

theta_small = np.linspace(0, 2*np.pi, num_points, endpoint=False)
small_loop_x = r * np.cos(theta_small)
small_loop_y = r * np.sin(theta_small)
small_loop_z = np.full(num_points, Height)

dA = np.pi * r**2 / num_points  # Area element of small loop

for i in range(num_points):
    Bz = magnetic_field_Bz(small_loop_x[i], small_loop_y[i], small_loop_z[i], I_large, large_loop_x, large_loop_y, large_loop_z)
    flux_21 += Bz * dA
    
M_21 = flux_21 / I_large

# Compute mutual inductance M_12 (flux through large loop due to current in small loop)
I_small = 1  # Assume unit current in the small loop
flux_12 = 0

dA = np.pi * R**2 / num_points  # Area element of large loop

for i in range(num_points):
    Bz = magnetic_field_Bz(large_loop_x[i], large_loop_y[i], large_loop_z[i], I_small, small_loop_x, small_loop_y, small_loop_z)
    flux_12 += Bz * dA
    
M_12 = flux_12 / I_small

print(f"Mutual Inductance M_21: {M_21:.6e} H")
print(f"Mutual Inductance M_12: {M_12:.6e} H")

