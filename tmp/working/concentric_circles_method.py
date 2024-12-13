import cv2
import numpy as np

def detect_concentric_circles(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Impossible de charger l'image depuis le chemin spécifié.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    circles = []

    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)

        area_contour = cv2.contourArea(contour)
        if area_contour == 0:
            continue

        circularity = (4 * np.pi * area_contour) / (2 * np.pi * radius)**2
        if 0.8 <= circularity <= 1.2:
            circles.append((int(x), int(y), int(radius)))

    for i, (x1, y1, r1) in enumerate(circles):
        for j, (x2, y2, r2) in enumerate(circles[i + 1:], start=i + 1):
            if abs(x1 - x2) < 5 and abs(y1 - y2) < 5 and abs(r1 - r2) > 5:
                cv2.circle(image, (x1, y1), r1, (0, 255, 0), 2)
                cv2.circle(image, (x2, y2), r2, (255, 0, 0), 2)

                cv2.drawMarker(image, (x1, y1), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)

                print(f"Cercles concentriques détectés au centre ({x1}, {y1}) avec rayons {r1} et {r2}.")

    cv2.imshow("Concentric Circles Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image_path = "res/images/sources/bouchon/imabouchon1.jpg"
detect_concentric_circles(image_path)