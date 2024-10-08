from vpython import *
import math

# constants

dt, k, g = 0.0001, 150000, vector(0,-9.8,0)

m = 1.0 # mass of each ball
size = 0.2 # ball size
top = 0.5 # ceiling height
N = 2 # number of balls that are lifted
l = 2 # rod length

scene = canvas(width=800, height=1000, center=vec(0, -0.2, 0), background=vec(0.5,0.5,0), align = 'left') 

avgkin = graph(width = 400, align = 'right')
funck = gcurve(graph = avgkin, color=color.blue, width =4)
avgpot = graph(width = 400, align = 'right')
funcp = gcurve(graph = avgpot, color=color.blue, width =4)

pivot = [] # the upper end of the rod
ball = [] # the balls
rod = []

# initial conditions

for i in range(5):
  pivot.append(sphere(radius = size*0.2, color = color.white, pos = vec((i-2)*0.4, top, 0)))

  if i < N:
    ball.append(sphere(radius = size, color = color.white))
    ball[i].pos = vec((i-2)*0.4 - math.sqrt(2**2-1.95**2), -top-0.95, 0);
  
  else:
    ball.append(sphere(radius = size, color = color.white, pos = vec((i-2)*0.4, top - l + m*g.y/k, 0)));

  ball[i].v = vec(0,0,0)
  ball[i].m = m
  rod.append(cylinder(radius = size*0.1, pos = pivot[i].pos, axis = ball[i].pos-pivot[i].pos))

# graph of total E_k U_g
# graph of avg total E_k, U_g

### functions

# function after collision velocity
def af_col_v(m1, m2, v1, v2, x1, x2): 
  v1_prime = v1 + 2*(m2/(m1+m2))*(x1-x2) * dot (v2-v1, x1-x2) / dot (x1-x2, x1-x2)
  v2_prime = v2 + 2*(m1/(m1+m2))*(x2-x1) * dot (v1-v2, x2-x1) / dot (x2-x1, x2-x1)
  return (v1_prime, v2_prime)

# simulation

akin = 0
apot = 0

t = 0 

while (True):
  rate(5000)

  akin = 0
  apot = 0

  #for b in ball: 
  for i in range(5):
    rod[i].axis = ball[i].pos-rod[i].pos

    spring_force = -k * (mag(rod[i].axis) - l) * rod[i].axis.norm()
    ball[i].a = g + spring_force / m

    ball[i].v += ball[i].a * dt
    ball[i].pos += ball[i].v * dt
    
  for i in range(4):
    if dot (ball[i].pos-ball[i+1].pos , ball[i].pos-ball[i+1].pos) <= (2*size)**2:
      (ball[i].v, ball[i+1].v) = af_col_v(ball[i].m, ball[i+1].m, ball[i].v, ball[i+1].v, ball[i].pos, ball[i+1].pos)

  t += dt

  for i in range(5):
    h0 = top - l - m*g.y/k

    akin += 0.5 * m * ball[i].v.mag**2
    apot += - m * g.y * (ball[i].pos.y-h0)

  funck.plot(t,akin)
  funcp.plot(t,apot)
