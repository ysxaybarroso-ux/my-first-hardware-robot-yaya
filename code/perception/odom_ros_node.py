import math 
import perception.distance_sensor
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import core.servo_controller
import threading
import perception.connectivite
import behavior.state_machine 
import perception.stt
import behavior.commandes
import perception.camera_tracking
import perception.stabilitee_sensor as stab
import behavior.oled_display as oled
class Odom(Node):
    def __init__(self):
        super().__init__('nav_node')
        self.publisher = self.create_publisher(Odometry, '/odom', 10)
        self.create_timer(0.2, self.Envoi_Position)

    def Envoi_Position(self):
        y = 0
        x = 0 
        z = math.sin(core.servo_controller.theta/2)
        w = math.cos(core.servo_controller.theta /2)
        odom = Odometry()
        odom.pose.pose.position.x = core.servo_controller.distance_x
        odom.pose.pose.position.y = core.servo_controller.distance_y
        odom.pose.pose.orientation.y = y
        odom.pose.pose.orientation.x = x
        odom.pose.pose.orientation.z = z
        odom.pose.pose.orientation.w = w

def main():
    thread_marche =threading.Thread(target=core.servo_controller.boucle_marche)
    thread_marche.start()

    thread_internet =threading.Thread(target=perception.connectivite.a_internet)
    thread_internet.start()

    thread_vocal =threading.Thread(target=perception.stt.Ecoute)
    thread_vocal.start()

    thread_commandes =threading.Thread(target=behavior.commandes.Traiter_commande)
    thread_commandes.start()

    thread_camera=threading.Thread(target=perception.camera_tracking.detect)
    thread_camera.start()

    thread_stabilitee=threading.Thread(target=stab.lire_stabilitee)
    thread_stabilitee.start()

    thread_oled=threading.Thread(target=oled.boucle_affichage)
    thread_oled.start()

    thread_machine=threading.Thread(target=behavior.state_machine.boucle_state_machine)
    thread_machine.start()
    rclpy.init()
    Odom_class = Odom()
    rclpy.spin(Odom_class)