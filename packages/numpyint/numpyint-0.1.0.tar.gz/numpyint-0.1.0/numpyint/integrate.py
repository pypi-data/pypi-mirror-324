import numpy as np

GLOBAL_DTYPE=np.float32

def set_backend(dtype):
    """
    Set the default floating-point precision for cupy.

    Parameters:
        dtype (str): The desired precision, either 'float32' or 'float64'.
    """
    
    if dtype not in [np.float32, np.float64]:
        raise ValueError("dtype must be np.float32 or np.float64")
    
    global GLOBAL_DTYPE
    GLOBAL_DTYPE = dtype
    #print(f"Backend set to {dtype}.")
    
def get_data_type():
    return GLOBAL_DTYPE

# Method 1: Trapezoidal rule
def trapz_integrate(func, params, bounds, num_points, boundaries):
    """
    Compute the integral of func, using trapezoidal rule
    
    Parameters:
        func: integrand, defined by user
        params: expected to be [[1,2,3],[1,2,3],[1,2,3],...]. each row is used together within the func 
                for a single calculation. defined by user.
        bounds: expected to be like [[0,1],[0,1],[0,1],...]. defined by user
    """
    global GLOBAL_DTYPE
    if params is not None:
        ndim = len(bounds)  # determine nD integration
        vector_length = params.shape[0]  # length of parameters, for further vectorized integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = np.linspace(bound[0], bound[1], num_point, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        params_expanded = [params[:, i].reshape(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded)  # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = np.trapz(Y, grids[dim], axis=dim + 1)
            
    if params is None:
        
        ndim = len(bounds)  # determine nD integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = np.linspace(bound[0], bound[1], num_point, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        Y = func(*expanded_mesh)  # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = np.trapz(Y, grids[dim], axis=dim + 1)    
    return Y

# Method 2: Simpson rule
def simpsons_rule(y, x, axis):
    n = y.shape[axis]
    if n % 2 == 0:
        raise ValueError("Number of points must be odd for Simpson's rule.")
    dx = (x[-1] - x[0]) / (n - 1)
    coeffs = np.ones(n, dtype=y.dtype)
    coeffs[1:-1:2] = 4
    coeffs[2:-1:2] = 2
    coeffs = np.expand_dims(coeffs, axis=tuple(range(axis)) + tuple(range(axis + 1, y.ndim)))
    return np.sum(y * coeffs, axis=axis) * dx / 3

def simpson_integrate(func, params, bounds, num_points, boundaries):
    global GLOBAL_DTYPE
    if params is not None:
        ndim = len(bounds)  # determine nD integration
        vector_length = params.shape[0]  # length of parameters, for further vectorized integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = np.linspace(bound[0], bound[1], num_point, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        params_expanded = [params[:, i].reshape(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded)  # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = simpsons_rule(Y, grids[dim], axis=dim + 1)
    if params is None:
        ndim = len(bounds)  # determine nD integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = np.linspace(bound[0], bound[1], num_point, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        Y = func(*expanded_mesh)  # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = simpsons_rule(Y, grids[dim], axis=dim + 1)
    return Y    


# Method 3: Boole's Rule
def booles_rule(y, x, axis):
    n = y.shape[axis]
    if (n - 1) % 4 != 0:
        raise ValueError("Number of points minus one must be a multiple of 4 for Boole's rule.")
    dx = (x[-1] - x[0]) / (n - 1)
    coeffs = np.ones(n, dtype=y.dtype)
    coeffs[0] = 7
    coeffs[-1] = 7
    coeffs[1:-1:4] = 32
    coeffs[2:-1:4] = 12
    coeffs[3:-1:4] = 32
    coeffs[4:-1:4] = 14
    coeffs = np.expand_dims(coeffs, axis=tuple(range(axis)) + tuple(range(axis + 1, y.ndim)))
    return np.sum(y * coeffs, axis=axis) * 2 * dx / 45

def booles_integrate(func, params, bounds, num_points, boundaries):
    global GLOBAL_DTYPE
    if params is not None:
        ndim = len(bounds)  # determine nD integration
        vector_length = params.shape[0]  # length of parameters, for further vectorized integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = np.linspace(bound[0], bound[1], num_point, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        params_expanded = [params[:, i].reshape(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded)  # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = booles_rule(Y, grids[dim], axis=dim + 1)
    
    if params is None:
        ndim = len(bounds)  # determine nD integration
        grids = []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid = np.linspace(bound[0], bound[1], num_point, dtype=GLOBAL_DTYPE)
            grids.append(grid)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        Y = func(*expanded_mesh)  # unpacking
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = booles_rule(Y, grids[dim], axis=dim + 1)
    return Y



# Method 4: Gauss-Legendre rule
def gauss_legendre_rule(y, x, w, axis):
    w = np.expand_dims(w, axis=tuple(range(axis)) + tuple(range(axis + 1, y.ndim)))
    return np.sum(y * w, axis=axis)

# def gauss_legendre_nodes_weights(n):
#     global GLOBAL_DTYPE
#     nodes, weights = np.polynomial.legendre.leggauss(n)
#     nodes = nodes.astype(data_type)
#     weights = weights.astype(data_type)
#     return nodes, weights

def gauss_integrate(func, params, bounds, num_points,boundaries):
    global GLOBAL_DTYPE
    if params is not None:
        ndim = len(bounds)  # determine nD integration
        vector_length = params.shape[0]  # length of parameters, for further vectorized integration
        grids, weights = [], []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid, weight = np.polynomial.legendre.leggauss(num_point)
            grid = 0.5 * (bound[1] - bound[0]) * grid + 0.5 * (bound[1] + bound[0])
            weight = 0.5 * (bound[1] - bound[0]) * weight
            grid = grid.astype(GLOBAL_DTYPE)
            weight = weight.astype(GLOBAL_DTYPE)
            grids.append(grid)
            weights.append(weight)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        params_expanded = [params[:, i].reshape(vector_length, *([1] * ndim)) for i in range(params.shape[1])]
        Y = func(*expanded_mesh, params_expanded)
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = gauss_legendre_rule(Y, grids[dim], weights[dim], axis=dim + 1)
            
    if params is None:
        ndim = len(bounds)  # determine nD integration
        grids, weights = [], []
        for i, (bound, num_point) in enumerate(zip(bounds, num_points)):
            grid, weight = np.polynomial.legendre.leggauss(num_point)
            grid = 0.5 * (bound[1] - bound[0]) * grid + 0.5 * (bound[1] + bound[0])
            weight = 0.5 * (bound[1] - bound[0]) * weight
            grid = grid.astype(GLOBAL_DTYPE)
            weight = weight.astype(GLOBAL_DTYPE)
            grids.append(grid)
            weights.append(weight)
        mesh = np.meshgrid(*grids, indexing='ij')
        expanded_mesh = [m[np.newaxis, ...] for m in mesh]
        Y = func(*expanded_mesh)
        if boundaries is not None:
            weight = boundaries(*expanded_mesh).astype(Y.dtype)
            Y = Y * weight
        for dim in reversed(range(ndim)):
            Y = gauss_legendre_rule(Y, grids[dim], weights[dim], axis=dim + 1)
    return Y


# Method 5: Monte Carlo rule (fixed sampling points per dimension)
def mc_integrate(func, params, bounds, num_points, boundaries):
    global GLOBAL_DTYPE
    if params is not None:
        ndim = len(bounds)
        vector_length = params.shape[0]
        samples = []
        for bound in bounds:
            sample = (np.random.rand(vector_length, num_points) * (bound[1] - bound[0]) + bound[0]).astype(GLOBAL_DTYPE)
            samples.append(sample[..., np.newaxis])
        volume = 1.0
        for bound in bounds:
            volume *= (bound[1] - bound[0])
        params_expanded = [params[:, i].reshape(vector_length, 1, 1) for i in range(params.shape[1])]
        Y = func(*samples, params_expanded)
        if boundaries is not None:
            weight = boundaries(*samples).astype(Y.dtype)
            Y = Y * weight
        integral = volume * np.mean(Y, axis=1).squeeze()
        
    if params is None:
        ndim = len(bounds)
        vector_length = 1
        samples = []
        for bound in bounds:
            sample = (np.random.rand(vector_length, num_points) * (bound[1] - bound[0]) + bound[0]).astype(GLOBAL_DTYPE)
            samples.append(sample[..., np.newaxis])
        volume = 1.0
        for bound in bounds:
            volume *= (bound[1] - bound[0])
        Y = func(*samples)
        if boundaries is not None:
            weight = boundaries(*samples).astype(Y.dtype)
            Y = Y * weight
        integral = volume * np.mean(Y, axis=1).squeeze()
    return integral























