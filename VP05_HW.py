from vpython import *
from diatomic import *

N = 20 # 20 molecules
L = ((24.4E-3/(6E23))*N)**(1/3.0)/50 # 2L is the length of the cubic container box, the number is made up
m = 14E-3/6E23 # average mass of O and C
k, T = 1.38E-23, 298.0 # some constants to set up the initial speed
initial_v = (3*k*T/m)**0.5 # some constant
shr = 0.3 # some constant

scene = canvas(width = 400, height =400, align = 'left', background = vec(1, 1, 1))
container = box(length = 2*L, height = 2*L, width = 2*L, opacity=0.4, color = color.yellow )
energies = graph(width = 600, align = 'left', ymin=0)
c_avg_com_K = gcurve(color = color.green)
c_avg_v_P = gcurve(color = color.red)
c_avg_v_K = gcurve(color = color.purple)
c_avg_r_K = gcurve(color = color.blue)

# average values
avg_com_K, avg_v_P, avg_v_K, avg_r_K = 0, 0, 0, 0

COs = []

for i in range(N): # initialize the 20 CO molecules
    O_pos = vec(random()-0.5, random()-0.5, random()-0.5)*L # random() yields a random number between 0 and 1
    CO = CO_molecule(pos=O_pos, axis = vector(1.0*d, 0, 0)) # generate one CO molecule
    CO.C.v = vector(initial_v*random(), initial_v*random(), initial_v*random()) # set up the initial velocity of C
    CO.O.v = vector(initial_v*random(), initial_v*random(), initial_v*random()) # set up the initial velocity of O
    COs.append(CO) # store this molecule into list COs

times = 0 # number of loops that has been run

dt = 5E-16
t = 0 # current time

#Collision function
def Collision(b1, b2):
    colvec = b2.pos-b1.pos
    u1 = b1.v+(2*b2.m/(b1.m+b2.m))*colvec*dot(colvec,b2.v-b1.v)/dot(colvec,colvec)
    u2 = b2.v+(2*b1.m/(b1.m+b2.m))*colvec*dot(colvec,b1.v-b2.v)/dot(colvec,colvec)
    b1.v = u1
    b2.v = u2

while True:
    rate(3000)
    for CO in COs:
        CO.time_lapse(dt)
        
    # collisions between the atoms of different molecules
    for i in range(N-1):
        for j in range(i+1,N):
            if mag(COs[i].O.pos-COs[j].O.pos) <= (COs[i].O.radius+COs[j].O.radius)*shr:
                Collision(COs[i].O,COs[j].O)
            if mag(COs[i].O.pos-COs[j].C.pos) <= (COs[i].O.radius+COs[j].C.radius)*shr:
                Collision(COs[i].O,COs[j].C)
            if mag(COs[i].C.pos-COs[j].O.pos) <= (COs[i].C.radius+COs[j].O.radius)*shr:
                Collision(COs[i].C,COs[j].O)
            if mag(COs[i].C.pos-COs[j].C.pos) <= (COs[i].C.radius+COs[j].C.radius)*shr:
                Collision(COs[i].C,COs[j].C)
            
    # collisions of the atoms on walls
    for CO in COs:
        #O
        if CO.O.pos.x >= L-CO.O.radius or CO.O.pos.x <= -L+CO.O.radius:
            CO.O.v.x *= -1
        if CO.O.pos.y >= L-CO.O.radius or CO.O.pos.y <= -L+CO.O.radius:
            CO.O.v.y *= -1
        if CO.O.pos.z >= L-CO.O.radius or CO.O.pos.z <= -L+CO.O.radius:
            CO.O.v.z *= -1
        
        #C
        if CO.C.pos.x >= L-CO.C.radius or CO.C.pos.x <= -L+CO.C.radius:
            CO.C.v.x *= -1
        if CO.C.pos.y >= L-CO.C.radius or CO.C.pos.y <= -L+CO.C.radius:
            CO.C.v.y *= -1
        if CO.C.pos.z >= L-CO.C.radius or CO.C.pos.z <= -L+CO.C.radius:
            CO.C.v.z *= -1

    
    # sum com_K, v_K, v_P, and r_K for all molecules
    total_com_K, total_v_K, total_v_P, total_r_K = 0, 0, 0, 0
    for CO in COs:
        total_com_K += CO.com_K()
        total_v_K += CO.v_K()
        total_v_P += CO.v_P()
        total_r_K += CO.r_K()
    
    # calculate the average values since the beginning of the simulation
    avg_com_K = (avg_com_K*times+total_com_K)/(times+1)
    avg_v_K = (avg_v_K*times+total_v_K)/(times+1)
    avg_v_P = (avg_v_P*times+total_v_P)/(times+1)
    avg_r_K = (avg_r_K*times+total_r_K)/(times+1)
    
    t += dt
    times += 1
    
    # plot avg_com_K, avg_v_K, avg_v_P, and avg_r_K
    c_avg_com_K.plot(pos = (t, avg_com_K))
    c_avg_v_K.plot(pos = (t, avg_v_K))
    c_avg_v_P.plot(pos = (t, avg_v_P))
    c_avg_r_K.plot(pos = (t, avg_r_K))

