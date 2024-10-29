from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
import umath
from final_final_path import path_plan

path = path_plan()
wait(1000)
hub = PrimeHub()
left = Motor(Port.E, Direction.CLOCKWISE)
right = Motor(Port.F, Direction.COUNTERCLOCKWISE)
watch = StopWatch() 

driver = DriveBase(left, right, wheel_diameter=56, axle_track=112)


hub.display.number(69)
hub.imu.reset_heading(0)


left.control.limits(acceleration=1000)
right.control.limits(acceleration=1000)

#make it drive only 1 meter forward
def drive(tiles):
    meters = 304.8/2
    distance = tiles*meters
    driver.straight(distance)

#make it to turn a perfect 90 
# def turn(target_angle, speed=69):
#     current_angle = hub.imu.heading()
#     direction = 1 if target_angle < current_angle else -1

#     while abs(hub.imu.heading() - target_angle) > 1:  # 1 degree tolerance
#         left.run(direction * speed)
#         right.run(-direction * speed)
    
#     left.stop()
#     right.stop()
#     hub.imu.reset_heading(0)

def turn(target_angle, speed=100):
    current_angle = hub.imu.heading()
    wheel_circumference = umath.pi * 56  
    turn_distance = (target_angle / 360) * (umath.pi * 161.29)  

    motor_degrees = (turn_distance / wheel_circumference) * 360

    #left
    if target_angle == 90:
        left.run_angle(-speed, motor_degrees, Stop.HOLD, wait=False)
        right.run_angle(speed, motor_degrees, Stop.HOLD, wait=True)
    #right 
    elif target_angle == -90:
        # Right turn: Left motor moves forward, right motor moves backward
        left.run_angle(-speed, motor_degrees, Stop.HOLD, wait=False)
        right.run_angle(speed, motor_degrees, Stop.HOLD, wait=True)
    hub.imu.reset_heading(0)
   ###########################################################################

def main():
    possible_directions = [(-1,0),(1,0),(0,-1),(0,1)]    


    # def drive_path(path):
    #     heading = 'x'
    #     for i in range(len(path) - 1):
    #         print(path)
    #         x1,y1 = path[i]
    #         x2,y2 = path[i+1]
    #         print(x1,y1)
    #         print(x2,y2)
            
            
    #         if((x2 - x1 == 1) or (x2 - x1 == -1)):
    #             if(heading == 'y'):
    #                 if(x2-x1 == 1):
    #                     turn(90)
    #                 if(x2-x1 == -1):
    #                     turn(-90)
    #             drive(1)
    #             heading = 'x'
            
    #         if((y2-y1 == 1) or (y2-y1 == -1)):
    #             if(heading == 'x'):
    #                 if(y2-y1 == 1):
    #                     turn(-90)
    #                 if(y2-y1 == -1):
    #                     turn(90)
    #             drive(1)
    #             heading = 'y'
    def drive_path(path):
        heading = 'x'
        for i in range(len(path) - 1):
            print(path)
            x1,y1 = path[i]
            x2,y2 = path[i+1]
            print(x1,y1)
            print(x2,y2)
            
            
            if((x2 - x1 == 1) or (x2 - x1 == -1)):
                if(heading == 'neg_y'):
                    if(x2-x1 == 1):
                        turn(-90)
                        heading = 'x'
                    if(x2-x1 == -1):
                        turn(90)
                        heading = 'neg_x'
                if(heading == 'y'):
                    if(x2-x1 == 1):
                        turn(90)
                        heading = 'x'
                    if(x2-x1 == -1):
                        turn(-90)
                        heading = 'neg_x'
                drive(1)
                #heading = 'x'
            
            if((y2-y1 == 1) or (y2-y1 == -1)):
                if(heading == 'x'):
                    if(y2-y1 == 1):
                        turn(-90)
                        heading = 'y'
                    if(y2-y1 == -1):
                        turn(90)
                        heading = 'neg_y'
                if(heading == 'neg_x'):
                    if(y2-y1 == 1):
                        turn(90)
                        heading = 'y'
                    if(y2-y1 == -1):
                        turn(-90)
                        heading = 'neg_y'
                    
                drive(1)
                #heading = 'y'

    #path = [(3, 3), (4, 3), (4, 4), (3, 4), (3, 5), (2, 5)]

    drive_path(path)
    #turn(-90)
    #2down, 2right

main()

watch.reset()
