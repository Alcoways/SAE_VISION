import cv2
import numpy as np

# Method 1

# Method 2
class ConcentricCirclesDetector:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.circles = []

    def load_image(self):
        self.image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        if self.image is None:
            raise ValueError("Impossible de charger l'image depuis le chemin spécifié.")

    def preprocess_image(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(self.gray, (9, 9), 2)
        edges = cv2.Canny(blurred, 50, 150)
        return edges

    def detect_contours(self, edges):
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x, y), radius = cv2.minEnclosingCircle(contour)
            area_contour = cv2.contourArea(contour)
            if area_contour == 0:
                continue
            circularity = (4 * np.pi * area_contour) / (2 * np.pi * radius)**2
            if 0.8 <= circularity <= 1.2:
                self.circles.append((int(x), int(y), int(radius)))

    def detect_concentric_circles(self):
        for i, (x1, y1, r1) in enumerate(self.circles):
            for j, (x2, y2, r2) in enumerate(self.circles[i + 1:], start=i + 1):
                if abs(x1 - x2) < 5 and abs(y1 - y2) < 5 and abs(r1 - r2) > 5:
                    cv2.circle(self.image, (x1, y1), r1, (0, 255, 0), 2)
                    cv2.circle(self.image, (x2, y2), r2, (255, 0, 0), 2)
                    cv2.drawMarker(self.image, (x1, y1), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
                    print(f"Cercles concentriques détectés au centre ({x1}, {y1}) avec rayons {r1} et {r2}.")

    def show_result(self):
        cv2.imshow("Concentric Circles Detection", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def process(self):
        self.load_image()
        edges = self.preprocess_image()
        self.detect_contours(edges)
        self.detect_concentric_circles()
        self.show_result()


# Method 3