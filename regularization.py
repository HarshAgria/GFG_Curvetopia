import numpy as np
from scipy.spatial import distance, ConvexHull
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression, RANSACRegressor

def detect_line(XY, tolerance=5):
    if len(XY) < 2:
        return False
    model = LinearRegression().fit(XY[:, 0].reshape(-1, 1), XY[:, 1])
    predicted = model.predict(XY[:, 0].reshape(-1, 1))
    return np.allclose(predicted, XY[:, 1], atol=tolerance)

def detect_circle(XY, tolerance=5):
    if len(XY) < 5:
        return False
    
    centroid = np.mean(XY, axis=0)
    distances = np.linalg.norm(XY - centroid, axis=1)
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)
    
    if std_distance / mean_distance < (tolerance / 100.0):
        return True
    
    return False

def detect_ellipse(XY, tolerance=2, angle_threshold=45, eigenvalue_ratio_threshold=0.2):
    if len(XY) < 5:
        return False
    
    centroid = np.mean(XY, axis=0)
    centered_XY = XY - centroid
    
    cov_matrix = np.cov(centered_XY, rowvar=False)
    
    eigenvalues, _ = np.linalg.eigh(cov_matrix)
    
    eigenvalue_ratio = eigenvalues[0] / eigenvalues[1]
    
    if eigenvalue_ratio < eigenvalue_ratio_threshold:
        return False
    
    distances = np.linalg.norm(XY - centroid, axis=1)
    
    mean_distance = np.mean(distances)
    std_distance = np.std(distances)
    
    if std_distance / mean_distance < (tolerance / 100.0):
        angles = []
        for i in range(len(XY)):
            v1 = XY[i] - XY[i - 1]
            v2 = XY[(i + 1) % len(XY)] - XY[i]
            angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1.0, 1.0)))
            angles.append(angle)
        
        if np.all(np.array(angles) > angle_threshold):  # Ensures no sharp angles
            return True
    
    return False

def detect_rectangle(XY, angle_tolerance=5, side_tolerance=5):
    if len(XY) != 4:
        return False

    side_lengths = [distance.euclidean(XY[i], XY[(i+1) % 4]) for i in range(4)]
    diagonals = [distance.euclidean(XY[i], XY[(i+2) % 4]) for i in range(2)]

    if not (np.allclose(side_lengths[:2], side_lengths[2:], atol=side_tolerance) and
            np.allclose(diagonals[0], diagonals[1], atol=side_tolerance)):
        return False
    
    angles = []
    for i in range(4):
        v1 = XY[i] - XY[i - 1]
        v2 = XY[(i + 1) % 4] - XY[i]
        
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return False
        
        angle = np.arccos(np.clip(np.dot(v1, v2) / (norm_v1 * norm_v2), -1.0, 1.0))
        angles.append(np.degrees(angle))

    # print(f"Angles: {angles}")
    
    return np.allclose(angles, 90, atol=angle_tolerance)

def detect_rounded_rectangle(XY, side_tolerance=5, aspect_ratio_tolerance=0.5):
    if len(XY) < 8:
        return False

    hull = ConvexHull(XY)
    hull_points = XY[hull.vertices]
    
    if len(hull_points) < 4:
        return False

    side_lengths = [distance.euclidean(hull_points[i], hull_points[(i + 1) % len(hull_points)]) for i in range(len(hull_points))]

    if len(side_lengths) >= 4:
        if not (np.allclose(side_lengths[0], side_lengths[2], atol=side_tolerance) and
                np.allclose(side_lengths[1], side_lengths[3], atol=side_tolerance)):
            return False
    else:
        return False
    
    width = max(hull_points[:, 0]) - min(hull_points[:, 0])
    height = max(hull_points[:, 1]) - min(hull_points[:, 1])
    aspect_ratio = width / height if height > 0 else 0

    if not (1 - aspect_ratio_tolerance < aspect_ratio < 1 + aspect_ratio_tolerance):
        return False
    
    return True

def detect_polygon(XY, num_sides):
    if len(XY) < num_sides:
        return False
    hull = ConvexHull(XY)
    if len(hull.vertices) != num_sides:
        return False
    distances = [distance.euclidean(XY[hull.vertices[i]], XY[hull.vertices[(i+1) % num_sides]]) for i in range(num_sides)]
    return np.allclose(distances, np.mean(distances), atol=1e-2)

def detect_star_shape(XY, distance_tolerance=15, angle_tolerance=10):
    if len(XY) < 10:
        return False
    
    centroid = np.mean(XY, axis=0)
    
    angles = np.arctan2(XY[:, 1] - centroid[1], XY[:, 0] - centroid[0])
    sorted_indices = np.argsort(angles)
    XY_sorted = XY[sorted_indices]
    
    distances_from_centroid = np.linalg.norm(XY_sorted - centroid, axis=1)
    
    peaks = (distances_from_centroid[1:-1] > distances_from_centroid[:-2]) & \
            (distances_from_centroid[1:-1] > distances_from_centroid[2:])
    valleys = (distances_from_centroid[1:-1] < distances_from_centroid[:-2]) & \
              (distances_from_centroid[1:-1] < distances_from_centroid[2:])
    
    peaks = np.r_[False, peaks, False]
    valleys = np.r_[False, valleys, False]
    
    if not (np.sum(peaks) == np.sum(valleys) and np.sum(peaks) == 5):
        return False

    sharp_angles = []
    for i in range(len(XY_sorted)):
        prev_point = XY_sorted[i - 1]
        current_point = XY_sorted[i]
        next_point = XY_sorted[(i + 1) % len(XY_sorted)]
        
        v1 = prev_point - current_point
        v2 = next_point - current_point
        
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            continue
        
        angle = np.degrees(np.arccos(np.clip(np.dot(v1, v2) / (norm_v1 * norm_v2), -1.0, 1.0)))
        sharp_angles.append(angle)
    
    sharp_angles = np.array(sharp_angles)
    if np.sum(sharp_angles < (90 - angle_tolerance)) >= 5:
        return True
    
    return False

def detect_parabola(XY, tolerance=6.5, ransac_tolerance=2):
    if len(XY) < 3:
        return False
    
    X = XY[:, 0].reshape(-1, 1)
    y = XY[:, 1]
    
    ransac_model = make_pipeline(PolynomialFeatures(degree=2), RANSACRegressor(residual_threshold=ransac_tolerance))
    ransac_model.fit(X, y)
    
    y_pred_ransac = ransac_model.predict(X)
    
    residuals_ransac = np.abs(y - y_pred_ransac)
    
    ransac_coeff = ransac_model.named_steps['ransacregressor'].estimator_.coef_
    if ransac_coeff[2] == 0:
        return False
    
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    linear_model = LinearRegression().fit(X_poly, y)
    y_pred_linear = linear_model.predict(X_poly)
    
    residuals_linear = np.abs(y - y_pred_linear)
    
    median_residual = np.median(residuals_linear)
    adjusted_tolerance = tolerance * median_residual
    
    if np.all(residuals_linear < adjusted_tolerance):
        first_derivative = np.gradient(y_pred_linear, X[:, 0])
        second_derivative = np.gradient(first_derivative, X[:, 0])
        
        if np.all(second_derivative > 0) or np.all(second_derivative < 0):
            curvature_variation = np.max(second_derivative) - np.min(second_derivative)
            if curvature_variation < (tolerance * 0.1):
                return True
    
    return False
