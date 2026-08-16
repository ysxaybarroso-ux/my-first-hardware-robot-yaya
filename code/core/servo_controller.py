import scservo_sdk
import kinematics
import config
import gait
import behavior.state_machine
import perception.stabilitee_sensor as stab
import math
import behavior.cmd_vel_bridge as cmd
import perception.camera_tracking as cam
"""import gpiod
chip = gpiod.Chip('gpiochip0')
ligne_sg90 = chip.get_line(NUMERO_PIN)  # à remplacer par le vrai numéro une fois câblé
ligne_sg90.request(consumer='sg90', type=gpiod.LINE_REQ_DIR_OUT)"""

"""port = "COM3"
baud_rate = 1000000 """
distance_x = 0 
distance_y = 0
theta =0
objectif_pas = 0
nombre_pas =0
z_result = 0

""" port_handler = scservo_sdk.PortHandler(port)
protocol_end = 0 
packet_handler = scservo_sdk.PacketHandler(protocol_end)"""

theta1, theta2, theta3 = kinematics.kenematic_inverse(config.x_repos,
                                                       config.y_repos,
                                                         config.z_repos,
                                                         config.coxa,
                                                           config.cuisse, 
                                                           config.tibia)

"""if port_handler.openPort():
    print("open all alright")
else:
    print("ohoh problem no open brather")

if port_handler.setBaudRate(baud_rate):
    print("good speed good speed fella")
else: 
    print("no good speed man not good")"""

"""def tell_servo(servo_id, servo_angle):
    position_brute = int(((servo_angle+ 180) / 360) * 4096)
    packet_handler.write2ByteTxRx(port_handler, servo_id,config.ADDR_GOAL_POSITION,position_brute)"""


def tell_servo_sg90(angle):
    pass
    # TODO  matériel reçu : convertir angle (-30 à 30) en durée de pulse PWM
    # ( 1500 + (angle/30)*500 microsecondes), envoyer  gpiod / lib PWM Radxa 

def mouvement(t):
    global z_result
    gait_offset = gait.trot(t, config.step_lenght , config.step_height , config.stance_ratio , behavior.state_machine.direction)
    for nom_patte, (x,y,z) in config.targets.items():
        dx , dz = gait_offset[nom_patte]
        if stab.pitch is not None and stab.roll is not None:
            z_result = compensation_inclinaison(nom_patte, math.radians(stab.pitch), math.radians(stab.roll))

        x = config.x_repos + dx
        y = config.y_repos
        z = config.z_repos + dz + z_result

        if "D" in nom_patte:
            y = -y

        theta1, theta2, theta3 = kinematics.kenematic_inverse(x,y,z,config.coxa,config.cuisse,config.tibia)
        """tell_servo(patte["hanche_id"], theta1)"""
        """tell_servo(patte["cuisse_id"], theta2)"""
        """tell_servo(patte["genou_id"], theta3)"""
        print(f"{nom_patte}: hanche={theta1:.1f}° cuisse={theta2:.1f}° genou={theta3:.1f}°")

def mouvement_continu(t):
    global z_result
    gait_offset = gait.trot_continu(t, config.step_lenght , config.step_height , config.stance_ratio , cmd.ordre.angular.z, cmd.ordre.linear.x)
    for nom_patte, (x,y,z) in config.targets.items():
        dx , dz = gait_offset[nom_patte]
        if stab.pitch is not None and stab.roll is not None:
            z_result = compensation_inclinaison(nom_patte, math.radians(stab.pitch), math.radians(stab.roll))

        x = config.x_repos + dx
        y = config.y_repos
        z = config.z_repos + dz + z_result

        if "D" in nom_patte:
            y = -y

        theta1, theta2, theta3 = kinematics.kenematic_inverse(x,y,z,config.coxa,config.cuisse,config.tibia)
        """tell_servo(patte["hanche_id"], theta1)"""
        """tell_servo(patte["cuisse_id"], theta2)"""
        """tell_servo(patte["genou_id"], theta3)"""
        print(f"{nom_patte}: hanche={theta1:.1f}° cuisse={theta2:.1f}° genou={theta3:.1f}°")

def compensation_inclinaison(nom_patte, pitch , roll):
    signe_y = 1 if "D" in nom_patte else -1
    signe_x = 1 if "V" in nom_patte else -1
    ajustement_pitch =  config.distance_x_patte * math.tan(pitch) * signe_x
    ajustement_roll = config.distance_y_patte * math.tan(roll) * signe_y
    ajustement_z = ajustement_pitch + ajustement_roll
    return ajustement_z

def orienter_camera():
    centre_image = cam.derniere_image.shape[1] /2 
    if behavior.state_machine.state == "MANUAL":
        angle = behavior.state_machine.camera_angular_z * 30
        """tell_servo_sg90(angle)"""
    elif behavior.state_machine.state == "FOLLOW":
        if cam.cible_x is not None:
            ecart = cam.cible_x - centre_image
            angle = (ecart /centre_image ) * 30
            """tell_servo_sg90(angle)""" 
    else : 
         """tell_servo_sg90(0)"""


def boucle_marche():
    global  distance_x, distance_y, theta ,nombre_pas
    distance_x = 0 
    distance_y = 0
    theta = 0
    t = 0.0
    old_t = t
    distance_totale= 0
    while True:
        if  behavior.state_machine.state == "ORDER":
            nombre_pas = 0
            while nombre_pas < objectif_pas:
                mouvement(t)
                nombre_pas += 1
                t = (t + 0.02) % 1.0
                if old_t > t:
                    if behavior.state_machine.direction == "F":
                        distance_y += config.step_lenght * math.sin(theta)
                        distance_x += config.step_lenght * math.cos(theta)
                    elif behavior.state_machine.direction == "G":
                        theta -= config.rotation_par_cycle
                    else: 
                        theta += config.rotation_par_cycle
                old_t = t
                """port_handler.closePort()"""
        else: 
            while cmd.ordre is not None  and (cmd.ordre.linear.x != 0 or cmd.ordre.angular.z != 0):
                            mouvement_continu(t)
                            nombre_pas += 1
                            t = (t + 0.02) % 1.0
                            if old_t > t:
                                distance_y += cmd.ordre.linear.x * math.sin(theta)
                                distance_x += cmd.ordre.linear.x * math.cos(theta)
                                theta += cmd.ordre.angular.z
                            old_t = t
                            """port_handler.closePort()"""