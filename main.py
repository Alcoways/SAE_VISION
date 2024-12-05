import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
import os
import random

##################################
""" executableopenscad="D:\OpenSCAD-2021.01-x86-64\openscad-2021.01\openscad.exe"
d1=10
d2=5
l_table=1000
l_mire=70
l_coin=2
mire=1
u=random.randint(-l_mire//2+d1//2,l_mire//2-d1//2)
v=random.randint(-l_mire//2+d1//2,l_mire//2-d1//2)
c1="[160/255,119/255,109/255]"
c2="[249/255,58/255,58/255]"
chaine=f'" {executableopenscad}" -D d1={d1} -D d2={d2} -D u={u} -D v={v} -D l_table={l_table} -D c1={c1} -D c2={c2} -D l_coin={l_coin} -D l_mire={l_mire} -D mire={mire} --camera 13,-12,18,45.2,0,355.4,292 -o image1.png ../Openscad/BouchonMire.scad'
os.system(chaine)
print("openscad")
exit() """
##################################

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
    cv2.line(image,(u-5,v),(u+5,v),(0,255,0),1)
    cv2.line(image,(u,v-5),(u,v+5),(0,255,0),1)

def processImage(image: str, srcPoints):

    if image is None:
        raise FileNotFoundError(f"Impossible de charger l'image : {image_path}")

    target_points  = np.array([[0, 0], [167, 0], [167, 167], [0, 167]], dtype=np.float32)
    homography, _ = cv2.findHomography(srcPoints, target_points )
    transformed_image = cv2.warpPerspective(image, homography, (168, 168))

    cv2.imwrite("transformed_image.png", transformed_image)
    
    template = cv2.imread('src/images/template/template_bouchon.png')
    mask = cv2.imread('src/images/template/template_mask_bouchon.png')
    # Obtenir les dimensions du modèle
    w, h,  = template.shape[:2]

    # Appliquer le template matching
    result = cv2.matchTemplate(transformed_image, template, cv2.TM_CCOEFF_NORMED, mask=mask)

    # Trouver la position du maximum de la correspondance
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(max_val)

    if max_val>0.5:
        # Dessiner un rectangle autour de la zone correspondante
        top_left = max_loc
        top_right = (top_left[0] + w, top_left[1])
        bottom_left = (top_left[0] , top_left[1] + h)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 1)

        center = (top_left[0] + w//2, top_left[1] + h//2)
        # cv2.circle(transformed_image, center, 16, (0, 255, 0), 1)
        # cv2.circle(transformed_image, center, 11, (0, 255, 0), 1)
        drawcross(transformed_image,top_left[0],top_left[1])
        drawcross(transformed_image,bottom_right[0],bottom_right[1])
        drawcross(transformed_image,top_right[0],top_right[1])
        drawcross(transformed_image,bottom_left[0],bottom_left[1])
        cv2.line(transformed_image,top_left,top_right,(255,0,0),1)
        cv2.line(transformed_image,top_left,bottom_left,(255,0,0),1)
        cv2.line(transformed_image,top_right,bottom_right,(255,0,0),1)
        cv2.line(transformed_image,bottom_left,bottom_right,(255,0,0),1)
        drawcross(transformed_image,center[0],center[1])

    cv2.imshow('Template Matching', transformed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#Programme

with open('src/data/listecolors.out', 'r') as file:
    # Créer une liste pour stocker les données
    couleurs = []
    
    # Lire chaque ligne du fichier
    for line in file:
        # Supprimer les espaces ou caractères superflus et diviser la ligne par les virgules
        values = line.strip().split(',')
        
        # Convertir les valeurs en float (elles semblent être des nombres à virgule flottante)
        values = tuple(int(float(value.strip())) for value in values)
        
        # Ajouter les valeurs extraites à la liste data
        couleurs.append(values)

with open('src/data/listepoints.out', 'r') as file:
    points = []
    
    # Lire chaque ligne du fichier
    for line in file:
        # Supprimer les espaces et couper la ligne à la virgule
        coordinates = line.strip().split(',')
        
        # Convertir les coordonnées en float et les ajouter à la liste points
        x = float(coordinates[0].strip())
        y = float(coordinates[1].strip())
        points.append((x, y))

# Afficher la liste des points
print(points)

theta, translation_x, translation_y = estimate_rigid_transform(points[0],points[1],points[2],points[3])
print(f"theta: {theta} \n translation_x: {translation_x} \n translation_y: {translation_y}" )

create_pattern_and_mask(32,32,22,couleurs[1],couleurs[0])
pixels_mire_source = np.array([[991, 564], [655, 489], [593, 831], [949, 900]], dtype=np.float32)
image = cv2.imread("src/images/bouchon/imabouchon1.jpg")
processImage(image, pixels_mire_source)
