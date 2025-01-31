import torch
import numpy as np #necessary for Gauss method

GLOBAL_DTYPE=torch.float32
GLOBAL_DEVICE='cpu'

def set_backend(dtype, ddevice):
    """
    Set the default floating-point precision for cupy.

    Parameters:
        dtype (str): The desired precision, either 'float32' or 'float64'.
    """
    
    if dtype not in [torch.float32, torch.float64]:
        raise ValueError("dtype must be torch.float32 or torch.float64")
        
    if ddevice not in ['cuda', 'cpu']:
        raise ValueError("device must be 'cuda' or 'cpu'")
    
    global GLOBAL_DTYPE, GLOBAL_DEVICE
    GLOBAL_DTYPE = dtype
    GLOBAL_DEVICE = ddevice
    # print(f"Backend set to {GLOBAL_DEVICE}.")
    
def get_data_type():
    return GLOBAL_DTYPE, GLOBAL_DEVICE

# Method 1: Trapezoidal rule
def trapz_integrate(func, params, bounds, num_points, boundaries):
    global GLOBAL_DTYPE, GLOBAL_DEVICE
    if params is not None:
        ndim = len(bounds) # determine nD integration
        grids = []
        vector_length = params.shape[0] # length of parameters, for further vectorized integration
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = torch.linspace(bound[0], bound[1], num_point, device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh]
        params_expanded = [params[:, i].view(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded) # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = torch.trapz(Y, grids[dim], dim=dim + 1)  
            
    if params is None:
        ndim = len(bounds) # determine nD integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = torch.linspace(bound[0], bound[1], num_point, device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh]
        Y = func(*expanded_mesh) # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = torch.trapz(Y, grids[dim], dim=dim + 1)  
    return Y

# Method 2: Simpson rule
def simpsons_rule(y, x, dim):
    n = y.size(dim)
    if n % 2 == 0:
        raise ValueError("Number of points must be odd for Simpson's rule.")
    dx = (x[-1] - x[0]) / (n - 1)
    coeffs = torch.ones(n, device=y.device, dtype=y.dtype)
    coeffs[1:-1:2] = 4
    coeffs[2:-1:2] = 2
    coeffs = coeffs.view(*([1] * dim), -1, *([1] * (y.ndim - dim - 1)))
    return torch.sum(y * coeffs, dim=dim) * dx / 3

def simpson_integrate(func,params,bounds,num_points,boundaries):
    global GLOBAL_DTYPE, GLOBAL_DEVICE

    if params is not None:
        ndim = len(bounds) # determine nD integration
        vector_length = params.shape[0] # length of parameters, for further vectorized integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = torch.linspace(bound[0], bound[1], num_point, device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh]
        params_expanded = [params[:, i].view(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded) # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = simpsons_rule(Y, grids[dim], dim=dim + 1)
    
    if params is None:
        ndim = len(bounds) # determine nD integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = torch.linspace(bound[0], bound[1], num_point, device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh]
        Y = func(*expanded_mesh) # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = simpsons_rule(Y, grids[dim], dim=dim + 1)
    return Y


# Method 3: Boole's Rule
def booles_rule(y, x, dim):
    n = y.size(dim)
    if (n - 1) % 4 != 0:
        raise ValueError("Number of points minus one must be a multiple of 4 for Boole's rule.")
    dx = (x[-1] - x[0]) / (n - 1)
    coeffs = torch.ones(n, device=y.device, dtype=y.dtype)
    coeffs[0] = 7
    coeffs[-1] = 7
    coeffs[1:-1:4] = 32
    coeffs[2:-1:4] = 12
    coeffs[3:-1:4] = 32
    coeffs[4:-1:4] = 14
    coeffs = coeffs.view(*([1] * dim), -1, *([1] * (y.ndim - dim - 1)))
    return torch.sum(y * coeffs, dim=dim) * 2 * dx / 45

def booles_integrate(func,params,bounds,num_points,boundaries):
    global GLOBAL_DTYPE, GLOBAL_DEVICE

    if params is not None:
        ndim = len(bounds) # determine nD integration
        vector_length = params.shape[0] # length of parameters, for further vectorized integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = torch.linspace(bound[0], bound[1], num_point, device=GLOBAL_DEVICE,dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh]
        params_expanded = [params[:, i].view(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded) # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = booles_rule(Y, grids[dim], dim=dim + 1)
        return Y
    
    if params is None:
        ndim = len(bounds) # determine nD integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = torch.linspace(bound[0], bound[1], num_point, device=GLOBAL_DEVICE,dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh]
        Y = func(*expanded_mesh) # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = booles_rule(Y, grids[dim], dim=dim + 1)
        return Y

# Method 4: Gauss-Legendre rule
def gauss_legendre_rule(y, x, w, dim):
    w = w.view(*([1] * dim), -1, *([1] * (y.ndim - dim - 1)))
    return torch.sum(y * w, dim=dim)

# Additionally, we have nodes & weights for this method from numpy, and convert to
def gauss_legendre_nodes_weights(n, device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE):
    nodes, weights = np.polynomial.legendre.leggauss(n)
    nodes = torch.tensor(nodes, device=device, dtype=dtype)
    weights = torch.tensor(weights, device=device, dtype=dtype)
    return nodes, weights

def gauss_integrate(func,params,bounds,num_points,boundaries):
    global GLOBAL_DTYPE, GLOBAL_DEVICE

    if params is not None:
        ndim = len(bounds) # determine nD integration
        vector_length = params.shape[0] # length of parameters, for further vectorized integration
        grids, weights = [], []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid, weight = gauss_legendre_nodes_weights(num_point)
            grid = 0.5 * (bound[1] - bound[0]) * grid + 0.5 * (bound[1] + bound[0])
            weight = 0.5 * (bound[1] - bound[0]) * weight
            grids.append(grid)
            weights.append(weight)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh] 
        params_expanded = [params[:, i].view(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded)
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = gauss_legendre_rule(Y, grids[dim], weights[dim], dim=dim + 1)
            
    if params is None:
        ndim = len(bounds) # determine nD integration
        grids, weights = [], []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid, weight = gauss_legendre_nodes_weights(num_point)
            grid = 0.5 * (bound[1] - bound[0]) * grid + 0.5 * (bound[1] + bound[0])
            weight = 0.5 * (bound[1] - bound[0]) * weight
            grids.append(grid)
            weights.append(weight)
        mesh = torch.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m.unsqueeze(0) for m in mesh] 
        Y = func(*expanded_mesh)
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).to(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = gauss_legendre_rule(Y, grids[dim], weights[dim], dim=dim + 1)
    return Y


# Method 5: Monte Carlo rule (fixed sampling points per dimension)
def mc_integrate(func,params,bounds,num_points,boundaries):
    global GLOBAL_DTYPE, GLOBAL_DEVICE

    if params is not None:
        ndim = len(bounds)
        vector_length = params.shape[0]
        samples = []
        for bound in bounds:
            sample = torch.rand((vector_length, num_points), device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE) * (bound[1] - bound[0]) + bound[0]
            samples.append(sample.unsqueeze(-1))
        volume = 1.0
        for bound in bounds:
            volume *= (bound[1] - bound[0])
        params_expanded = [params[:, i].view(vector_length, 1, 1) for i in range(params.shape[1])]
        Y = func(*samples, params_expanded)
        if boundaries is not None:
            weight = boundaries(*samples).to(Y.dtype)
            Y = Y * weight
        integral = volume * torch.mean(Y, dim=1).squeeze()
        
    if params is None:
        ndim = len(bounds)
        vector_length = 1
        samples = []
        for bound in bounds:
            sample = torch.rand((vector_length, num_points), device=GLOBAL_DEVICE, dtype=GLOBAL_DTYPE) * (bound[1] - bound[0]) + bound[0]
            samples.append(sample.unsqueeze(-1))
        volume = 1.0
        for bound in bounds:
            volume *= (bound[1] - bound[0])
        Y = func(*samples)
        if boundaries is not None:
            weight = boundaries(*samples).to(Y.dtype)
            Y = Y * weight
        integral = volume * torch.mean(Y, dim=1).squeeze()
    return integral








