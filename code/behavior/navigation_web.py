from nav_msgs.msg import  OccupancyGrid
from rclpy.node import Node
import rclpy
import threading
import os
import io
from flask import send_file
from flask import render_template
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import perception.camera_tracking as camera
from flask import request
from flask import Flask
from PIL import Image
import behavior.state_machine as state
import cv2
app = Flask(__name__)

carte = None
derniere_carte = None


class navigation_web (Node):
    def __init__(self):
        super().__init__('nav_node')
        self.publisher_ = self.create_subscription(OccupancyGrid, '/map', self.afficher_carte, 10 )
        self.action_client = ActionClient(self , NavigateToPose, 'navigateToPose')

    def afficher_carte(self, msg):
        global derniere_carte 
        derniere_carte = msg
        return msg

@app.route('/carte')
def envoyer_carte():
    image = generer_image_carte()
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

@app.route('/shutdown' , methods=['POST'])
def shutdown_protocol3():
    os.system("sudo shutdown now")
    return "ok"

@app.route('/state', methods=['POST'])
def change_state():
    donnees = request.json
    new_state = donnees['state']
    state.state = new_state
    return "ok"

@app.route('/')
def page_html():
    return render_template('index.html')
@app.route('/camera')
def envoyer_camera():
    if camera.personne_detectee is None:
        return "no one in the zone yet"
    image_annotee = camera.personne_detectee[0].plot()
    succes , buffer_encode = cv2.imencode('.png' , image_annotee)
    return send_file(io.BytesIO(buffer_encode) , mimetype='image/png')

@app.route('/choisir_personne', methods=['POST'])
def choisir_personne():
    donnees = request.json
    click_x = donnees['x']
    click_y = donnees['y']
    for boite in camera.personne_detectee[0].boxes:
        x_min, y_min, x_max, y_max = boite.xyxy[0]
        if x_min <= click_x <= x_max and y_min <= click_y <= y_max:
            camera.cible_x = (x_max + x_min) / 2
            camera.cible_y = (y_min + y_max)  / 2
        return "ok"

@app.route('/manual', methods=['POST'])
def recevoir_manual():
    donnees = request.json
    state.manual_angular_y = donnees['dx']
    state.manual_linear_x = donnees['dy']
    return "ok"

@app.route('/manual_camera', methods=['POST'])
def recevoir_manual_camera():
    donnees = request.json
    state.camera_angular_z = donnees['dx']
    return "ok"

@app.route('/objectif', methods=['POST'])
def recevoir_objectif():
    donnees = request.json
    x = donnees['x']
    y = donnees['y']
    x_real = derniere_carte.info.origin.position.x + x *  derniere_carte.info.resolution
    y_real = derniere_carte.info.origin.position.y + y *  derniere_carte.info.resolution
    goal_msg = NavigateToPose.Goal()
    goal_msg.pose.header.frame_id = 'map'
    goal_msg.pose.pose.position.x = x_real
    goal_msg.pose.pose.position.y = y_real
    goal_msg.pose.pose.orientation.w = 1.0
    carte.action_client.send_goal_async(goal_msg)
    return "ok"

def generer_image_carte():
    global derniere_carte
    hauteur = derniere_carte.info.height
    longueur = derniere_carte.info.width
    image = Image.new("RGB",(longueur , hauteur))
    for p, pixel in  enumerate(derniere_carte.data):
        y = p // longueur
        x = p % longueur
        if pixel ==  0:
            image.putpixel((x, y), (37, 39, 38))
        elif pixel == -1:
            image.putpixel((x,y),(158, 3, 3))
        else:
            image.putpixel((x,y), (122, 118, 118))
    return image 
    
def main():
    global carte
    thread_web = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    thread_web.start() 
    rclpy.init()
    carte = navigation_web()
    rclpy.spin(carte)
