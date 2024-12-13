import cv2
import math
import numpy as np
import random

class ImageOutlineDrawer:
    def __init__(self, image_path: str, pixels: np.array, color: tuple, thickness: int) -> None:
        self.image_path = image_path
        self.pixels = pixels.astype(np.int32)
        self.color = color
        self.thickness = thickness
        self.image = None

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise FileNotFoundError(f"Image not found at path: {self.image_path}")

    def draw_outline(self):
        for pixel in range(len(self.pixels)):
            cv2.line(
                self.image,
                tuple(self.pixels[pixel]),
                tuple(self.pixels[(pixel + 1) % len(self.pixels)]),
                self.color,
                self.thickness
            )

    def save_image(self, output_path: str):
        cv2.imwrite(output_path, self.image)

    def process(self, output_path: str):
        self.load_image()
        self.draw_outline()
        self.save_image(output_path)


class ImageTransformer:
    def __init__(self, image_path: str, src_points: np.array):
        self.image_path = image_path
        self.src_points = src_points.astype(np.float32)
        self.target_points = np.array([[0, 0], [167, 0], [167, 167], [0, 167]], dtype=np.float32)
        self.image = None
        self.transformed_image = None

    def load_image(self):
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise FileNotFoundError(f"Image not found at path: {self.image_path}")

    def compute_homography(self):
        self.homography, _ = cv2.findHomography(self.src_points, self.target_points)

    def apply_transformation(self):
        self.transformed_image = cv2.warpPerspective(self.image, self.homography, (168, 168))

    def save_transformed_image(self, output_path: str):
        cv2.imwrite(output_path, self.transformed_image)

    def process(self, output_path: str):
        self.load_image()
        self.compute_homography()
        self.apply_transformation()
        self.save_transformed_image(output_path)


class RigidTransform2DEstimator:
    def __init__(self, p1_a, p2_a, p1_b, p2_b):
        self.p1_a = np.array(p1_a)
        self.p2_a = np.array(p2_a)
        self.p1_b = np.array(p1_b)
        self.p2_b = np.array(p2_b)
        self.theta = None
        self.translation_x = None
        self.translation_y = None

    def compute_vectors(self):
        self.v_a = self.p2_a - self.p1_a
        self.v_b = self.p2_b - self.p1_b

    def compute_rotation(self):
        norm_v_a = np.linalg.norm(self.v_a)
        norm_v_b = np.linalg.norm(self.v_b)

        cos_theta = np.dot(self.v_a, self.v_b) / (norm_v_a * norm_v_b)
        sin_theta = (self.v_a[0] * self.v_b[1] - self.v_a[1] * self.v_b[0]) / (norm_v_a * norm_v_b)
        self.theta = np.arctan2(sin_theta, cos_theta)

    def compute_translation(self):
        rotation_matrix = np.array([
            [np.cos(self.theta), -np.sin(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)]
        ])
        translation = self.p1_b - np.dot(rotation_matrix, self.p1_a)
        self.translation_x, self.translation_y = translation

    def estimate(self):
        self.compute_vectors()
        self.compute_rotation()
        self.compute_translation()
        return self.theta, self.translation_x, self.translation_y


class TestPointGenerator:
    def __init__(self, mean=0.001, std_dev=0.1):
        self.mean = mean
        self.std_dev = std_dev
        self.theta = None
        self.tx = None
        self.ty = None
        self.p1_a = None
        self.p2_a = None
        self.p1_b = None
        self.p2_b = None

    def generate_points(self):
        xa, ya = random.randint(0, 20), random.randint(0, 20)
        xb, yb = random.randint(0, 20), random.randint(0, 20)
        self.p1_a = (xa, ya)
        self.p2_a = (xb, yb)

    def generate_transform(self):
        self.theta = random.uniform(0, math.pi)
        self.tx = random.randint(0, 20)
        self.ty = random.randint(0, 20)

    def apply_transform(self):
        xa, ya = self.p1_a
        xb, yb = self.p2_a

        self.p1_b = (
            xa * math.cos(self.theta) - ya * math.sin(self.theta) + self.tx + random.gauss(self.mean, self.std_dev),
            xa * math.sin(self.theta) + ya * math.cos(self.theta) + self.ty + random.gauss(self.mean, self.std_dev)
        )
        self.p2_b = (
            xb * math.cos(self.theta) - yb * math.sin(self.theta) + self.tx + random.gauss(self.mean, self.std_dev),
            xb * math.sin(self.theta) + yb * math.cos(self.theta) + self.ty + random.gauss(self.mean, self.std_dev)
        )

    def generate_test_data(self):
        self.generate_points()
        self.generate_transform()
        self.apply_transform()
        return {
            "theta": self.theta,
            "tx": self.tx,
            "ty": self.ty,
            "p1_a": self.p1_a,
            "p2_a": self.p2_a,
            "p1_b": self.p1_b,
            "p2_b": self.p2_b
        }