import torch
import numpy as np
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# to parent dir  
from torchint import trapz_integrate, simpson_integrate, booles_integrate, gauss_integrate, mc_integrate
from torchint import set_backend, get_data_type

# Method 1: Trapezoidal rule
data_type=torch.float32
device_type='cuda'
set_backend(data_type, device_type)

# Integrand
def function(x,y,z,params):
    a = params[0]
    b = params[1]
    c = params[2]
    return a*torch.exp(-b*(x**2+y**2+z**2))+c*torch.sin(x)*torch.cos(y)*torch.exp(z)

# Parameters
a_values=torch.linspace(1.0,10.0,10000, device=device_type,dtype=data_type) 
b_values=torch.linspace(2.0,20.0,10000, device=device_type,dtype=data_type)
c_values=torch.linspace(0.5,5,10000, device=device_type,dtype=data_type) 
param_values=torch.stack((a_values,b_values,c_values),dim=1) #combine to one variable

# user-defined hyper-parameters
bound=[[0,1],[0,1],[0,1]]
num_point=[33,33,33]

def boundary(x, y, z):
    condition1 = x**2 + y**2 + z**2 > 0.2
    condition2 = x**2 + y**2 + z**2 < 0.8
    return condition1 & condition2

# calculation and timing
start_time = time.time()
integral_values=trapz_integrate(function,param_values,bound,num_point,boundary)
end_time = time.time()
elapsed_time = end_time - start_time

#print results
print(integral_values)
print("time used: "+ str(elapsed_time)+ "s")
print(integral_values.dtype)
print(integral_values.device)
print(get_data_type())
torch.cuda.empty_cache()

#########################################################
def function(x):
    return torch.sin(x)

bound=[[0,1]]
num_point=[33]

# calculation and timing
start_time = time.time()
integral_values=trapz_integrate(function,None,bound,num_point,None)
end_time = time.time()
elapsed_time = end_time - start_time

#print results
print(integral_values)
print("time used: "+ str(elapsed_time)+ "s")
print(integral_values.dtype)
print(integral_values.device)

torch.cuda.empty_cache()