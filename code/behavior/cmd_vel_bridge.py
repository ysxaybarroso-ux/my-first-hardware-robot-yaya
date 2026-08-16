from geometry_msgs.msg import  Twist
from rclpy.node import Node
import rclpy

ordre  = None 

class commande_suivi (Node):
    def __init__(self):
        super().__init__('suis_ordre_node')
        self.publisher_ = self.create_subscription( Twist , '/cmd_vel', self.recevoir_commande, 10 )


    def recevoir_commande(self, msg):
        global ordre
        ordre = msg

def main():
    rclpy.init()
    cmd_s = commande_suivi()
    rclpy.spin(cmd_s)