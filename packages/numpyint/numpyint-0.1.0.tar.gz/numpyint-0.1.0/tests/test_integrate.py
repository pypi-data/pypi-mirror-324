import sys
import os
import numpy as np
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))# to parent dir  
from numpyint import trapz_integrate, simpson_integrate, booles_integrate, gauss_integrate, mc_integrate
from numpyint import set_backend, get_data_type

data_type=np.float64
set_backend(data_type)

# Integrand
def function(x, y, z, params):
    a = params[0]
    b = params[1]
    c = params[2]
    return a * np.exp(-b * (x**2 + y**2 + z**2)) + c * np.sin(x) * np.cos(y) * np.exp(z)

# Parameters
a_values = np.linspace(1.0, 10.0, 1000, dtype=data_type)
b_values = np.linspace(2.0, 20.0, 1000, dtype=data_type)
c_values = np.linspace(0.5, 5, 1000, dtype=data_type)
param_values = np.stack((a_values, b_values, c_values), axis=1)  # combine to one variable

# user-defined hyper-parameters
bound = [[0, 1], [0, 1], [0, 1]]
num_point = 1000

def boundary(x1, x2, x3):
    condition1 = x1**2 + x2**2 + x3**2 > 0.2
    condition2 = x1**2 + x2**2 + x3**2 < 0.8
    return condition1 & condition2

# calculation and timing
start_time = time.time()
integral_values = mc_integrate(function, param_values, bound, num_point, boundary)
end_time = time.time()
elapsed_time = end_time - start_time

# print results
print(integral_values)
print("time used: " + str(elapsed_time) + "s")
print(integral_values.dtype)

#################################

def function(x):
    return np.sin(x)

bound = [[0,1]]

num_point = 10000

# calculation and timing
start_time = time.time()
integral_values = mc_integrate(function, None, bound, num_point, None)
end_time = time.time()
elapsed_time = end_time - start_time

# print results
print(integral_values)
print("time used: " + str(elapsed_time) + "s")
print(integral_values.dtype)