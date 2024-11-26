import matplotlib.pyplot as plt
import cv2
import numpy as np
import math


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

    cv2.imwrite('template_bouchon.png', img_bouchon)
    cv2.imwrite('template_mask_bouchon.png', img_mask_bouchon)


def processImage(image):
    template = cv2.imread('template_bouchon.png')
    mask = cv2.imread('template_mask_bouchon.png')
    # Obtenir les dimensions du modèle
    w, h = template.shape[:2]

    # Appliquer le template matching
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED, mask=mask)

    # Trouver la position du maximum de la correspondance
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(max_val)

    if max_val>0.5:
        # Dessiner un rectangle autour de la zone correspondante
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 1)

        center = (top_left[0] + w//2, top_left[1] + h//2)
        cv2.circle(image, center, 16, (0, 255, 0), 1)
        cv2.circle(image, center, 11, (0, 255, 0), 1)

    cv2.imshow('Template Matching', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#Programme

with open('listecolors.out', 'r') as file:
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

create_pattern_and_mask(32,32,22,couleurs[1],couleurs[0])
for i in range (1,7):
    image = cv2.imread(f'imabouchon{i}_rect.jpg')
    processImage(image)
