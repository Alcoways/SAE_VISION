from src.cap_recognization_methods import *

import subprocess

if __name__ == "__main__":

    print("Choose method type: \n 1: Pattern and mask \n 2: Concentric circles \n 3: Concentric ellipses")
    method = int(input())

    match method:
        case 1:
            # Pattern and mask method
            subprocess.run(["python", "src/method_1.py"])
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