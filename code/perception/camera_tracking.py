import cv2
from ultralytics import YOLO
import behavior.navigation_web as web
import math 

model = YOLO("yolo26n.pt")
personne_detectee = None
derniere_image = None
cible_x = None
cible_y = None
meilleure_distance = None
meilleure_boite = None


def detect():
    global personne_detectee ,derniere_image , meilleure_boite , meilleure_distance , cible_x, cible_y
    cap =  cv2.VideoCapture(0)
    while True:
        succes , frame = cap.read()
        results = model(frame, classes=[0])  # classes 0 = person for YOLO
        personne_detectee = results
        derniere_image = frame
        if cible_x is not None: #pas oblige de metre y et x du momment que ya x ya y
            meilleure_distance = None
            meilleure_boite = None
            for boite in results[0].boxes:
                x_min, y_min, x_max, y_max = boite.xyxy[0]
                centre_x = (x_min + x_max) / 2
                centre_y = (y_min + y_max) / 2
                distance = math.sqrt((centre_x - cible_x)**2 + (centre_y - cible_y)**2)
                if meilleure_distance is None or distance < meilleure_distance:
                    meilleure_distance = distance
                    meilleure_boite = (centre_x, centre_y)
            if meilleure_boite is not None:
                cible_x, cible_y = meilleure_boite
