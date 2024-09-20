import numpy as np
from vpython import *

A, N, omega = 0.10, 50, 2*pi/1.0
size, m, k, d = 0.06, 0.1, 10.0, 0.4
scene = canvas(title='Spring Wave', width=800, height=300, background=vec(0.5,0.5,0), center = vec((N-1)*d/2, 0, 0))

'''
balls = [sphere(radius=size, color=color.red, pos=vector(i*d, 0, 0), v=vector(0,0,0)) for i in range(N)] 
springs = [helix(radius = size/2.0, thickness = d/15.0, pos=vector(i*d, 0, 0), axis=vector(d,0,0)) for i in range(N-1)] 
'''

c = curve([vector(i*d, 1.0, 0) for i in range(N)], color=color.black) #1
Unit_K, n = 2*pi/(N*d), 10
Wavevector = n*Unit_K
phase = Wavevector*arange(N)*d
ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d+A*np.sin(phase), np.arange(N)*d, np.zeros(N), np.ones(N)*d

t, dt = 0, 0.0003

while True:
    rate(2000)
    t += dt
    
    spring_len[:-1] = ball_pos[1:]-ball_pos[:-1]
    spring_len[-1] = (ball_orig[-1]-ball_pos[-1])+(ball_pos[0]-ball_orig[0])+d

    ball_v[1:] += (-k*(spring_len[:-1]-d)/m*dt +k*(spring_len[1:]-d)/m*dt) 
    ball_v[0] += (k*(spring_len[0]-d)/m*dt-k*(spring_len[-1]-d)/m*dt)
    ball_pos += ball_v*dt
    
    ball_disp = ball_pos - ball_orig
    
    for i in range(N):
        c.modify(i, y = ball_disp[i]*4+1)


