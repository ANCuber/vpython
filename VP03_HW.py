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
sim_rate = 1000

#Set the scene
scene = canvas(width=800, height=800, background=vector(0.5,0.5,0), align = 'left')
info = canvas(width=600, height=600, background=vector(0.25,0.25,0.25), align = 'right')

#Some info
msg_start = text(text = 'Simulating... Please wait for a moment.', canvas = info, pos = vec(-10,0,0))

#Celestial body class
class c_body(sphere):
    m = 1
    v = vec(0,0,0)
    a = vec(0,0,0)

#Center of mass
def CM(m1, m2, p1, p2):
    return (m1*p1 + m2*p2)/(m1+m2)

#Set celestial bodies
sun = c_body(canvas = scene, pos = vec(0,0,0), m = mass['sun'], radius = size['sun'], color = color.orange, emissive = True)
earth = c_body(canvas = scene, pos = vec(0,0,0), m = mass['earth'], radius = size['earth'], texture = {'file':textures.earth}, make_trail = True)
moon = c_body(canvas = scene, pos = vec(moon_orbit['r']*cos(theta),moon_orbit['r']*sin(theta),0), m = mass['moon'], radius = size['moon'])

#position
C_em = CM(earth.m,moon.m,earth.pos,moon.pos)
earth.pos -= C_em
moon.pos -= C_em
earth.pos.x += earth_orbit['r']
moon.pos.x += earth_orbit['r']

C_ems = CM(sun.m,earth.m+moon.m,sun.pos,vec(earth_orbit['r'],0,0))
sun.pos -= C_ems
earth.pos -= C_ems
moon.pos -= C_ems

#velocity
earth.v += (moon.m)/(moon.m+earth.m)*vec(0,0,moon_orbit['v'])
moon.v += (earth.m)/(moon.m+earth.m)*vec(0,0,-moon_orbit['v'])
sun.v += (moon.m+earth.m)/(moon.m+earth.m+sun.m)*vec(0,0,earth_orbit['v'])
earth.v += (sun.m)/(moon.m+earth.m+sun.m)*vec(0,0,-earth_orbit['v'])
moon.v += (sun.m)/(moon.m+earth.m+sun.m)*vec(0,0,-earth_orbit['v'])

#Point of view
scene.forward = vec(-1,-1,-1)
scene.center = earth.pos

#G_Force funciton
def G_Force(M, m, pos_vec):
    if mag(pos_vec) == 0:
        return vec(0,0,0)
    return -G*M*m/mag2(pos_vec)*norm(pos_vec)

#Settings for simulation
c_bodies = [moon, earth, sun]
dt = 60*60*6/100

#Simulation
print("Simulation begins.")

cnt = 0
pre = 0
esp = 1e-3
ref = 2

while True:
    rate(sim_rate*1000)

    if cnt <= 1e6 and ref > dot(norm(cross(moon.pos-earth.pos,moon.v-earth.v)),vec(1,0,0)):
        ref = dot(norm(cross(moon.pos-earth.pos,moon.v-earth.v)),vec(1,0,0))
        pre = cnt
    if cnt > 1e6 and abs(dot(norm(cross(moon.pos-earth.pos,moon.v-earth.v)),vec(1,0,0)) - ref) <= esp:
        msg_result = text(text = "The precession period is about "+str("{:.5f}".format(round((cnt-pre)*dt/86400/364.2422,5)))+" years.", pos = vec(-10,-3,0), canvas = info)
        break
    
    #Consider gravity
    for cbody in c_bodies:
        cbody.a = vec(0,0,0)
        for center in c_bodies:
            cbody.a += G_Force(center.m,cbody.m,cbody.pos-center.pos)/cbody.m
        
    for cbody in c_bodies:
        cbody.v += cbody.a*dt
        cbody.pos += cbody.v*dt
    
    scene.center = earth.pos
    cnt += 1


