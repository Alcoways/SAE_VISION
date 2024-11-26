import cv2

def overprinting_outline_targe(image: str, pixels: list, color: tuple, thickness: int) -> None:
    image = cv2.imread(image)

    for pixel in range(len(pixels)):
        cv2.line(image, tuple(pixels[pixel]), tuple(pixels[(pixel + 1) % len(pixels)]), color, thickness)

    cv2.imwrite("outline_targe.png", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def processImage(image, srcPoints):
    pass

def read_out_file(file_path: str) -> None:
    with open(file_path, 'r') as out_file:
        print(out_file.read())

image_path = "imamire1.jpg"
pixels = [[991, 564], [655, 489], [593, 831], [949, 900]]
color = (0, 255, 0)
thickness = 1

overprinting_outline_targe(image=image_path, pixels=pixels, color=color, thickness=thickness)
read_out_file("listepoints.out")