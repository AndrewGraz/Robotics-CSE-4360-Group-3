from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch


MAX_OBSTACLES = 25  # Maximum number of obstacles
num_obstacles = 13  # Number of obstacles

# Obstacle locations (coordinates of their centers)
obstacles = [
    [0.61, 2.743], [0.915, 2.743], [1.219, 2.743], [1.829, 2.743],
    [1.829, 1.524], [1.829, 1.829], [1.829, 2.134], [2.743, 0.305],
    [2.743, 0.61], [2.743, 0.915], [2.743, 2.743], [3.048, 2.743],
    [3.353, 2.743], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
    [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
    [-1, -1], [-1, -1]
]

# Start and goal locations
start = [0.305, 1.219]
goal = [3.658, 1.829]



rear_motor = Motor(Port.A, Direction.CLOCKWISE)
front_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
watch = StopWatch() 

rear_motor.control.limits(acceleration=1000)
front_motor.control.limits(acceleration=1000)

def drive(rear_motor_speed, front_motor_speed):
    rear_motor.run(rear_motor_speed)
    front_motor.run(front_motor_speed)

watch.reset()
while watch.time() < 5000:
    drive(0, 300)
    wait(3000)
    drive(300, 0)
    wait(3000)
    drive(300, 300)
    wait(3000)
