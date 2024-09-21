from vpython import *
import numpy as np
from histogram import *

# some constants or variables
N = 200
m, size = 4E-3/6E23, 31E-12*10 # He atom are 10 times bigger for easiear collision but not too big for accuracy
L = ((24.4E-3/(6E23))*N)**(1/3.0)/2 + size # 2L is the cubic container's original length, width, and height
Lx, Ly, Lz = 2*L, 2*L, 2*L
k, T = 1.38e-23, 298.0 # boltzmann constant and initial temperature
gamma = 5/3
t, dt = 0, 3e-13
vrms = (2*k*1.5*T/m)**0.5 # the initial root mean square velocity
stage = 0 # stage number
atoms = [] # list to store atoms
v_W = L / (20000.0*dt) # the speed with which the walls move towards the center

# histogram setting
deltav = 50. # slotwidth for v histogram
vdist = graph(x=800, y=0, ymax = N*deltav/1000.,width=500, height=300, xtitle='v', ytitle='dN', align = 'left')
theory_low_T = gcurve(color=color.cyan) # for plot of the curve for the atom speed distribution
dv = 10.
for v in arange(0.,4201.+dv,dv): # theoretical speed distribution
    theory_low_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*T))**1.5)*exp((-0.5*m*v**2)/(k*T))*(v**2)*dv))

# for the simulation speed distribution
observation = ghistogram(graph = vdist, bins=arange(0.,4200.,deltav), color=color.red) 
observe_stg2 = ghistogram(graph = vdist, bins = arange(0.,4200.,deltav), color=color.blue)
observe_stg3 = ghistogram(graph = vdist, bins = arange(0.,4200.,deltav), color=color.green)

#initialization
scene = canvas(width=500, height=500, background=vector(0.2,0.2,0), align = 'left')
container = box(length = 2*L, height = 2*L, width = 2*L, opacity=0.2, color = color.yellow )

# particle position array and particle velocity array, N particles and 3 for x, y, z
p_a, v_a = np.zeros((N,3)), np.zeros((N,3))

# initialize the position and the velocity of particle
for i in range(N):
    #position
    p_a[i] = [2 * L*random() - L, 2 * L*random() - L, 2 * L*random() - L] # set particle position randomly
    if i== N-1: # the last atom is with yellow color and leaves a trail
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=color.yellow, make_trail = True, retain = 50)
    else: # other atoms are with random color and leaves no trail
        atom = sphere(pos=vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]), radius = size, color=vector(random(), random(), random()))

    #velocity
    ra = pi*random()
    rb = 2*pi*random()
    v_a[i] = [vrms*sin(ra)*cos(rb), vrms*sin(ra)*sin(rb), vrms*cos(ra)] # initial speed of the particle 

    atoms.append(atom)

# the function for handling velocity after collisions between two atoms
def vcollision(a1p, a2p, a1v,a2v):
    v1prime = a1v - (a1p - a2p) * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2)
    v2prime = a2v - (a2p - a1p) * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2)
    return v1prime, v2prime

# self-defined compare function
def cmpzero(x):
    if x > 0: return 1
    elif x == 0: return 0
    else: return -1

# variables
times = 0
P_imp = 0
flg = 0 # used to control stage switching

# keyboard input
def NextStage():
    global stage, flg
    stage += 1
    flg = 0

# button
button(text = 'Next Stage', pos = scene.title_anchor, bind = NextStage)

# main
print("--------start simulating--------")

while True:
    stgctrl = 0
    t += dt
    times += 1
    rate(10000)
    
    p_a += v_a*dt # calculate new positions for all atoms
    for i in range(N): atoms[i].pos = vector(p_a[i, 0], p_a[i, 1], p_a[i, 2]) # to display atoms at new positions
    
    # stage 0 
    if stage == 0: observation.plot(data = np.sqrt(np.sum(np.square(v_a),-1))) ## freeze histogram while going from stage 0 to stage 1
    # stage 1
    if stage == 1 and Lx > L:
        stgctrl = 1
        Lx -= 2*v_W*dt
        container.length -= 2*v_W*dt
    # stage 2
    if stage == 2:
        if flg == 0:
            stg2_Ek = sum(0.5*m*np.sum(np.square(v_a),-1))
            stg2_T = stg2_Ek/(3*N*k/2)
            for v in arange(0.,4201.+dv,dv): # theoretical speed distribution
                theory_low_T.plot(pos=(v,(deltav/dv)*N*4.*pi*((m/(2.*pi*k*stg2_T))**1.5)*exp((-0.5*m*v**2)/(k*stg2_T))*(v**2)*dv))
            flg = 1
        observe_stg2.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))
    # stage 3
    if stage == 3:
        if flg == 0:
            Lx = 2*L
            container.length = 2*L
            flg = 1
        observe_stg3.plot(data = np.sqrt(np.sum(np.square(v_a),-1)))
        
    
    ### find collisions between pairs of atoms, and handle their collisions
    r_array = p_a-p_a[:,np.newaxis] # array for vector from one atom to another atom for all pairs of atoms
    rmag = np.sqrt(np.sum(np.square(r_array),-1)) # distance array between atoms for all pairs of atoms
    hit = np.less_equal(rmag,2*size)-np.identity(N) # if smaller than 2*size meaning collision may happen
    # note: np.identity(N) creates an NxN identity matrix
    hitlist = np.sort(np.nonzero(hit.flat)[0]).tolist() # change hit to a list
    
    for ij in hitlist: # i,j encoded as i*Natoms+j
        i, j = divmod(ij,N) # atom pair, i-th and j-th atoms, hit each other
        hitlist.remove(j*N+i) # remove j,i pair from list to avoid handling the collision twice
        if sum((p_a[i]-p_a[j])*(v_a[i]-v_a[j])) < 0: # only handling collision if two atoms are approaching each other
            v_a[i], v_a[j] = vcollision(p_a[i], p_a[j], v_a[i], v_a[j]) # handle collision

    # find collisions between the atoms and the walls, and handle their elastic collisions
    for i in range(N):
        if abs(p_a[i][0]) >= Lx/2 - size and p_a[i][0]*v_a[i][0] > 0:
            P_imp += abs(v_a[i][0]*m*2)
            v_a[i][0] = - (v_a[i][0] + 2*v_W*cmpzero(v_a[i][0])*stgctrl)
        if abs(p_a[i][1]) >= Ly/2 - size and p_a[i][1]*v_a[i][1] > 0:
            P_imp += abs(v_a[i][1]*m*2)
            v_a[i][1] = - v_a[i][1]
        if abs(p_a[i][2]) >= Lz/2 - size and p_a[i][2]*v_a[i][2] > 0:
            P_imp += abs(v_a[i][2]*m*2)
            v_a[i][2] = - v_a[i][2]

    # print some values
    if times%1000 == 0:
        total_Ek = sum(0.5*m*np.sum(np.square(v_a),-1))
        curT = total_Ek/(3*N*k/2)
        P = P_imp/(1000*dt)/((Lx*Lx+Ly*Ly+Lz*Lz)*2)
        V = Lx*Ly*Lz
        
        print("Temperature:", curT, "(K)")
        print("Pressure:", P, "(N/m^2)")
        print("Volume:", V, "(m^3)")
        print("P*V:", P*V)
        print("N*k*T:", N*k*curT)
        print("P*(V**gamma):", P*(V**gamma))
        print("--------------------------------")

        P_imp = 0

