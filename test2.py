import numpy as np
from scipy.optimize import fsolve
import datetime

d = 0.00794
g = 9.81
rho = 1000
mu = 0.001
epsilon = 0.0000015
a1 = 0.32*0.26
a2 = np.pi*((d/2)**2)
k = 0.42*(1-(d**2/0.26**2))
timestep = 0.01


def v2(h, f):
    return np.sqrt((2*d*g*h)/(d+(L*f)+(k*d)))

def re(h, f):
    return (rho*v2(h, f)*d)/mu

def f(y, h):
    return (1/np.sqrt(y)) + (2*np.log10(((epsilon/d)/3.7)+(2.51/(re(h, y)*np.sqrt(y)))))

def getV2(h):
    friction = fsolve(f,0.02,args=(h),maxfev=1000)[0]
    with open("frictionvals.txt", 'a') as file1:
        file1.write(str(friction)+"\n")
    with open("headlossvals.txt", 'a') as file1:
        headloss = L*(v2(h, friction)**2)*friction/d/2/g
        file1.write(str(headloss)+"\n")
    with open("reynolds.txt", 'a') as file1:
        file1.write(str(re(h, friction))+"\n")
    with open("v2vals.txt", 'a') as file1:
        file1.write(str(v2(h, friction))+"\n")
    return v2(h, friction)

def getNextH(hPrev):
    return hPrev - (getV2(hPrev)*a2/a1*timestep)

def getTimeToDrain():
    hCurr = hinit
    time = 0
    while(hCurr > hfinal):
        time += timestep
        hCurr = getNextH(hCurr)
    
    return time

lengths = [0.2, 0.3, 0.4, 0.6]
open('frictionvals.txt', 'w').close()
open('headlossvals.txt', 'w').close()
open('reynolds.txt', 'w').close()
open('v2vals.txt', 'w').close()
for i in lengths:
    L = i
    hinit = 0.1 + (L/150)
    hfinal = 0.02 + (L/150)
    drainTime = getTimeToDrain()
    print(str(datetime.timedelta(seconds=drainTime))+"\n")




