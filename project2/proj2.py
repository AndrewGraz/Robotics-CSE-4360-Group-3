from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
import umath
import urandom
#wait(1000)
hub = PrimeHub()
fan = Motor(Port.D, Direction.COUNTERCLOCKWISE)
left = Motor(Port.E, Direction.CLOCKWISE)
right = Motor(Port.F, Direction.COUNTERCLOCKWISE)
watch = StopWatch() 
driver = DriveBase(left, right, wheel_diameter=56, axle_track=116)
hub.display.number(69)
hub.imu.reset_heading(0)
left.control.limits(acceleration=1000)
right.control.limits(acceleration=1000)
button = ForceSensor(Port.B)
ultra = UltrasonicSensor(Port.C)
color_sensor = ColorSensor(Port.A)
alarm = hub.speaker


global robot_angle
global wf_time_limit

wf_time_limit = 100*1000
robot_angle = 0


def turn(target_angle, speed=100):
    current_angle = hub.imu.heading()
    wheel_circumference = umath.pi * 56  
    turn_distance = (target_angle / 360) * (umath.pi * 161.29)  

    motor_degrees = (turn_distance / wheel_circumference) * 360

    #left
    if target_angle >0:
        left.run_angle(-speed, motor_degrees, Stop.HOLD, wait=False)
        right.run_angle(speed, motor_degrees, Stop.HOLD, wait=True)
    #right 
    elif target_angle <0:
        # Right turn: Left motor moves forward, right motor moves backward
        left.run_angle(-speed, motor_degrees, Stop.HOLD, wait=False)
        right.run_angle(speed, motor_degrees, Stop.HOLD, wait=True)
    hub.imu.reset_heading(0)
   ###########################################################################


def wall_follow(message):
    wall_watch = StopWatch()
    wall_watch.reset()
    
    maintain_dist = 90
    wall_align_distance = 70
    no_wall_threshold = 350
    max_rate = 25
    kp = 0.35

    wait_time = 5
    drive_s = 100
    driver.reset()

    global wf_time_limit

    while True:
        if detect_red():
            return
        #print("INSIDE WALL FOLLOW")
        
        if wall_watch.time() > wf_time_limit:
            print("Wall Follow Timeout, selecting new goal direction")
            return
        
        
        distance = ultra.distance()
        correction_dist = maintain_dist - distance
        
        turn_rate = kp * (correction_dist)
        turn_rate = max(-1*max_rate , min(max_rate, turn_rate))
        
        if message == "from wander":
            if button.touched() == True:

                #previous_wall_hit_pos = robot_pos
                driver.straight(-60)
                #print(distance)
                distance = ultra.distance()
                align_watch = StopWatch()
                align_watch.reset()
                while distance > wall_align_distance:
                    if align_watch.time() > 10*1000:
                        print("Could not align, picking new goal")
                        return
                    
                    print(distance)
                    # driver.stop()
                    turn(-10)
                    
                    wait(100)
                    distance = ultra.distance()
        else:
        
            #driver.drive(drive_s,0)#turn_rate)
            if distance > no_wall_threshold:
                for i in range(70):
                    if button.touched():
                        driver.straight(100)
                        break
                   
                    if detect_red():
                        return
                    driver.drive(100,0)
                    wait(10)
                    
                turn(100)
               
                for i in range(70):
                    if button.touched():
                        driver.straight(100)
                        break
                    
                    if detect_red():
                        return 
                    driver.drive(200,0)
                    wait(10)
            else:
                driver.reset()
                driver.drive(drive_s, turn_rate)
                
                for i in range(wait_time):  
                    if detect_red():
                        return
                    wait(1)

            if button.touched():
                driver.straight(-80)
                turn(-100)
                
        message = "" 

    print(f"Exiting wall following...")


def get_random_goal():
    r = urandom.randrange(0,360,90)
    return r

def detect_red():
    color_watch = StopWatch()
    color_watch.reset()
    color = color_sensor.color()
    if color == Color.BLACK:
        alarm.play_notes(["F#4/4", "C4/4","F#4/4", "C4/4"], tempo=120)
        wait(1000)
        while color_watch.time() < 75*1000:
            turn(-25)
            fan.run(10000)
            wait(5000)

def wander():
    global robot_angle
    random_goal = get_random_goal()
    turn(1*robot_angle)
    turn(-1*random_goal)
    robot_angle = random_goal
    driver.reset()
    
    while button.touched() == False:
    
        driver.reset()
        #print("H")
        driver.drive(100, 0)
        wait(40)
        #print(driver.distance())
        
        if button.touched() == True:
            #driver.stop()
            driver.straight(100)
            wall_follow("from wander")
            turn(robot_angle)
            random_goal = get_random_goal()
            turn(-1*random_goal)
            robot_angle = random_goal
        

wander()
