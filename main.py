import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
import os
import random
import subprocess

def generer_openscad(d1,d2,mire,l_mire):
    
    #chemin d'accès à openscad à modifier
    executableopenscad="/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD"

    l_table=100
    u=random.uniform((l_table-l_mire)/2+d1/2,(l_table-l_mire)/2+l_mire-d1/2)
    v=random.uniform((l_table-l_mire)/2+d1/2,(l_table-l_mire)/2+l_mire-d1/2)
    print("U: ", u, "V: ", v)

    c1="[109/255,119/255,160/255]"
    c2="[249/255,58/255,58/255]"
    chemin_scad = "./Openscad/BouchonMire2.scad"

    # Liste de commandes et paramètres
    commande = [
        executableopenscad,
        "-D", f"d1={d1}",
        "-D", f"d2={d2}",
        "-D", f"u={u}",
        "-D", f"v={v}",
        "-D", f"c1={c1}",
        "-D", f"c2={c2}",
        "-D", f"l_mire={l_mire}",
        "-D", f"mire={mire}",
        "--camera", "58,30,12,40,0,16,246",
        "--imgsize", "1920,1080",
        "-o", "imabouchon_openscad.png",
        chemin_scad 
    ]
    print("Commande générée :", " ".join(commande))
    subprocess.run(commande)
    print("")



def estimate_rigid_transform(p1_a, p2_a, p1_b, p2_b):
    v_a = np.array([p2_a[0] - p1_a[0], p2_a[1] - p1_a[1]])
    v_b = np.array([p2_b[0] - p1_b[0], p2_b[1] - p1_b[1]])

    norm_v_a = np.linalg.norm(v_a)
    norm_v_b = np.linalg.norm(v_b)

    cos_theta = np.dot(v_a, v_b) / (norm_v_a * norm_v_b)
    sin_theta = (v_a[0] * v_b[1] - v_a[1] * v_b[0]) / (norm_v_a * norm_v_b)
    theta = np.arctan2(sin_theta, cos_theta)

    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

    translation = np.array(p1_b) - np.dot(rotation_matrix, np.array(p1_a))

    return theta, translation[0], translation[1]



def create_pattern_and_mask(width, d1, d2, bgr_color_center, bgr_color_contour):

    centre_cercle=(width/2,width/2)

    img_bouchon = np.zeros((width, width, 3), dtype=np.uint8)
    img_mask_bouchon = np.zeros((width, width, 3), dtype=np.uint8)
    for u in range (width):
        for v in range (width):
            dist_pix_centre = math.sqrt((centre_cercle[0]-u-0.5)**2+(centre_cercle[1]-v-0.5)**2)
            if dist_pix_centre<d2//2:
                img_bouchon[u,v] = (bgr_color_center)
                img_mask_bouchon[u,v] = (255,255,255)
            elif dist_pix_centre<d1//2:
                img_bouchon[u,v] = (bgr_color_contour) 
                img_mask_bouchon[u,v] = (255,255,255)

    cv2.imwrite('src/images/template/template_bouchon.png', img_bouchon)
    cv2.imwrite('src/images/template/template_mask_bouchon.png', img_mask_bouchon)



def drawcross(image,u,v):
    cv2.line(image,(u-5,v),(u+5,v),(255,0,0),1)
    cv2.line(image,(u,v-5),(u,v+5),(255,0,0),1)



def processImage(image: str, srcPoints):
    if image is None:
        raise FileNotFoundError(f"Impossible de charger l'image : {image_path}")

    target_points  = np.array([[0, 0], [167, 0], [167, 167], [0, 167]], dtype=np.float32)
    homography, _ = cv2.findHomography(srcPoints, target_points )
    transformed_image = cv2.warpPerspective(image, homography, (168, 168))

    # transformed_image = cv2.imread("src/images/bouchon/imabouchon2_rect.jpg")

    template = cv2.imread('src/images/template/template_bouchon.png')
    mask = cv2.imread('src/images/template/template_mask_bouchon.png')
    w, h,  = template.shape[:2]
    result = cv2.matchTemplate(transformed_image, template, cv2.TM_CCORR_NORMED , mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print("Max_val: ", max_val)
    print("")

    if max_val>0.92:
        top_left = max_loc
        center = (top_left[0] + w//2 , top_left[1] + h//2)
        cv2.circle(transformed_image, center, 16, (0, 0, 255), 1)
        cv2.circle(transformed_image, center, 11, (0, 255, 0), 1)
        drawcross(transformed_image,center[0],center[1])
    else:
        center = None

    cv2.imwrite("imabouchon_openscad_rect_detection.png", transformed_image)
    # cv2.imshow('Template Matching', transformed_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return center



def afficher_coordonées(bouchon_mire):
    if bouchon_mire!=None:
        print("Le bouchon se trouve au coordonées x=", bouchon_mire[0], ", y=", bouchon_mire[1], " dans le repere mire.")
        bouchon_mire = (80,80)
        bouchon_robot = appliquer_transformatio_rigide(bouchon_mire, theta, translation_x, translation_y)
        print("Le bouchon se trouve au coordonées x=", bouchon_robot[0], ", y=", bouchon_robot[1], " dans le repere robot.")
    else:
        print("Pas de bouchon detecté sur cette image")
    print("")

def appliquer_transformatio_rigide(pMire, theta, tx, ty):
    pMire_x, pMire_y = pMire
    pRobot_x = math.cos(math.radians(theta)) * pMire_x - math.sin(math.radians(theta)) * pMire_y + tx
    pRobot_y = math.cos(math.radians(theta)) * pMire_x - math.sin(math.radians(theta)) * pMire_y + ty
    return pRobot_x, pRobot_y



#Programme Principal

d1=15
d2=10
l_mire=80
mire=0
generer_openscad(d1,d2,mire,l_mire)

with open('src/data/listecolors.out', 'r') as file:
    couleurs = []
    for line in file:
        values = line.strip().split(',')
        values = tuple(int(float(value.strip())) for value in values)
        couleurs.append(values)

#Choix de points correspondants dans le repere mire et robot 
points = [(0,0), (80, 80), (345,526), (425,446)]

print("P1 repère mire: ", points[0], "P2 repère mire: ", points[1], "\nP1  repère robot: ", points[2], "P2 repère robot: ", points[3])
print("")

theta, translation_x, translation_y = estimate_rigid_transform(points[0],points[1],points[2],points[3])

print(f"Theta: {theta} \nTranslation_x: {translation_x} \nTranslation_y: {translation_y}" )
print("")

create_pattern_and_mask(32,32,22,couleurs[1],couleurs[0])

#COORDONEES COIN MIRE EXEMPLE INETDOC
# pixels_mire_source = np.array([[991, 564], [655, 489], [593, 831], [949, 900]], dtype=np.float32)
# image = cv2.imread("src/images/bouchon/imabouchon1.jpg")

#COORDONEES COIN MIRE EXEMPLE OPENSCAD
pixels_mire_source = np.array([[1409,245], [691, 106], [399,659], [1250,860]], dtype=np.float32)
image = cv2.imread("imabouchon_openscad.png")


bouchon_mire = processImage(image, pixels_mire_source)
afficher_coordonées(bouchon_mire)
