from vpython import *
import numpy as np

R, L, C = 30, 0.2, 2e-5
T, F = 1/120, 120

W = 2 * pi * F
Z = sqrt(R**2 + (W * L - 1 / (W * C))**2)

def v(t):
    if t < 0 or t >= 12 * T: return 0
    return 36 * sin(2 * pi * F * t)

def vpr(t):
    if t < 0 or t >= 12 * T: return 0
    return 2 * pi * F * 36 * cos(2 * pi * F * t)


t = 0
dt = 1.0/(F * 3000)

scene1 = graph(align = 'left', xtitle='t', ytitle='i (A) blue, v (100V) red, i_the (A) yellow', background=vector(0.2, 0.6, 0.2))
scene2 = graph(align = 'left', xtitle='t', ytitle='Energy (J)', background=vector(0.2, 0.6, 0.2))

i_t = gcurve(color=color.blue, graph = scene1)
v_t = gcurve(color=color.red, graph = scene1)
ith = gcurve(color=color.yellow, graph = scene1)
E_t = gcurve(color=color.red, graph = scene2)

from vpython import graph, gcurve
import numpy as np

def solve_and_plot_vpython(fx, A, B, C, y0, dy0, x_range, dx, scene, y_graph):
    """
    Solves Ay'' + By' + Cy = f(x) and plots y vs x using VPython.
    
    Parameters:
    - fx: function of x
    - A, B, C: coefficients
    - y0: initial y value
    - dy0: initial y' value
    - x_range: tuple (x_start, x_end)
    - dx: step size
    """
    x0, x_end = x_range
    x_vals = []
    y_vals = []

    y1 = y0
    y2 = dy0
    x = x0
    y3 = y0

    # VPython plot setup
    # scene = graph(title="Solution to Ay'' + By' + Cy = f(x)", xtitle='x', ytitle='y')
    # y_graph = gcurve(color=color.cyan)

    mx, mxi = 0, 0
    sumi = 0
    E = 0
    flg = 0

    while x <= x_end:
        i_the = 0.40156 * sin(2 * pi * F * x - 70 / 180 * pi)
        sumi += y1*dx

        x_vals.append(x)
        y_vals.append(y1)
        y_graph.plot(pos=(x, y1))
        v_t.plot(x, 0.01 * v(x))
        if x < 12 * T:
            ith.plot(x, i_the)
        else:
            ith.plot(x, 0)
        if x > 0:
            E_t.plot(x, (L*y1*y1/2 + sumi*sumi/2/C))
            # if L*y1*y1/2 + sumi/C/2*sumi < 1e-8:
            #     print(y1, sumi)
        
        if abs(x-12*T) <= 1e-7:
            E = (L/2)*y1*y1 + sumi*sumi/(2*C)

        if x > 12 * T and (L/2)*y1*y1 + sumi*sumi/(2*C) <= 0.1 * E and flg == 0:
            print("t when the energy decays to 10%:", x, "s");
            flg = 1

        if x >= 8 * T and x <= 9 * T and mx < abs(y1):
            mx = abs(y1)
            mxi = x

        # Runge-Kutta 4th-order
        def dy1dx(x, y1, y2):
            return y2

        def dy2dx(x, y1, y2):
            return (fx(x) - B * y2 - C * y1) / A

        k1_1 = dx * dy1dx(x, y1, y2)
        k1_2 = dx * dy2dx(x, y1, y2)

        k2_1 = dx * dy1dx(x + dx/2, y1 + k1_1/2, y2 + k1_2/2)
        k2_2 = dx * dy2dx(x + dx/2, y1 + k1_1/2, y2 + k1_2/2)

        k3_1 = dx * dy1dx(x + dx/2, y1 + k2_1/2, y2 + k2_2/2)
        k3_2 = dx * dy2dx(x + dx/2, y1 + k2_1/2, y2 + k2_2/2)

        k4_1 = dx * dy1dx(x + dx, y1 + k3_1, y2 + k3_2)
        k4_2 = dx * dy2dx(x + dx, y1 + k3_1, y2 + k3_2)

        y1 += (k1_1 + 2*k2_1 + 2*k3_1 + k4_1) / 6
        y2 += (k1_2 + 2*k2_2 + 2*k3_2 + k4_2) / 6

        x += dx
        y3 = y1
    print("I_cal:", mx)
    print("I_the:", 0.40156)

    print("phi_cal:", (mxi - 8 * T) / T * pi - pi / 2)
    print("phi_the:", atan((W*L-1/(W*C))/R))
    # print("phi:", )

solve_and_plot_vpython(vpr, L, R, 1/C, 0, 0, (0, 20 * T), dt, scene1, i_t);



