"""library import"""
import math 
import config



def kenematic_inverse(x,y,z, coxa , cuisse , tibia):
    """angle"""
    print("calculating....")
    theta1 = math.atan2(y,z)
    h = math.hypot(y,z)
    h_restant = h - coxa

    d = math.hypot(x , h_restant)

    theta3_calc = (cuisse**2 + tibia**2 - d**2) /(2* cuisse *tibia)
    cos_theta3 = max(-1.0, min(1.0 , theta3_calc))
    theta3 = math.acos(cos_theta3)

    theta2_all =math.atan2(x,h_restant)
    theta2_restant = math.acos((d**2 + cuisse**2 - tibia**2) / (2*d*cuisse))
    theta2 = theta2_all - theta2_restant

    print("new target calculated in x: ",x,"y:",y,"z:",z)
    return math.degrees(theta1) , math.degrees(theta2) , math.degrees(theta3)

if __name__ == "__main__":
    result = kenematic_inverse(config.x, config.y, config.z, config.coxa, config.cuisse, config.tibia)
    print("helloww world", result)