import numpy as np
import matplotlib.pyplot as plt

def detect_symmetry(XY, tolerance=1e-2):
    centroid = np.mean(XY, axis=0)
    
    mirrored_XY = np.copy(XY)
    mirrored_XY[:, 0] = 2 * centroid[0] - mirrored_XY[:, 0]
    
    distances = np.linalg.norm(XY - mirrored_XY, axis=1)
    
    is_symmetric = np.all(distances < tolerance)
    
    if is_symmetric:
        plt.plot(mirrored_XY[:, 0], mirrored_XY[:, 1], 'g--', label='Mirrored')
        plt.plot(XY[:, 0], XY[:, 1], 'b-', label='Original')
        plt.title('Symmetry Detected')
        plt.legend()
        plt.show()
        return True, XY
    else:
        return False, None

def detect_rotational_symmetry(XY, angle=180, tolerance=1e-2):
    centroid = np.mean(XY, axis=0)
    
    angle_rad = np.deg2rad(angle)
    
    rotation_matrix = np.array([[np.cos(angle_rad), -np.sin(angle_rad)],
                                [np.sin(angle_rad),  np.cos(angle_rad)]])
    
    rotated_XY = (XY - centroid) @ rotation_matrix.T + centroid
    
    distances = np.linalg.norm(XY - rotated_XY, axis=1)
    
    is_symmetric = np.all(distances < tolerance)
    
    if is_symmetric:
        plt.plot(rotated_XY[:, 0], rotated_XY[:, 1], 'r--', label='Rotated')
        plt.plot(XY[:, 0], XY[:, 1], 'b-', label='Original')
        plt.title('Rotational Symmetry Detected')
        plt.legend()
        plt.show()
        return True, XY
    else:
        return False, None
