import socket
#pip install socket
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import math
sitl = None
import dronekit_sitl
vehicle = connect('udp:127.0.0.1:14552', wait_ready=True)



def gotocord(aloc):
    vehicle.airspeed = 17
    vehicle.simple_goto(aloc)
    while(get_distance_metres(aloc)>=0.5):
	continue 
    vehicle.airspeed =0
    
    print("reached")



def get_distance_metres(aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    aLocation1=vehicle.location.global_relative_frame
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
	vehicle.armed = True
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    i=0
    while True:
	i=i+1
	
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
	if(i%4==0 and vehicle.location.global_relative_frame.alt<0.5):
	    vehicle.armed = True
	    print("hello")
	    vehicle.simple_takeoff(aTargetAltitude)
        time.sleep(1)


arm_and_takeoff(10)


  
  
while(True):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1234))
    msg =s.recv(50)
    msg=msg.decode("utf-8")
    lat=msg[:11]
    lon=msg[11:22]
    alt=msg[22:23]
    
    try:
        float(lat)
        float(lon)

    
        print(lat)
        print(lon)
    

    
        po = LocationGlobalRelative(float(lat), float(lon), 20)
        vehicle.simple_goto(po)
	time.sleep(1)
    except:
	pass
  
  
