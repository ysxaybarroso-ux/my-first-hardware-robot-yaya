import scservo_sdk
import kinematics
import config

port = "COM3"
baud_rate = 1000000

port_handler = scservo_sdk.PortHandler(port)
protocol_end = 0 
packet_handler = scservo_sdk.PacketHandler(protocol_end)

theta1, theta2, theta3 = kinematics.kenematic_inverse(config.x,
                                                       config.y,
                                                         config.z,
                                                         config.coxa,
                                                           config.cuisse, 
                                                           config.tibia)

if port_handler.openPort():
    print("open all alright")
else:
    print("ohoh problem no open brather")

if port_handler.setBaudRate(baud_rate):
    print("good speed good speed fella")
else: 
    print("no good speed man not good")

def tell_servo(servo_id, servo_angle):
    position_brute = int((servo_angle/ 360) * 4096)
    packet_handler.write2ByteTxRx(port_handler, servo_id,config.ADDR_GOAL_POSITION,position_brute)

def mouvement():
    theta1, theta2, theta3 =  kinematics.kenematic_inverse(config.x, config.y, config.z,config.coxa, config.cuisse, config.tibia)
    tell_servo(config.patte_AVG["hanche_id"],theta1)
    tell_servo(config.patte_AVG["cuisse_id"],theta2)
    tell_servo(config.patte_AVG["genou_id"],theta3)

    theta1, theta2, theta3 = kinematics.kenematic_inverse(config.x, config.y, config.z,config.coxa, config.cuisse, config.tibia)
    tell_servo(config.patte_ARG["hanche_id"],theta1)
    tell_servo(config.patte_ARG["cuisse_id"],theta2)
    tell_servo(config.patte_ARG["genou_id"],theta3)

    theta1, theta2, theta3 = kinematics.kenematic_inverse(config.x, -config.y, config.z,config.coxa, config.cuisse, config.tibia)
    tell_servo(config.patte_AVD["hanche_id"],theta1)
    tell_servo(config.patte_AVD["cuisse_id"],theta2)
    tell_servo(config.patte_AVD["genou_id"],theta3)

    theta1, theta2, theta3 = kinematics.kenematic_inverse(config.x, -config.y, config.z,config.coxa, config.cuisse, config.tibia)
    tell_servo(config.patte_ARD["hanche_id"],theta1)
    tell_servo(config.patte_ARD["cuisse_id"],theta2)
    tell_servo(config.patte_ARD["genou_id"],theta3)

try:
    mouvement()
finally:
    port_handler.closePort()