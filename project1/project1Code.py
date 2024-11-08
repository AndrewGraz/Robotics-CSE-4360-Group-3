from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
import umath

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
    meters = 304.8
    distance = tiles*meters
    driver.straight(distance)

#make it to turn a perfect 90 
def turn(target_angle, speed=69):
    current_angle = hub.imu.heading()
    direction = 1 if target_angle < current_angle else -1

    while abs(hub.imu.heading() - target_angle) > 1:  # 1 degree tolerance
        left.run(direction * speed)
        right.run(-direction * speed)
    
    left.stop()
    right.stop()
    hub.imu.reset_heading(0)
   ###########################################################################

class tree:
    __slots__ = 'cell_coord', 'parent'
    def __init__(self,cell_coord):
        self.cell_coord = cell_coord
        self.parent = None
        #self.children = []

def main():
    possible_directions = [(-1,0),(1,0),(0,-1),(0,1)]    


    def drive_path(path):
        heading = 'x'
        for i in range(len(path) - 1):
            print(path)
            x1,y1 = path[i]
            x2,y2 = path[i+1]
            print(x1,y1)
            print(x2,y2)
            
            
            if((x2 - x1 == 1) or (x2 - x1 == -1)):
                if(heading == 'y'):
                    if(x2-x1 == 1):
                        turn(90)
                    if(x2-x1 == -1):
                        turn(-90)
                drive(1)
                heading = 'x'
            
            if((y2-y1 == 1) or (y2-y1 == -1)):
                if(heading == 'x'):
                    if(y2-y1 == 1):
                        turn(-90)
                    if(y2-y1 == -1):
                        turn(90)
                drive(1)
                heading = 'y'
           



    def bfs_search(start, goal, goal_size, free_cells):
        rt = tree(start)
        queue = [rt]
        visited_cells = [rt.cell_coord]
        c = 0
        while len(queue) != 0:
            c = c + 1
            print(c)
            curr = queue.pop(0)
            curr_cell = curr.cell_coord
            if(curr_cell == goal):
                print(f"Goal found")
                path = []
                while curr is not None:
                    #path.append(curr.cell_coord)
                    yield curr.cell_coord
                    curr = curr.parent
                
                return path[::-1]

            for x,y in possible_directions:
                adj_cell = (curr_cell[0] + x, curr_cell[1] + y)
                if adj_cell in free_cells and adj_cell not in visited_cells and 0 <= adj_cell[0] < int(grid_width/cell_len) and 0 <= adj_cell[1] < int(grid_height/cell_len):
                    adj = tree(adj_cell)
                    adj.parent = curr
                    #curr.children.append(adj)
                    queue.append(adj)
                    visited_cells.append(adj.cell_coord)

        print("No path to goal")
        return None

    cell_len = 1 #feet
    grid_height = 10  #feet
    grid_width = 16 
    feet_to_metres = 0.3048
    robot_max_dim = 0
    robot_max_dim_in_cells = robot_max_dim/cell_len
    obstacle_size = 1
    obstacle_size_in_cells = obstacle_size/cell_len


    start_loc = (0.305, 1.219)
    goal_loc_center = (3.658, 1.829)
    goal_radius = 1
    goal_radius_in_cells = goal_radius/cell_len

    start_loc_in_feet = (int(start_loc[0]/feet_to_metres), int(start_loc[1]/feet_to_metres))
    goal_loc_center_in_feet = (int(goal_loc_center[0]/feet_to_metres), int(goal_loc_center[1]/feet_to_metres))

    start_loc_in_cells = (int(start_loc_in_feet[0]//cell_len), int(start_loc_in_feet[1]//cell_len))
    goal_loc_center_in_cells = (int(goal_loc_center_in_feet[0]//cell_len), int(goal_loc_center_in_feet[1]//cell_len))

    occupied_cells = []
    #obstacles_center = [(0.61, 2.743),(0.915, 2.743),(1.219, 2.743),(1.829, 1.219),(1.829, 1.524),(1.829, 1.829), (1.829, 2.134),(2.743, 0.305),(2.743, 0.61),(2.743, 0.915),(2.743, 2.743),(3.048, 2.743),(3.353, 2.743)]
    #obstacles_center_in_feet = [(int(x//feet_to_metres), int(y//feet_to_metres)) for x,y in obstacles_center]
    obstacles_center_in_feet = [(1,1),(2,1),(1,2),(2,2),(2,7),(2,8),(5,4),(5,5),(5,6),(8,8),(8,2),(9,2),(10,2)]
    #obstacles_center_in_feet = [(0,0),(5,1),(5,2),(5,3),(5,4),(8,8),(16,10), (12,4), (11,4),(10,4), (9,5),(9,6)]
    obstacles_center_in_cells = []
    for i in range(len(obstacles_center_in_feet)):
        obstacles_center_in_cells.append((int(obstacles_center_in_feet[i][0]/cell_len),int(obstacles_center_in_feet[i][1]/cell_len)))

    all_cells = []
    for x in range(int(grid_width/cell_len)):
        for y in range(int(grid_height/cell_len)):
            all_cells.append((x,y))

    # print(f"____ALL_CELLS____")
    # for cell in all_cells:
    #     print(cell)
    # print("\n\n")


    for obstacle_center_x, obstacle_center_y in obstacles_center_in_cells:
        left_edge_obstacle = umath.floor(obstacle_center_x - obstacle_size_in_cells*0.5 - robot_max_dim_in_cells)
        right_edge_obstacle = umath.floor(obstacle_center_x + obstacle_size_in_cells*0.5 + robot_max_dim_in_cells -1)
        bottom_edge_obstacle = umath.floor(obstacle_center_y - obstacle_size_in_cells*0.5 - robot_max_dim_in_cells)
        top_edge_obstacle = umath.floor(obstacle_center_y + obstacle_size_in_cells*0.5 + robot_max_dim_in_cells -1)

        for x in range(left_edge_obstacle, right_edge_obstacle + 1):
            for y in range(bottom_edge_obstacle, top_edge_obstacle +1):
                if (x,y) not in occupied_cells:
                    occupied_cells.append((x,y))


    print(f"____OCCUPIED_CELLS____")
    for cell in occupied_cells:
        print(cell)
    print("\n\n")

    free_cells = []
    for cell in all_cells:
        if cell not in occupied_cells:
            if cell not in free_cells:
                free_cells.append(cell)

    print(f"All cells: {len(all_cells)}\nOccupied cells: {len(occupied_cells)}\nFree cells: {len(free_cells)}")


    print(f"start = {start_loc_in_cells}\ngoal={goal_loc_center_in_cells}\nradius = {goal_radius_in_cells}\nfree ={len(free_cells)}")
    #path = bfs_search(start_loc_in_cells, goal_loc_center_in_cells, goal_radius_in_cells, free_cells)
    path_generator = bfs_search(start_loc_in_cells, goal_loc_center_in_cells, goal_radius_in_cells, free_cells)
    if path_generator:
        path = list(path_generator)[::-1]
        drive_path(path)
        print("Path to goal", path)
    else:
        print("No path found")


main()
watch.reset()

