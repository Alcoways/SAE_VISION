from src.cap_recognization_methods import *
from src.utils import *

import numpy as np

""" A = np.array([[0, 0], [1, 0]])
B = np.array([[1, 1], [2, 1]])

estimator = RigidTransform2DEstimator(A[0], A[1], B[0], B[1])
theta, translation_x, translation_y = estimator.estimate()
print(f"theta: {theta} \ntranslation_x: {translation_x} \ntranslation_y: {translation_y}") """

""" generator = TestPointGenerator()
test_data = generator.generate_test_data()

print(f"theta: {test_data['theta']} \n tx: {test_data['tx']} \n ty: {test_data['ty']}")
print(f"p1_a: {test_data['p1_a']}, p2_a: {test_data['p2_a']}")
print(f"p1_b: {test_data['p1_b']}, p2_b: {test_data['p2_b']}")

image_path = "res/images/sources/mire/imamire.jpg"
pixels_mire_source = np.array([[991, 564], [655, 489], [593, 831], [949, 900]], dtype=np.float32)
color = (0, 255, 0)
thickness = 1
output_path = "res/images/generated/mire/outline_target.png"

drawer = ImageOutlineDrawer(image_path, pixels_mire_source, color, thickness)
drawer.process(output_path) 

image_path = "res/images/sources/bouchon/imabouchon1.jpg"
pixels_mire_source = np.array([[991, 564], [655, 489], [593, 831], [949, 900]], dtype=np.float32)
output_path = "res/images/generated/bouchon/transformed_image.png"

transformer = ImageTransformer(image_path, pixels_mire_source)
transformer.process(output_path) """

if __name__ == "name":

    print("Choose method type: \n 1: Pattern and mask \n 2: Concentric circles \n 3: Concentric ellipses")
    method = int(input())

    match method:
        case 1:
            # Pattern and mask method
            pass
        case 2:
            # Concentric circles method
            image_path = "res/images/sources/bouchon/imabouchon1.jpg"
            output_path = "res/images/generated/circles/concentric_circles_detected.png"

            detector = ConcentricCirclesDetector(image_path)
            detector.process(output_path)
        case 3:
            # Concentric ellipses method
            image_path = "res/images/sources/bouchon/imabouchon1.jpg"
            output_path = "res/images/generated/ellipses/concentric_ellipses.png"

            detector = ConcentricEllipsesDetector(image_path)
            detector.process(output_path)


