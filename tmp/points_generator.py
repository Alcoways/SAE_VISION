import math
import numpy as np
import random

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


xa, ya = random.randint(0, 20), random.randint(0, 20)
p1_a = (xa, ya)

xb, yb = random.randint(0, 20), random.randint(0, 20)
p2_a = (xb, yb)

theta = random.uniform(0, math.pi)
tx = random.randint(0, 20)
ty = random.randint(0, 20)

print(f"theta: {theta} \n tx: {tx} \n ty: {ty}")

mean = 0.001
std_dev = 0.1

p1_b = (
    xa * math.cos(theta) - ya * math.sin(theta) + tx + random.gauss(mean, std_dev),
    xa * math.sin(theta) + ya * math.cos(theta) + ty + random.gauss(mean, std_dev)
)
p2_b = (
    xb * math.cos(theta) - yb * math.sin(theta) + tx + random.gauss(mean, std_dev),
    xb * math.sin(theta) + yb * math.cos(theta) + ty + random.gauss(mean, std_dev)
)

print(f"p1_a: {p1_a}, p2_a: {p2_a}")
print(f"p1_b: {p1_b}, p2_b: {p2_b}")

# Calcul de la transformation
theta, translation_x, translation_y = estimate_rigid_transform(p1_a, p2_a, p1_b, p2_b)
print(f"theta: {theta} \n translation_x: {translation_x} \n translation_y: {translation_y}")
