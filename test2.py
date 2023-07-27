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
dTjoint = 0.0111125
a3 = np.pi*((dTjoint/2)**2)
k = 0.42*(1-(d**2/0.26**2))
k2 = 1
k3 = 1 - (d/dTjoint)
reThres = 2300
timestep = 0.01

# Function for v2 of flow entering tube derived form bernouillis equation
def v2(L, h, f, withTjoint):
    if (not withTjoint):
        return np.sqrt((2*d*g*h)/(d+(L*f)+(k*d)))
    else:
        return np.sqrt((2*d*g*h)/(d+(L*f)+(k*d)+(k2*d)+(2*k3*d*((a2/2/a3)**2))))

# Function for reynolds number in terms of v2
def re(L, h, f, withTjoint):
    return (rho*v2(L, h, f, withTjoint)*d)/mu

# Implicit funciton for friction factor in terms reynolds number -> v2 -> f
# Fully turbulent (Colebrook's Equation)
def f(y, L, h, withTjoint):
    return (1/np.sqrt(y)) + (2*np.log10(((epsilon/d)/3.7)+(2.51/(re(L, h, y, withTjoint)*np.sqrt(y)))))

# Implicit funciton for friction factor in terms reynolds number -> v2 -> f
# Fully laminar (64/Re)
def fLam(y, L, h, withTjoint):
    return y - (64/re(L, h, y, withTjoint))

# Function to get v2 by solving at specific height by getting f (solving implicit function with scipy fsolve)
def getV2(L, h, isTurbulent, withTjoint):
    if isTurbulent:
        friction = fsolve(f,0.02,args=(L,h,withTjoint),maxfev=1000)[0]
    else:
        friction = fsolve(fLam,0.02,args=(L,h,withTjoint),maxfev=1000)[0]

    if re(L, h, friction, withTjoint) < reThres:
        isTurbulent = False

    with open("frictionvals.txt", 'a') as file1:
        file1.write(str(friction)+"\n")
    with open("headlossvals.txt", 'a') as file1:
        headloss = L*(v2(L, h, friction, withTjoint)**2)*friction/d/2/g
        file1.write(str(headloss)+"\n")
    with open("reynolds.txt", 'a') as file1:
        file1.write(str(re(L, h, friction, withTjoint))+"\n")
    with open("v2vals.txt", 'a') as file1:
        file1.write(str(v2(L, h, friction, withTjoint))+"\n")
    return v2(L, h, friction, withTjoint), isTurbulent

# Function to get next height based on v2
def getNextH(L, hPrev, isTurbulent, withTjoint):
    v2, isTurbulent = getV2(L, hPrev, isTurbulent, withTjoint)
    if (not withTjoint):
        return (hPrev - (v2*a2/a1*timestep)), isTurbulent
    else:
        return (hPrev - (v2*a2/a1*timestep)), isTurbulent
    

# Main function to get time to drain depeding on length of tube and if T-joint is attached
def getTimeToDrain(L, withTjoint):
    hInit = 0.1 + (L/150)
    hCurr = hInit
    time = 0
    isTurbulent = True
    while(hCurr > (hInit - 0.08)):
        time += timestep
        hCurr, isTurbulent = getNextH(L, hCurr, isTurbulent, withTjoint)  
    return time


lengths = [0.1, 0.2, 0.3, 0.4, 0.6]
expResults = [199, 214, 266, 288]
open('frictionvals.txt', 'w').close()
open('headlossvals.txt', 'w').close()
open('reynolds.txt', 'w').close()
open('v2vals.txt', 'w').close()
withTjoint = True
for i in lengths:
    L = i
    drainTime = getTimeToDrain(L, withTjoint)
    print(str(i) + "cm: " + str(datetime.timedelta(seconds=drainTime))+"\n")







