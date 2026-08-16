import socket 
import time

isConnected = False

def a_internet():
    global isConnected 
    while True:
            try:
                socket.setdefaulttimeout(3)
                socket.socket(socket.AF_INET , socket.SOCK_STREAM).connect(("8.8.8.8", 53))
                isConnected =  True
            except socket.error:
                isConnected  =False
            time.sleep(360)
        

