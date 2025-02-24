from vpython import *
import numpy as np

R1, R2 = 0.06, 0.12  
z1, z2 = 0.10, 0.00 
I = 1.0
mu = 4 * np.pi * 1e-7  

N, M = 1000, 1000

def LoopCoord(R, i, z):
    return R*cos(2*pi*i/N), R*sin(2*pi*i/N), z

def AreaCoord(R, i, z):
    return R*(i/M), 0, z

def BiotSavart(Pnt, lpnts, dls):
    r = Pnt-lpnts
    return np.sum((I * mu / (4*pi)) * (np.cross(dls, r)) / (np.linalg.norm(r, axis=1) ** 3)[:, None], axis=0)

SmallLoopCut = np.array([LoopCoord(R1, i, z1) for i in range(N+1)])
Small_dl = SmallLoopCut[1:] - SmallLoopCut[:N]
# SmallLoopPnt = (SmallLoopCut[1:] + SmallLoopCut[:N]) / 2
SmallLoopPnt = SmallLoopCut[:N]
LargeLoopCut = np.array([LoopCoord(R2, i, z2) for i in range(N+1)])
Large_dl = LargeLoopCut[1:] - LargeLoopCut[:N]
# LargeLoopPnt = (LargeLoopCut[1:] + LargeLoopCut[:N]) / 2
LargeLoopPnt = LargeLoopCut[:N]

SmallAreaPar = np.array([AreaCoord(R1, i, z1) for i in range(M+1)])
LargeAreaPar = np.array([AreaCoord(R2, i, z2) for i in range(M+1)])
SmallAreaPnt = (SmallAreaPar[1:] + SmallAreaPar[:M]) / 2;
LargeAreaPnt = (LargeAreaPar[1:] + LargeAreaPar[:M]) / 2;

SmallMag = np.array([BiotSavart(SmallAreaPnt[i], LargeLoopPnt, Large_dl) for i in range(M)])
LargeMag = np.array([BiotSavart(LargeAreaPnt[i], SmallLoopPnt, Small_dl) for i in range(M)])

zeros = np.zeros((M, 2), dtype=int)

SmallAreaZ = (np.linalg.norm(SmallAreaPar[1:], axis=1)**2 - np.linalg.norm(SmallAreaPar[:M], axis=1)**2) * pi
LargeAreaZ = (np.linalg.norm(LargeAreaPar[1:], axis=1)**2 - np.linalg.norm(LargeAreaPar[:M], axis=1)**2) * pi

SmallArea = np.hstack((zeros, SmallAreaZ.reshape(-1,1)))
LargeArea = np.hstack((zeros, LargeAreaZ.reshape(-1,1)))

SmallFlux = np.sum(np.sum(SmallArea * SmallMag, axis=1))
LargeFlux = np.sum(np.sum(LargeArea * LargeMag, axis=1))

print(f"Magnetic flux inside the smaller loop: {abs(SmallFlux)}")
print(f"Magnetic flux inside the larger loop: {abs(LargeFlux)}")
