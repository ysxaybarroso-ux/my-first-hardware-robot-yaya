from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import behavior.state_machine as machine
import behavior.commandes as cmd
import time
import random
from PIL import Image
import os

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)
nom_dossier = ""


def choose_anim():
    global nom_dossier
    if machine.isTalking == True:
        if machine.mode_turtle:
            nom_dossier = "mode_parle"
        else:
            nom_dossier = "il_parle"
    elif machine.state == "MANUAL":
        if machine.mode_turtle:
            nom_dossier = "mode_manuel_tortue"
        else:
            nom_dossier = "mode_manuel"

        
    elif machine.state == "FOLLOW":
        if machine.mode_turtle:
            nom_dossier = "mode_follow_tortue"
        else:
            nom_dossier = "mode_follow"

    elif machine.state == "NAVIGATION":
        if machine.mode_turtle:
            nom_dossier = "mode_navigation_tortue"
        else:
            nom_dossier = "mode_navigation"
    elif machine.state == "STATIC":
        options = ["normal", "clin_oeil", "sifflement", "clignement_2_yeux"]
        probabilites = [40, 25, 15,20] #  total == 100
        reponse = random.choices(options, weights=probabilites, k=1)[0]
        nom_dossier = reponse
    return nom_dossier

def boucle_affichage():
    animation_actuelle = None
    frame_actuelle = 0
    while True:
        nouvelle_animation = choose_anim()
        if nouvelle_animation == animation_actuelle:
            frame_actuelle += 1 
        else:
            frame_actuelle = 0
            animation_actuelle = nouvelle_animation

        chemin = "sprites/" + animation_actuelle
        fichiers = sorted(os.listdir(chemin))
        nom_fichier = (fichiers[frame_actuelle % len(fichiers)])
        image =Image.open(chemin + "/" + nom_fichier)
        device.display(image)
        time.sleep(1/12)