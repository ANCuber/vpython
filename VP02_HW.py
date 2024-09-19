#Importing packages
from vpython import *
import math

#Setting parameters
ball_size, ball_m = 0.2, 1
top = 1 #the height of the device
dt, k, g = 0.0001, 150000, 9.8
L = 2 #rope length
sim_rate = 5000
N = 3 #how many balls are lifted at the beginning

#Variables
t = 0
sum_Ek = 0
sum_U = 0

#Creating objects
scene = canvas(width = 500, height = 500, centre = vec(0,0,0), background = vec(0.5,0.5,0), align = 'left')
top_balls = []
ropes = []
balls = []

#Building the device and Lifting the ball(s)
for i in range(5):
    top_balls.append(sphere(radius = ball_size*0.2, color = color.white, pos = vec((i-2)*0.4,top,0)))
    
    if i < N:
        balls.append(sphere(radius = ball_size, color = color.white))
        balls[i].pos = vec((i-2)*0.4-math.sqrt(2**2-1.95**2),-0.95,0);
    else:
        balls.append(sphere(radius = ball_size, color = color.white, pos = vec((i-2)*0.4,top-L-ball_m*g/k,0)))
    
    balls[i].v = vec(0,0,0)
    balls[i].m = ball_m
    ropes.append(cylinder(radius = ball_size*0.1, pos = top_balls[i].pos, axis = balls[i].pos-top_balls[i].pos))

print("Pre-building succeeded.")

#Significant function(s)
def Collision(b1, b2):
    colvec = b2.pos-b1.pos
    u1 = b1.v+(2*b2.m/(b1.m+b2.m))*colvec*dot(colvec,b2.v-b1.v)/dot(colvec,colvec)
    u2 = b2.v+(2*b1.m/(b1.m+b2.m))*colvec*dot(colvec,b1.v-b2.v)/dot(colvec,colvec)
    return (u1, u2)

#Creating the graph windows and curves
GraphWin1 = graph(width = 450, align = 'right', xtitle = 't(s)', ytitle = 'Total Energy (Blue: Ek(J), Green: Ug(J))')
GraphWin2 = graph(width = 450, align = 'right', xtitle = 't(s)', ytitle = 'Avg Energy (Blue: Ek(J), Green: Ug(J))')

Ek_fun = gcurve(graph = GraphWin1, color = color.blue, width = 2)
U_fun = gcurve(graph = GraphWin1, color = color.green, width = 2)

Ek_avg = gcurve(graph = GraphWin2, color = color.blue, width = 2)
U_avg = gcurve(graph = GraphWin2, color = color.green, width = 2)

#Ek_msg = text(text = "All Kinetic Energies: Blue Line", scene = GraphWin, color = color.blue)

#Simulation
print("Simulation begins.")

while True:
    t += dt#Update the current time
    rate(sim_rate)
    
    total_Ek = 0
    total_U = 0

    #Update positions and some related information
    for i in range(5):
        T_force = -k*(mag(ropes[i].axis)-L)*ropes[i].axis.norm()
        balls[i].a = vector(0,-g,0)+T_force/ball_m

        balls[i].v += balls[i].a*dt
        balls[i].pos += balls[i].v*dt
        
        total_Ek += ((ball_m)*(dot(balls[i].v,balls[i].v)))/2
        
        total_U += ball_m*g*(balls[i].pos.y-(top-L-ball_m*g/k))

        ropes[i].axis = balls[i].pos-ropes[i].pos
    
    sum_Ek += total_Ek*dt
    sum_U += total_U*dt

    #Check collisions
    for i in range(4):
        if dot(balls[i].pos-balls[i+1].pos,balls[i].pos-balls[i+1].pos) <= (2*ball_size)**2:
            (u1, u2) = Collision(balls[i],balls[i+1])
            balls[i].v = u1
            balls[i+1].v = u2

    #Drawing curves
    Ek_fun.plot(pos = (t,total_Ek))
    U_fun.plot(pos = (t,total_U))
    Ek_avg.plot(pos = (t,sum_Ek/t))
    U_avg.plot(pos = (t,sum_U/t))
    
