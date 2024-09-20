from vpython import *

#constants
G = 6.673E-11
mass = {'sun':1.989E30, 'earth':5.972E24, 'moon':7.36E22}
radius = {'earth':6.371E6*10, 'moon':1.317E6*10, 'sun':6.95E8*10}
earth_orbit = {'r':1.495E11, 'v':2.9783E4}
moon_orbit = {'r':3.84E8, 'v':1.022E3}
axis = vec(0,1,0)
theta = 5.145*pi/180

def G_force(self,source):
    return -G*self.m*source.m / mag2(self.pos-source.pos)*norm(self.pos-source.pos)

#background
scene = canvas(width=800, height=800, background=vec(0.5,0.5,0))
scene.forward = vector(-1, -1, 0)
#local_light(pos = vec(0,0,0))

#object
sun = sphere(pos=vec(0,0,0), radius = radius['sun'], m = mass['sun'], color = color.orange, emissive=True)
earth = sphere(pos = vec(earth_orbit['r'],0,0), radius = radius['earth'], m = mass['earth'], texture={'file':textures.earth})
moon = sphere(pos = earth.pos+vec(moon_orbit['r']*cos(theta),moon_orbit['r']*sin(theta),0), radius = radius['moon'], m = mass['moon'], color = color.white, make_trail = True)
earth.v = vector(0, 0, -earth_orbit['v'])
moon.v = earth.v + vector(0, 0, -moon_orbit['v'])
sun.v = vec(0,0,0)

#time
dt=60*60
t = 0

while True:
    scene.center = earth.pos
    rate(1000)
    moon.a = (G_force(moon, earth)+G_force(moon,sun)) / moon.m
    moon.v = moon.v + moon.a * dt
    moon.pos = moon.pos + moon.v * dt
    earth.a = (G_force(earth, moon)+G_force(earth,sun)) / earth.m
    earth.v = earth.v + earth.a *dt
    earth.pos = earth.pos + earth.v * dt
    sun.a = (G_force(sun,moon)+G_force(sun,earth))/sun.m
    sun.v = sun.v+sun.a*dt
    sun.pos = sun.pos+sun.v*dt
    t += dt
