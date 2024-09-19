from vpython import *
size, m = 0.02, 0.2 # ball size = 0.02 m, ball mass = 0.2kg
L, k = 0.2, 20 # spring original length = 0.2m, force constant = 20 N/m
amplitude = 0.03
b = 0.05 * m * sqrt(k/m)
fa = 0.1
wd = 1*sqrt(k/m)
T = 2*pi/wd

scene = canvas(width=600, height=400, range = 0.3, align = 'left', center=vec(0.3, 0, 0), background=vec(0.5,0.5,0))

'''
wall_left = box(length=0.005, height=0.3, width=0.3, color=color.blue) 
ball = sphere(radius = size, color=color.red)
spring = helix(radius=0.015, thickness =0.01)
oscillation = graph(width = 400, align = 'left', xtitle='t',ytitle='x',background=vec(0.5,0.5,0))
x = gcurve(color=color.red,graph = oscillation)
'''

power = graph(width = 400, align = 'left', xtitle = 't', ytitle = 'avg_power', background=vec(0.5,0.5,0))
Pt = gdots(color=color.green, graph = power, size = 0.000001)

class obj: pass
ball, spring = obj(), obj()

ball.pos = vector(L, 0 , 0) # ball initial position
ball.v = vector(0, 0, 0) # ball initial velocity
ball.m = m
spring.pos = vector(0, 0, 0)

t, dt = 0, 0.001
Pcnt = 0
esp = 0.002
n = 1

while True:
    #rate(1000)
    
    spring.axis = ball.pos - spring.pos # spring extended from spring endpoint A to ball
    spring_force = - k * (mag(spring.axis) - L) * norm(spring.axis) # spring force vector
    sinF = fa*sin(wd*t)*vec(1,0,0)

    ball.a = spring_force/ball.m - b*ball.v/ball.m + sinF/ball.m
    ball.v += ball.a*dt
    ball.pos += ball.v*dt
    
    Pcnt += dot(ball.a*ball.m,ball.v)*dt
    t += dt
    #x.plot(pos=(t,ball.pos.x - L))
    
    '''
    if curt >= 2*pi/wd-esp and curt <= 2*pi/wd+esp:
        Pt.plot(pos = (t,Pcnt/(2*pi/wd)))
        Pcnt = 0
    '''
    
    if (t/T) >= n:
        Pt.plot(pos = (t,Pcnt/T))
        n += 1
        Pcnt = 0
    

