#Importing packages
from vpython import *
import math
import numpy
print("Succeeded in importing packages.")

#Setting parameters
g = 9.8 #set g = 9.8 m/s^2
r = 0.25 #set ball radius
h = 15.0 #initialize the height of the scene
C_drag = 0.9 #drag coefficient
VC = 0.5 #velocity's proportional constant
theta = (math.pi)/4 #angle of the ball's initial velocity
dt = 0.001 #time step
InitPos = vec(-15,r,0)
print("Succeeded in setting parameters.")

#Some variables
total_dis = 0
displacement = 0
MaxH = 0

#Creating Scenes and Objects
scene = canvas(width = 800, height = 1200, align = 'left', center = vec(0,h/2,0), background = vec(0.5,0.5,0))
ball = sphere(radius = r, color = color.red, make_trail = True, trail_radius = 0.05)
floor = box(length = 40, height = 0.01, width = 10, color = vec(1,1,1))
msg = text(text = 'HW01', pos = vec(-10,10,0))
print("Succeeded in creating scencs and objects.")

#Initializing
ball.pos = InitPos
ball.v = vec(20*math.cos(theta),20*math.sin(theta),0)
print("Initializing finished.")

#Creating velocity arrow(s)
ball_vel = arrow(color = color.green, shaftwidth = 0.05)
def UpdateBallVelocity(v,obj):
    v.pos = obj.pos
    v.axis = VC*obj.v
print("Succeeded in creating arrows.")

#Creating a graph window
SvsT = graph(width = 450, align = 'right', xtitle = 't(s)', ytitle = '|v| (m/s)')

#Drawing the graph of speed versus time
FuncSpeed = gcurve(graph = SvsT, color = color.blue, width = 2)

#Bouncing function
def Bouncing():
    global total_dis
    global displacement
    global MaxH
    t = 0
    cnt = 0
    while cnt < 3:
        rate(800)

        ball.v += vec(0,-g,0)*dt-ball.v*C_drag*dt
        ball.pos += ball.v*dt
        
        UpdateBallVelocity(ball_vel,ball)
        FuncSpeed.plot(pos = (t,mag(ball.v)))

        total_dis += math.sqrt(ball.v.x**2+ball.v.y**2+ball.v.z**2)*dt
        MaxH = max(MaxH,ball.pos.y)
        t += dt

        if ball.pos.y <= r:
            ball.v.y *= -1
            cnt += 1
    displacement = ball.pos.x-InitPos.x

print("simulation begins.")
Bouncing()
print("Simulation ended.")

#Showing some final information
msg.visible = False
msg_disp = text(text = 'Displacement = ' + str("{:.5f}".format(round(displacement,5))) + ' m', pos = vec(-10,12,0))
msg_dist = text(text = 'Total Distance = ' + str("{:.5f}".format(round(total_dis,5))) + ' m', pos = vec(-10,10,0))
msg_maxh = text(text = 'Largest Height = ' + str("{:.5f}".format(round(MaxH,5))) + ' m', pos = vec(-10,8,0))
print("Information is shown.")

