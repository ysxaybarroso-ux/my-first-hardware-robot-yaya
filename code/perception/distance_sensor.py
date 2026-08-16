from rplidar import RPLidar
import core.config



lidar = RPLidar(core.config.PORT)

def get_scan():
    for scan in lidar.iter_scans():
        return scan

def repere_obstacle(scan):
    obstacles = []
    for (_, angle, distance) in scan:
        if (angle < 30 or angle > 330) and distance < 100:
            obstacles.append((angle, distance))
        
    return obstacles    