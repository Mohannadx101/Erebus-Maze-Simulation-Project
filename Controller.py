from controller import Robot , Motor, Camera, Lidar, Emitter, Receiver
import cv2
import numpy as np
import math
import struct



robot = Robot()
timestep = 32
max_velocity = 6.28 

# Wheels
wheel1 = robot.getDevice('wheel1 motor')
wheel2 = robot.getDevice('wheel2 motor')
wheel1.setPosition(float('inf'))
wheel2.setPosition(float('inf'))

# Defining
gps = robot.getDevice('gps')
compass = robot.getDevice('compass')
camera_right = robot.getDevice('right_camera')
camera_left = robot.getDevice('left_camera')
color_sensor = robot.getDevice('colour_sensor')
lidar = robot.getDevice('lidar')
emitter = robot.getDevice('emitter')
receiver = robot.getDevice('receiver')

#Enabling sensors
gps.enable(timestep)
compass.enable(timestep)
camera_right.enable(timestep)
camera_left.enable(timestep)
color_sensor.enable(timestep)
lidar.enable(timestep)
lidar.enablePointCloud()
lidar_values = []
gps_readings = [0, 0, 0]
compass_value = 0
color_sensor_values = [0, 0, 0]
receiver.enable(timestep)
last_turn_time = -5
turn_cooldown = 2
current_velocity = 0  # Keep track of current velocity outside the function
acceleration_rate = 0.3  # Adjust for smoother acceleration


# Getting Color sensor values
def get_color_sensor_values():
    image = color_sensor.getImage()
    
    r = color_sensor.imageGetRed(image, 1, 0, 0)
    g = color_sensor.imageGetGreen(image, 1, 0, 0)
    b = color_sensor.imageGetBlue(image, 1, 0, 0)

    color_sensor_values[0] = r
    color_sensor_values[1] = g
    color_sensor_values[2] = b
    
    
#Getting LIDAR values
def get_lidar_values():
    global lidar_values
    lidar_values = []
    
    range_image = lidar.getRangeImage()
    
    for layer in range(4):
        lidar_values.append([])
        for point in range(512):
            lidar_values[layer].append(
                 round(
                    range_image[layer * 512 + point] * 100,
                    2
                )
            )


# Getting GPS Readings
def get_gps_readings():
    gps_readings[0] = gps.getValues()[0]
    gps_readings[1] = gps.getValues()[1]
    gps_readings[2] = gps.getValues()[2]


# Getting Compass Values
def get_compass_value():
    global compass_value
    compass_value = compass.getRollPitchYaw()[2]
    compass_value = compass_value * 180 / math.pi
    compass_value = round(compass_value, 1)
    

#Turning the robot 90 degrees to a straight line Left
def turn_90():
    compass_value_rounded_to_nearest_90 = round(compass_value / 90) * 90
    next_angle = compass_value_rounded_to_nearest_90 + 90
    if next_angle > 180:
        next_angle -= 360
        
    while robot.step(timestep) != -1:
        get_all_sensor_values()
        print("--------------------GPS Values-------------------------")
        print("X", gps_readings[0])
        print("Y", gps_readings[2])
        print("--------------------------------------------------------")
        print()
        print("-------------------Lidar Values------------------------")
        print("Front: ", lidar_values[2][0])
        print("Left: ", lidar_values[2][383])
        print("Right: ", lidar_values[2][127])
        print("Back: ", lidar_values[2][255])
        print("--------------------------------------------------------")
        print()
        print("--------------------Compass Values---------------------")
        print(compass_value)
        print("--------------------------------------------------------")
        print()
        print("---------------------Color Values-----------------------")
        print(color_sensor_values)
        print("--------------------------------------------------------")
        
        wheel1.setVelocity(3)
        wheel2.setVelocity(-3)
        
        if abs(compass_value - next_angle) < 7:
            break


# Robot acceleration to max speed
# This function is called in the main loop to gradually accelerate the robot to its maximum speed.
def accelerate_to_max_speed():
    global current_velocity  # Keep track of velocity across iterations
    
    if current_velocity < max_velocity:
        current_velocity += acceleration_rate  # Gradually increase
        if current_velocity > max_velocity:
            current_velocity = max_velocity  # Cap it at max velocity

    wheel1.setVelocity(current_velocity)
    wheel2.setVelocity(current_velocity)

# Turning the robot 90 degrees to the Right
def turn_90_right():
    stop()
    global compass_value
    compass_value_rounded_to_nearest_90 = round(compass_value / 90) * 90
    next_angle = compass_value_rounded_to_nearest_90 - 90
    if next_angle < -180:
        next_angle += 360
        
    while robot.step(timestep) != -1:
        get_all_sensor_values()
        print("--------------------GPS Values-------------------------")
        print("X", gps_readings[0])
        print("Y", gps_readings[2])
        print("--------------------------------------------------------")
        print()
        print("-------------------Lidar Values------------------------")
        print("Front: ", lidar_values[2][0])
        print("Left: ", lidar_values[2][383])
        print("Right: ", lidar_values[2][127])
        print("Back: ", lidar_values[2][255])
        print("--------------------------------------------------------")
        print()
        print("--------------------Compass Values---------------------")
        print(compass_value)
        print("--------------------------------------------------------")
        print()
        print("---------------------Color Values-----------------------")
        print(color_sensor_values)
        print("--------------------------------------------------------")
        
        wheel1.setVelocity(-3)
        wheel2.setVelocity(3)
        
        if abs(compass_value - next_angle) < 7:
            stop()
            break
        
#Stopping the robot
def stop():
    start_time = robot.getTime()
    while robot.step(timestep) != -1:
        wheel1.setVelocity(0)
        wheel2.setVelocity(0)
        if robot.getTime() - start_time >= 1:  # 5 seconds delay
            break

#Getting all sensor values
def get_all_sensor_values():
    get_color_sensor_values()
    get_lidar_values()
    get_gps_readings()
    get_compass_value()
    


# Main loop:
start = robot.getTime()
while robot.step(timestep) != -1:
    get_all_sensor_values()
    print("--------------------GPS Values-------------------------")
    print("X", gps_readings[0])
    print("Y", gps_readings[2])
    print("--------------------------------------------------------")
    print()
    print("-------------------Lidar Values------------------------")
    print("Front: ", lidar_values[2][0])
    print("Left: ", lidar_values[2][383])
    print("Right: ", lidar_values[2][127])
    print("Back: ", lidar_values[2][255])
    print("--------------------------------------------------------")
    print()
    print("--------------------Compass Values---------------------")
    print(compass_value)
    print("--------------------------------------------------------")
    print()
    print("---------------------Color Values-----------------------")
    print(color_sensor_values)
    print("--------------------------------------------------------")
    
    current_time = robot.getTime()
    front = lidar_values[2][0]
    left = lidar_values[2][383]
    right = lidar_values[2][127]
    back = lidar_values[2][255]
    
    if(front < 6 or (color_sensor_values[0] < 100 and color_sensor_values[1] < 100 and color_sensor_values[2] < 100)):
        last_turn_time = current_time
        
        if(left < right):
            turn_90_right()
            
        else:
            turn_90()
            
    else:
        accelerate_to_max_speed()
    
    
