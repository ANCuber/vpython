import numpy as np
from vpython import *

A, N, omega = 0.10, 50, 2*pi/1.0
m, k, d = 0.1, 10.0, 0.4
scene = canvas(title='Spring Wave', width=800, height=300, background=vec(0.5,0.5,0), center = vec((N-1)*d/2, 0, 0))
msgt = text(text = 'Simulating for a few seconds...', pos = vec(0,2,0), height = 0.4)
sim_rate = 5000

def Simulation(n):
    c = curve([vector(i*d, -0.5, 0) for i in range(N)], color=color.black)
    Unit_K = 2*pi/(N*d)
    Wavevector = n*Unit_K
    phase = Wavevector*arange(N)*d
    ball_pos, ball_orig, ball_v = np.arange(N)*d+A*np.sin(phase), np.arange(N)*d, np.zeros(N)
    spring_len = np.ones(N)*d

    t, dt = 0, 0.0003
    preset = 6

    T, flg, esp, cnt, avgcnt = 0, 0, 0.000001, 0, 0
    std = 0
    mxd = -1e9
    ins = 0


    while True:
        rate(sim_rate)
        t += dt
        cnt += 1
    
        #update spring status
        spring_len[:-1] = ball_pos[1:]-ball_pos[:-1]
        spring_len[-1] = (ball_orig[-1]-ball_pos[-1])+(ball_pos[0]-ball_orig[0])+d

        #update ball position 
        ball_v[1:] += (-k*(spring_len[:-1]-d)/m*dt +k*(spring_len[1:]-d)/m*dt) 
        ball_v[0] += (k*(spring_len[0]-d)/m*dt-k*(spring_len[-1]-d)/m*dt)
        ball_pos += ball_v*dt
    
        ball_disp = ball_pos - ball_orig
    
        for i in range(N): #drawing the wave
            c.modify(i, y = ball_disp[i]*4+1)

        #period
        if cnt <= sim_rate*preset*0.4:
            mxd = max(mxd,spring_len[std])
        else: 
            if spring_len[std] <= mxd+esp and spring_len[std] >= mxd-esp:
                if flg != 0 and ins == 0:
                    T = ((t-flg)+T*avgcnt)/(avgcnt+1)
                    avgcnt += 1
                ins = 1
                flg = t
            else:
                ins = 0

        #result
        if cnt == sim_rate*preset:
            c.clear()
            print("i:",n,"Period:",T)
            return (Wavevector,2*pi/T)

#Graph
dispersion = graph(title = 'Dispersion Relationship', xtitle = 'wavevector', ytitle = 'angular frequency')
ang = gdots(graph = dispersion, color = color.green, radius = 5)

#Drawing graph
for i in range(1,int(N/2)):
    ang.plot(pos = Simulation(i))
