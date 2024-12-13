import cv2
import numpy as np

def overprinting_outline_targe(image_path: str, pixels: np.array, color: tuple, thickness: int) -> None:
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image}")

    pixels = pixels.astype(np.int32)    # Convert the np array pixels to integer for the line function of cv2

    for pixel in range(len(pixels)):
        cv2.line(image, tuple(pixels[pixel]), tuple(pixels[(pixel + 1) % len(pixels)]), color, thickness)

    cv2.imwrite("src/images/generated/mire/outline_target.png", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def processImage(image_path: str, srcPoints):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image}")

    target_points  = np.array([[0, 0], [167, 0], [167, 167], [0, 167]], dtype=np.float32)
    homography, _ = cv2.findHomography(srcPoints, target_points )
    transformed_image = cv2.warpPerspective(image, homography, (168, 168))

    cv2.imwrite("src/images/generated/bouchon/transformed_image.png", transformed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_out_file(file_path: str) -> None:
    with open(file_path, 'r') as out_file:
        print(out_file.read())

image_path = "src/images/sources/mire/imamire.jpg"
pixels_mire_source = np.array([[991, 564], [655, 489], [593, 831], [949, 900]], dtype=np.float32)
color = (0, 255, 0)
thickness = 1

overprinting_outline_targe(image_path=image_path, pixels=pixels_mire_source, color=color, thickness=thickness)
processImage("src/images/sources/bouchon/imabouchon1.jpg", pixels_mire_source)
# read_out_file("listepoints.out")