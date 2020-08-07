import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import math
sitl = None

import dronekit_sitl

# Connect to the Vehicle
vehicle = connect('udp:127.0.0.1:14553', wait_ready=True)

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


arm_and_takeoff(20)
time.sleep(6)

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
gotocord(point1)

print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
gotocord(point2)

for i in range(2):
    vehicle.mode = VehicleMode("RTL")



print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

