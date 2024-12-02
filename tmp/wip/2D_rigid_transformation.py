import matplotlib.pyplot as plt
import numpy as np

A = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
B = np.array([[1, 1], [2, 1], [2, 2], [1, 2]])
# B = np.array([[2, 2], [2.75, 2.5], [2.5, 3.25], [1.75, 2.75]])

centroid_A = np.mean(A, axis=0)
centroid_B = np.mean(B, axis=0)

A_centered = A - centroid_A
B_centered = B - centroid_B

u = A_centered[1] - A_centered[0]
v = B_centered[1] - B_centered[0]

cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
sin_theta = np.cross(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
theta = np.arctan2(sin_theta, cos_theta)

R = np.array([[cos_theta, -sin_theta],
              [sin_theta, cos_theta]])

t = centroid_B - np.dot(R, centroid_A)

A_transformed = np.dot(A, R.T) + t

print("A transformé :\n", A_transformed)
print("B attendu :\n", B)

plt.scatter(A[:, 0], A[:, 1], color='blue', label='A (original)')
plt.scatter(B[:, 0], B[:, 1], color='green', label='B (cible)')
plt.scatter(A_transformed[:, 0], A_transformed[:, 1], color='red', label='A (transformé)', marker='+')

plt.legend()
plt.axis('equal')
plt.title("Visualisation de la transformation rigide 2D")
plt.show()
