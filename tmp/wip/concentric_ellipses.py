import cv2
import numpy as np

# Charger l'image
image = cv2.imread("res/images/sources/bouchon/imabouchon1.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Prétraitement
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

# Détection des contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Détection d'ellipses
ellipses = []
for contour in contours:
    if len(contour) >= 5:
        ellipse = cv2.fitEllipse(contour)
        ellipses.append(ellipse)

# Filtrage pour garder uniquement les ellipses concentriques
concentric_ellipses = []
for i, ellipse1 in enumerate(ellipses):
    for j, ellipse2 in enumerate(ellipses):
        if i >= j:  # Éviter de comparer une ellipse avec elle-même ou refaire les comparaisons
            continue

        # Extraire les caractéristiques des ellipses
        (x1, y1), (major1, minor1), angle1 = ellipse1
        (x2, y2), (major2, minor2), angle2 = ellipse2

        # 1. Vérifier la proximité des centres
        center_distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if center_distance > 0.1:  # Seuil de distance des centres (ajustez selon vos besoins)
            continue

        # 2. Vérifier le rapport des axes
        ratio_major = max(major1, major2) / min(major1, major2)
        ratio_minor = max(minor1, minor2) / min(minor1, minor2)
        if ratio_major > 1.2 or ratio_minor > 1.2:  # Seuil de tolérance sur le rapport des dimensions
            continue

        # 3. Vérifier l'orientation
        if abs(angle1 - angle2) > 10:  # Seuil de tolérance sur l'angle (en degrés)
            continue

        # Si tous les critères sont remplis, les ellipses sont concentriques
        concentric_ellipses.append((ellipse1, ellipse2))

# Afficher les ellipses concentriques détectées
for ellipse1, ellipse2 in concentric_ellipses:
    cv2.ellipse(image, ellipse1, (0, 255, 0), 2)  # Vert pour la première ellipse
    cv2.ellipse(image, ellipse2, (255, 0, 0), 2)  # Rouge pour la deuxième ellipse

# Afficher l'image finale
# cv2.imshow("Ellipses concentriques", image)
cv2.imwrite("res/images/generated/ellipses/concentric_ellipses.png", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
