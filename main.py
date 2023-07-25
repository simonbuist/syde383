import numpy as np
from matplotlib import pyplot as plt
import math
from scipy.optimize import fsolve

'''
Design Paramter: Discharge Length
Design Performance: total time it takes to drain water 
'''

#Variables for the tank
tank_surface_area = 0.32 * 0.26 
height_start_end = 0.08
height_start_tube = 0.1

#Variables for the tube
tube_length = [0.2,0.3,0.4,0.6] 
avg_time_to_drain = [199,214,266,288] #seconds
diameter = 0.00794 #meters
tube_surface_area = 3.14*(diameter**2)/4
sin_beta = 1/150
roughness = 0.0000015 #roughness of the plastic pipe in meters
relative_roughness = roughness/diameter
print(relative_roughness)
#Common variables
density = 1000 #kg/m^3
P_atm = 101.325 #KPa
array_size = 4
drained_volume = height_start_end * tank_surface_area
viscosity_water = 0.001 #Pa * second = kg/m * s

volumetric_flow_rate = np.empty(array_size)
water_velocity = np.empty(array_size)
for i in range(array_size):
    volumetric_flow_rate[i] = drained_volume/avg_time_to_drain[i]
    water_velocity[i] = volumetric_flow_rate[i]/tube_surface_area





# print(volumetric_flow_rate)
# print(water_velocity)
'''The above calculation proves that: 
If the flow through the tube is laminar and if both the friction on the flow entering the tube and flow accelerations to be negligibly small, then the flow rate is inversely proportional to the length of the discharge tube
'''
#However, further scrutiny is required to assess the friction & liminar vs. turbulent
#Using Bernoulli's equation to get the outlet velocity assuming there's no tube
outlet_velocity_init = (2*9.8*0.1)**1/2 #m/s (initial condition)
Re = density*outlet_velocity_init*diameter/viscosity_water
print (Re)
# equals to 0.98 which is a lot higher than the water_velocity from experimental results
# So we must account for friction
# def coleb_eqtn(y,epsilon = roughness , d = diameter, Rey = Re):
#     return -2.0*math.log((epsilon/d)/3.7+2.51/(Rey*y**1/2))-1/(y**1/2)
def coleb_eqtn(roughness = roughness,d = diameter,Re = Re):
    return (1/(-1.8*math.log(((roughness/d)/3.7)**1.11+6.9/Re)))**2

if (Re > 4000): #turbulent flow
    #get f using Colebrook's equation
    f = coleb_eqtn()
    print (f)

'''Assumption: 
1.Since length of the tube is much greater than the diameter, entrance length is neglected
2.No minor losses => only friction term to the right hand side of Bernoullis Equation
3.Angle of the tube is very small so no change in gravitational energy
Next step: Generate a model to account for friction and compare the results of the model with experimental result. In order to get the time to drain, need to model the volumetric flow rate 
'''



# plt.figure(figsize=[8, 5])
# plt.grid()
# plt.plot(tube_length, volumetric_flow_rate,'o')
# plt.show()
#Apply Bernoulli's Equation the first time


