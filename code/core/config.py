
"""for uart and perception"""
PORT = "/dev/ttyUSB0"   

"""const object in 3d"""

"""mouv max """
step_lenght = 20.0
step_height = 15.0

"""for the stability the length center robot to paw """
distance_x_patte = 145.8
distance_y_patte = 76

"""state vocaux"""
states_vocaux = {
    "suis": "FOLLOW", "follow": "FOLLOW",
    "manuel": "MANUAL", "manual": "MANUAL",
    "navigation": "NAVIGATION",
    "arrete": "STATIC", "stop": "STATIC"
}

"""the 2 first motor are near"""
coxa= 5.0 
cuisse= 110.00 
tibia = 120.00
largeur_robot = 197
rotation_par_cycle = (2* step_lenght) /largeur_robot

"""cible"""
targets = {
    "ARD": (10, 20, 0), 
    "ARG": (10, 40, 0),
    "AVD": (10, 20, 0),
    "AVG": (10, 40, 0),
}
stance_ratio = 0.5

ADDR_GOAL_POSITION = 42

"""servo id's (don't call the cops they have their)"""
patte_ARD = {
    "hanche_id" : 1,
    "cuisse_id" :2,
    "genou_id" : 3}

patte_ARG = {
    "hanche_id" : 4,
    "cuisse_id" :5, 
    "genou_id" : 6}

patte_AVD = {
    "hanche_id" : 7,
    "cuisse_id" :8,
    "genou_id" : 9}

patte_AVG = {
    "hanche_id" : 10,
    "cuisse_id" :11,
    "genou_id" : 12}
sg90_id = 13


pattes = {
    "ARD": patte_ARD,
    "ARG": patte_ARG,
    "AVD": patte_AVD,
    "AVG": patte_AVG
}


"""diagonale de patte avec offset"""
phase_offsets = {
    "AVD": 0,
    "ARG":0.,
    "AVG": 0.5,
    "ARD": 0.5,
}
"""repos position"""
x_repos = 0.0
y_repos = 40.0
z_repos = 130.0


"""commandes"""
directions = {"avance": "F","forward":"F", "backward":"B", "recule": "B","left":"G", "gauche": "G", "right": "D", "droite": "D"}