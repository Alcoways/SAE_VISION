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
class ConcentricEllipsesDetector:
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = None
        self.gray = None
        self.ellipses = []
        self.concentric_ellipses = []

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise FileNotFoundError(f"Image non trouvée : {self.image_path}")

    def preprocess_image(self):
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        return edges

    def detect_contours(self, edges):
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if len(contour) >= 5:
                ellipse = cv2.fitEllipse(contour)
                self.ellipses.append(ellipse)

    def find_concentric_ellipses(self):
        for i, ellipse1 in enumerate(self.ellipses):
            for j, ellipse2 in enumerate(self.ellipses):
                if i >= j:
                    continue

                (x1, y1), (major1, minor1), angle1 = ellipse1
                (x2, y2), (major2, minor2), angle2 = ellipse2

                center_distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                if center_distance > 0.1:
                    continue

                ratio_major = max(major1, major2) / min(major1, major2)
                ratio_minor = max(minor1, minor2) / min(minor1, minor2)
                if ratio_major > 1.2 or ratio_minor > 1.2:
                    continue

                if abs(angle1 - angle2) > 10:
                    continue

                self.concentric_ellipses.append((ellipse1, ellipse2))

    def draw_and_save_result(self, output_path: str):
        for ellipse1, ellipse2 in self.concentric_ellipses:
            cv2.ellipse(self.image, ellipse1, (0, 255, 0), 2)
            cv2.ellipse(self.image, ellipse2, (255, 0, 0), 2)
        cv2.imwrite(output_path, self.image)

    def process(self, output_path: str):
        self.load_image()
        edges = self.preprocess_image()
        self.detect_contours(edges)
        self.find_concentric_ellipses()
        self.draw_and_save_result(output_path)