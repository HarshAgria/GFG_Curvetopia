import numpy as np
from scipy.interpolate import splprep, splev

def complete_curve(XY, num_points=100, smoothness=0):
    XY = np.asarray(XY)
    
    if XY.ndim != 2 or XY.shape[1] != 2:
        raise ValueError("Input XY must be a 2D array or a list of coordinate pairs (x, y).")
    
    distances = np.sqrt(np.sum(np.diff(XY, axis=0)**2, axis=1))
    t = np.concatenate(([0], np.cumsum(distances)))
    t /= t[-1]

    tck, u = splprep(XY.T, u=t, s=smoothness, k=3)
    
    u_new = np.linspace(u.min(), u.max(), num_points)
    x_new, y_new = splev(u_new, tck, der=0)
    
    return np.vstack((x_new, y_new)).T

def complete_curves(paths_XYs, num_points=100, smoothness=0):
    completed_curves = []
    for path in paths_XYs:
        for XY in path:
            completed_curve = complete_curve(XY, num_points=num_points, smoothness=smoothness)
            completed_curves.append(completed_curve)
    return completed_curves
