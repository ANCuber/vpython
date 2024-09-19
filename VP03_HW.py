#Import packages
from vpython import *
import math

#Set parameters
G = 6.673E-11
mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun':1.99E30}
Mag = 10 #See the next line
size = {'earth': 6.371E6*Mag, 'moon': 1.317E6*Mag, 'sun':6.95E8*Mag} #10 times larger for better view
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145*pi/180.0
sim_rate = 5000
Slowing = 10

#Set the scene
scene = canvas(width=800, height=800, background=vector(0.5,0.5,0))
scene.light = []
local_light(pos = vec(0,0,0))

#Set celestial bodies
Cme = (mass['moon']*vec(moon_orbit['r'],0,0))/(mass['earth']+mass['moon'])
sun = sphere(pos = vec(0,0,0), m = mass['sun'], radius = size['sun'], color = color.orange, emissive = True)
sun.v = vec(0,0,0)
earth = sphere(pos = (-mass['moon']/(mass['earth']+mass['moon']))*vec(moon_orbit['r']*cos(theta),-moon_orbit['r']*sin(theta),0), m = mass['earth'], radius = size['earth'], make_trail = False, texture = {'file':textures.earth})
earth.v = vec(0,0,moon_orbit['v'])*(mass['moon']/(mass['earth']+mass['moon']))
moon = sphere(pos = (mass['earth']/(mass['earth']+mass['moon']))*vec(moon_orbit['r']*cos(theta),-moon_orbit['r']*sin(theta),0), m = mass['moon'], radius = size['moon'], make_trail = False)
moon.v = vec(0,0,-moon_orbit['v'])*(mass['earth']/(mass['earth']+mass['moon']))

earth.pos += vec(earth_orbit['r']*(mass['sun']/(mass['sun']+mass['earth']+mass['moon'])),0,0)
scene.center = earth.pos
earth.make_trail = True
moon.pos += vec(earth_orbit['r']*(mass['sun']/(mass['sun']+mass['earth']+mass['moon'])),0,0)
#moon.make_trail = True
sun.pos += vec(-earth_orbit['r']*((mass['earth']+mass['moon'])/(mass['sun']+mass['earth']+mass['moon'])),0,0)

earth.v += vec(0,0,-earth_orbit['v']*(mass['sun']/(mass['sun']+mass['earth']+mass['moon'])))
moon.v += vec(0,0,-earth_orbit['v']*(mass['sun']/(mass['sun']+mass['earth']+mass['moon'])))
sun.v = vec(0,0,earth_orbit['v']*((mass['earth']+mass['moon'])/(mass['sun']+mass['earth']+mass['moon'])))

#Point of view
scene.forward = vec(-1,-1,-1)

#Functions
def G_Force(M, m, pos_vec):
    if mag(pos_vec) == 0:
        return vec(0,0,0)
    return -G*M*m/mag2(pos_vec)*norm(pos_vec)

#Settings for simulation
#bodies_c = [moon, earth, sun]
c_bodies = [moon, earth, sun]
bodies = [moon, earth]
dt = 60*60*6/5
dt /= Slowing

#Simulation
print("Simulation begins.")

mx, mn = -1, 1
cnt = 0

while True:
    rate(sim_rate)
    pre = moon.pos-earth.pos
    
    #Consider gravity
    for cbody in c_bodies:
        cbody.a = vec(0,0,0)
        
        for center in c_bodies:
            cbody.a += G_Force(center.m,cbody.m,cbody.pos-center.pos)/cbody.m
        
        cbody.v += cbody.a*dt
        cbody.pos += cbody.v*dt

    aft = moon.pos-earth.pos
    crs = cross(pre,aft)
    cur = math.acos(dot(crs,vec(0,1,0))/mag(crs)*mag(vec(0,1,0)))
    mx = max(cur,mx)
    mn = min(cur,mn)

    if cnt >= sim_rate*20:
        break

    scene.center = earth.pos
    cnt += 1
print(mx/(pi/180), mn/(pi/180))

