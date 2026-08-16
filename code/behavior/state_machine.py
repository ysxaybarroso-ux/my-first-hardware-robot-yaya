import perception.distance_sensor
import core.gait
import core.config 
import core.servo_controller
import perception.camera_tracking as cam
"""state"""
state = "STATIC"  # all state are STATIC FOLLOW NAVIGATION AND MANUAL even ORDER
mode_turtle = False  #easter egg animation on oled
isTalking = False 

"""evitement state"""
isEvitement = False

"""direction"""
direction = "F"


compteur_presence = 0
compteur_abs = 0
manual_linear_x = 0
manual_angular_z = 0

camera_angular_z = 0

angle_precedent = None
distance_precedent = None
offset_repere = 5 # angle d'offset pour le scan de repere
seuil_N = 5 

scan = perception.distance_sensor.get_scan()

def evitement_obstacle( scan , seuil_N, offset_repere, angle_precedent, distance_precedent):
    obstacles = perception.distance_sensor.repere_obstacle(scan)

    if obstacles:
        actual_angle , distance_actual = min(obstacles, key =lambda o: o[1])

        same_obstacles = (angle_precedent is not None and distance_precedent is not None and
        abs(actual_angle - angle_precedent) <= offset_repere and  
        (distance_actual <= (distance_precedent + 40)) and 
        (distance_actual >= (distance_precedent - 40)))

        compteur_presence+= 1
        compteur_abs = 0
        angle_precedent = actual_angle
        distance_precedent = distance_actual
    else:
        compteur_abs +=1
        compteur_presence = 0
        angle_precedent = None


    if compteur_presence >= seuil_N:
        isEvitement = True
    elif compteur_abs >= seuil_N: 
        isEvitement= False

    return isEvitement , compteur_presence, compteur_abs, angle_precedent , distance_precedent

def launch_evitement():
    global direction
    if isEvitement:
        if angle_precedent < 180:
            direction = "G"
        else: 
            direction = "D"
            core.gait.trot( core.servo_controller.t, core.config.step_lenght, core.config.step_height, core.config.stance_ratio, direction )
    else: 
        direction = "F"
        core.gait.trot( core.servo_controller.t, core.config.step_lenght, core.config.step_height, core.config.stance_ratio, direction )

def launch_suivi():
    centre_image = cam.derniere_image.shape[1] /2 
    if cam.cible_x is not None:
        ecart = cam.cible_x - centre_image
        angular_z = -ecart / centre_image  # proportionnel 
        linear_x = 0.3  # vitesse d'avance fixe 
        core.gait.trot_continu(core.servo_controller.t, core.config.step_lenght, core.config.step_height , core.config.stance_ratio, angular_z, linear_x)

def boucle_state_machine():
    global isEvitement, compteur_presence, compteur_abs, angle_precedent, distance_precedent
    while True:
        scan = perception.distance_sensor.get_scan()
        isEvitement , compteur_presence , compteur_abs, angle_precedent , distance_precedent = evitement_obstacle( scan , seuil_N, offset_repere, angle_precedent, distance_precedent)

        if state ==  "STATIC":
            pass

        if state == "NAVIGATION":
            launch_evitement()

        if state == "FOLLOW":
            if isEvitement:
                launch_evitement()
            else:
                launch_suivi()

        if state == "MANUAL": 
            core.gait.trot_continu(core.servo_controller.t, core.config.step_lenght, core.config.step_height , core.config.stance_ratio, manual_angular_z , manual_linear_x)