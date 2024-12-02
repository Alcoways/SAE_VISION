import cv2
import numpy as np

image = cv2.imread("imabouchon1.jpg")

points_source = np.array([[991, 564], [655, 489], [593, 831], [949, 900]], dtype=np.float32)
# points_cibles = np.array([[167, 0], [0, 0], [0, 167], [167, 167]], dtype=np.float32) # Pour le rapport
points_cibles = np.array([[0, 0], [167, 0], [167, 167], [0, 167]], dtype=np.float32)

homography, _ = cv2.findHomography(points_source, points_cibles)

image_transforme = cv2.warpPerspective(image, homography, (168, 168))

cv2.imwrite("homo.png", image_transforme)
cv2.waitKey(0)
cv2.destroyAllWindows()