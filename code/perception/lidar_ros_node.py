import rclpy 
import math 
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import perception.distance_sensor

class LidarNode (Node):
    def __init__(self):
        super().__init__('lidar_node')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        self.create_timer(0.18, self.lire_scan)

    def lire_scan(self):
        scan = perception.distance_sensor.get_scan()
        sommes = [0]*360
        comptes = [0]*360
        ranges = [0] *360
        for qualite , angle , distance in scan:
            distance = distance / 1000
            indice = math.floor(angle)
            sommes[indice] += distance
            comptes[indice] += 1
        for n in range(360):
            if comptes[n] ==0:
                ranges[n] = float('inf')
            else: 
                ranges[n] = sommes[n] / comptes[n]
        msg = LaserScan()
        msg.angle_min = 0.0
        msg.angle_max = math.radians(359)
        msg.angle_increment = math.radians(1)
        msg.range_min = 0.15
        msg.range_max = 12.0
        msg.ranges = ranges
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    lidar = LidarNode()
    rclpy.spin(lidar)
