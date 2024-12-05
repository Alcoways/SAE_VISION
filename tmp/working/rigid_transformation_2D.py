import numpy as np

def estimate_rigid_transform(p1_a, p2_a, p1_b, p2_b):
    v_a = np.array([p2_a[0] - p1_a[0], p2_a[1] - p1_a[1]])
    v_b = np.array([p2_b[0] - p1_b[0], p2_b[1] - p1_b[1]])

    norm_v_a = np.linalg.norm(v_a)
    norm_v_b = np.linalg.norm(v_b)

    cos_theta = np.dot(v_a, v_b) / (norm_v_a * norm_v_b)
    sin_theta = (v_a[0] * v_b[1] - v_a[1] * v_b[0]) / (norm_v_a * norm_v_b)
    theta = np.arctan2(sin_theta, cos_theta)

    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

    translation = np.array(p1_b) - np.dot(rotation_matrix, np.array(p1_a))

    return theta, translation[0], translation[1]