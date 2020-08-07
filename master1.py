import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import math
sitl = None
import socket
#pip install socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5) 


import dronekit_sitl

# Connect to the Vehicle
vehicle = connect('udp:127.0.0.1:14558', wait_ready=True)


while True:
    cs,add = s.accept()
    print(add)
    print("connection to host from server is done")
    text=str(vehicle.location.global_relative_frame.lat)+str(vehicle.location.global_relative_frame.lon)+str(vehicle.location.global_relative_frame.alt)
    text=text.encode('utf-8')
    cs.send(text)
    cs.close()    
    time.sleep(1)



