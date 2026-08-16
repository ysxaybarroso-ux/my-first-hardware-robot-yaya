from math import sin, cos, pi
import config

def get_foot_offset(phase, step_lenght, step_height, stance_ratio = 0.5):
    if phase < stance_ratio:
        progression = phase / stance_ratio
        dx = step_lenght/2 - progression * step_lenght
        dz = 0
    else:
        progression = (phase - stance_ratio) / (1- stance_ratio)
        dx = -step_lenght/2 + progression * step_lenght
        dz = step_height * sin(progression * pi)
    return dx, dz

def trot (t, step_lenght , step_height , stance_ratio, direction):
    result = {}
    for nom_patte , offset in config.phase_offsets.items():
        phase = ( t + offset) %1
        if direction in ["D", "G"]:
            facteur = 1 - 2 * ((direction =="D")  == ("D" in nom_patte))
        elif direction == "F":
            facteur = 1
        elif direction == "B":
            facteur = -1
        dx, dz = get_foot_offset(phase , facteur * step_lenght , step_height, stance_ratio)
        result[nom_patte] = (dx, dz)
    return result

def trot_continu(t , step_lenght, step_height, stance_ratio, angular_z , linear_x):
    result = {}
    for nom_patte , offset in config.phase_offsets.items():
        phase = ( t + offset) %1

        signe_cote = 1 if "D" in nom_patte else -1
        effet_virage = signe_cote * angular_z
        facteur = linear_x + effet_virage

        dx, dz = get_foot_offset(phase , facteur * step_lenght , step_height, stance_ratio)
        result[nom_patte] = (dx, dz)
    return result