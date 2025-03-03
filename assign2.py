from vpython import *

R = 10 # meter
e0 = 8.854e-12
qe = 1.6e-19

def config_one(n):
    arr = []
    V_tot = 0
    for i in range(n):
        arr.append(vec(R*cos(i*(2*pi/n)), R*sin(i*(2*pi/n)), 0))
    for i in range(n-1):
        for j in range(i+1, n):
            V_tot += qe*qe/mag(arr[i]-arr[j])/(4*pi*e0)
    return V_tot

def config_two(n):
    arr = []
    V_tot = 0
    for i in range(n-1):
        arr.append(vec(R*cos(i*(2*pi/(n-1))), R*sin(i*(2*pi/(n-1))), 0))
        V_tot += qe*qe/mag(arr[i])/(4*pi*e0)
    for i in range(n-2):
        for j in range(i+1, n-1):
            V_tot += qe*qe/mag(arr[i]-arr[j])/(4*pi*e0)
    return V_tot

def cal(n):
    arr = []
    cnt = 0
    for i in range(n-1):
        arr.append(vec(R*cos(i*(2*pi/(n-1))), R*sin(i*(2*pi/(n-1))), 0))
    for i in range(1, n-1):
        if mag(arr[i]-arr[0]) < R:
            cnt += 1
    return cnt
        
def main():
    i = 1
    while True:
        if (config_one(i) > config_two(i)):
            print(i)
            print(cal(i))
            break
        i += 1
        
main()
