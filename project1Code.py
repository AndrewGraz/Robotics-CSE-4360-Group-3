from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase

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
def drive():
    drive_base

#make it to turn a perfect 90 
def turn(target_angle, speed):
    current_angle = hub.imu.heading()
    direction = 1 if target_angle < current_angle else -1

    while abs(hub.imu.heading() - target_angle) > 1:  # 1 degree tolerance
        left.run(direction * speed)
        right.run(-direction * speed)
    
    left.stop()
    right.stop()
    hub.imu.reset_heading(0)

    
watch.reset()
# while watch.time() < 3000:
driver.straight(348)
turn(90, 69)
