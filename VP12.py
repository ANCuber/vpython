from vpython import *
from numpy import *

N = 100
R, lamda = 1.0, 500E-9
d = 100E-6

dx, dy = d / N, d / N

scene1 = canvas(title='Real Image', align='left', height=600, width=600, center=vector(N * dx / 2, N * dy / 2, 0))
scene2 = canvas(title='False Image', align='right', x=800, height=600, width=600, center=vector(N * dx / 2, N * dy / 2, 0))
scene1.lights, scene2.lights = [], []
scene1.ambient, scene2.ambient = color.gray(0.99), color.gray(0.99)

side = linspace(-0.01 * pi, 0.01 * pi, N)
x, y = meshgrid(side, side)

aperture_side = linspace(-d / 2, d / 2, N)
X, Y = meshgrid(aperture_side, aperture_side)

valid_mask = (X * X + Y * Y) <= ((d / 2) ** 2)
k = 2 * pi / lamda
k_x = k * x / R
k_y = k * y / R

E_field = zeros((N, N))
for i in range(N):
    for j in range(N):
        E_field[i, j] = sum(cos(k_x[i, j] * X + k_y[i, j] * Y) * dx * dy * valid_mask) / R

# Real
intensity = (E_field) ** 2
maxI = amax(intensity)
base_color = vector(1 / maxI, 1 / maxI, 1 / maxI)
for i in range(N):
    for j in range(N):
        box(canvas=scene1, pos=vector(i * dx, j * dy, 0), length=dx, height=dy, width=dx, color=base_color*intensity[i, j])
       
# Rayleigh Criterion
min_intensity = intensity[50][50]
min = 0

tmp = 50
while tmp < N and intensity[tmp][50] <= min_intensity:
    min_intensity = intensity[tmp][50]
    min_pos = tmp
    tmp += 1

# False
intensity = abs(E_field)
maxI = amax(intensity)
base_color = vector(1 / maxI, 1 / maxI, 1 / maxI)
for i in range(N):
    for j in range(N):
        box(canvas=scene2, pos=vector(i * dx, j * dy, 0), length=dx, height=dy, width=dx, color=base_color*intensity[i, j])

sim_theta = -0.01 * pi + min_pos * (0.02 * pi) / N
print("Simulation:", sim_theta)
print("Theory (1.22 * lamda / d):", 1.22 * lamda / d)
