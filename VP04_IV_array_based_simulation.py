import numpy as np
from vpython import *

A, N, omega = 0.10, 50, 2*pi/1.0
size, m, k, d = 0.06, 0.1, 10.0, 0.4
scene = canvas(title='Spring Wave', width=800, height=300, background=vec(0.5,0.5,0), center = vec((N-1)*d/2, 0, 0))
msgt = text(text = 'Simulating for a few seconds...', pos = vec(0,2,0), height = 0.5)
sim_rate = 3000

'''
balls = [sphere(radius=size, color=color.red, pos=vector(i*d, 0, 0), v=vector(0,0,0)) for i in range(N)] #3
springs = [helix(radius = size/2.0, thickness = d/15.0, pos=vector(i*d, 0, 0), axis=vector(d,0,0)) for i in range(N-1)] #3
'''

c = curve([vector(i*d, 1.0, 0) for i in range(N)], color=color.black) #1
#ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d, np.arange(N)*d, np.zeros(N), np.ones(N)*d #5
Unit_K, n = 2*pi/(N*d), 10
Wavevector = n*Unit_K
phase = Wavevector*arange(N)*d
ball_pos, ball_orig, ball_v, spring_len = np.arange(N)*d+A*np.sin(phase), np.arange(N)*d, np.zeros(N), np.ones(N)*d

t, dt = 0, 0.0003

T, flg, esp, cnt, avgcnt = 0, 0, 0.000001, 0, 0
std = 0
mxd = -1e9
ins = 0

while True:
    rate(sim_rate)
    t += dt
    cnt += 1
    #ball_pos[0] = A * sin(omega * t ) #4
    
    #update spring status
    spring_len[:-1] = ball_pos[1:]-ball_pos[:-1]
    spring_len[-1] = (ball_orig[-1]-ball_pos[-1])+(ball_pos[0]-ball_orig[0])+d

    #update ball position 
    ball_v[1:] += (-k*(spring_len[:-1]-d)/m*dt +k*(spring_len[1:]-d)/m*dt) #6
    ball_v[0] += (k*(spring_len[0]-d)/m*dt-k*(spring_len[-1]-d)/m*dt)
    ball_pos += ball_v*dt
    
    ball_disp = ball_pos - ball_orig
    
    '''
    for i in range(N): balls[i].pos.x = ball_pos[i] #3
    for i in range(N-1): #3
        springs[i].pos = balls[i].pos #3
        springs[i].axis = balls[i+1].pos - balls[i].pos #3
    '''
    
    for i in range(N): #drawing the wave
        c.modify(i, y = ball_disp[i]*4+1)

    #period
    if cnt <= sim_rate*2:
        mxd = max(mxd,spring_len[std])
    else: 
        if spring_len[std] <= mxd+esp and spring_len[std] >= mxd-esp:
            if flg != 0 and ins == 0:
                #print(t-flg)
                T = ((t-flg)+T*avgcnt)/(avgcnt+1)
                avgcnt += 1
            ins = 1
            flg = t
        else:
            ins = 0

    #output
    if cnt == sim_rate*5:
        print("Period:",T)
        msg1 = text(text = 'Period: '+str(T)+' (s)', pos = vec(0,-0.5,0), height = 0.4)
        print("Angular Frequency:",2*pi/T)
        msg2 = text(text = 'Angular Frequency: '+str(2*pi/T)+' (rad/s)', pos = vec(0,-1.5,0), height = 0.4)
        break
    



