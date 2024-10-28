import math
import matplotlib.pyplot as plt
class tree:
    def __init__(self,cell_coord):
        self.cell_coord = cell_coord
        self.parent = None
        self.children = []

possible_directions = [(-1,0),(1,0),(0,-1),(0,1)]    

def bfs_search(start, goal, goal_size, free_cells):
    rt = tree(start)
    queue = [rt]
    visited_cells = [rt.cell_coord]

    while len(queue) != 0:
        curr = queue.pop(0)
        curr_cell = curr.cell_coord
        if(curr_cell == goal):
            print(f"Goal found")
            path = []
            while curr is not None:
                path.append(curr.cell_coord)
                curr = curr.parent
            
            return path[::-1]

        for x,y in possible_directions:
            adj_cell = (curr_cell[0] + x, curr_cell[1] + y)
            if adj_cell in free_cells and adj_cell not in visited_cells and 0 <= adj_cell[0] < int(grid_width/cell_len) and 0 <= adj_cell[1] < int(grid_height/cell_len):
                adj = tree(adj_cell)
                adj.parent = curr
                curr.children.append(adj)
                queue.append(adj)
                visited_cells.append(adj.cell_coord)

    print("No path to goal")
    return None

cell_len = 0.5 #feet
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
    left_edge_obstacle = math.floor(obstacle_center_x - obstacle_size_in_cells*0.5 - robot_max_dim_in_cells)
    right_edge_obstacle = math.floor(obstacle_center_x + obstacle_size_in_cells*0.5 + robot_max_dim_in_cells -1)
    bottom_edge_obstacle = math.floor(obstacle_center_y - obstacle_size_in_cells*0.5 - robot_max_dim_in_cells)
    top_edge_obstacle = math.floor(obstacle_center_y + obstacle_size_in_cells*0.5 + robot_max_dim_in_cells -1)

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

# print(f"____FREE_CELLS____")
# for cell in free_cells:
#     print(cell)
# print("\n\n")

print(f"All cells: {len(all_cells)}\nOccupied cells: {len(occupied_cells)}\nFree cells: {len(free_cells)}")


print(f"start = {start_loc_in_cells}\ngoal={goal_loc_center_in_cells}\nradius = {goal_radius_in_cells}\nfree ={len(free_cells)}")
path = bfs_search(start_loc_in_cells, goal_loc_center_in_cells, goal_radius_in_cells, free_cells)
#path = []
#for p in path:
    #print(p)

fig, ax = plt.subplots(figsize=(10, 6))

# Draw grid lines with updated cell size of 0.5 feet
for x in range(int(grid_width / cell_len) + 1):
    ax.plot([x * cell_len, x * cell_len], [0, grid_height], color="black", linewidth=0.5)
for y in range(int(grid_height / cell_len) + 1):
    ax.plot([0, grid_width], [y * cell_len, y * cell_len], color="black", linewidth=0.5)

# Draw occupied cells (obstacles) scaled by cell_len
for ox, oy in occupied_cells:
    occupied_square = plt.Rectangle((ox * cell_len, oy * cell_len), cell_len, cell_len, color="black")
    ax.add_patch(occupied_square)

# Draw obstacle centers
for cx, cy in obstacles_center_in_cells:
    ax.plot(cx * cell_len, cy * cell_len, 'ro')  # Adjust to new cell_len for alignment

# Draw start location in green
ax.plot(start_loc_in_cells[0] * cell_len, start_loc_in_cells[1] * cell_len, 'go', markersize=8)

# Draw goal location as a blue circle with radius goal_radius
goal_circle = plt.Circle((goal_loc_center_in_cells[0] * cell_len, goal_loc_center_in_cells[1] * cell_len),
                         goal_radius, color="blue", fill=True, linewidth=2)
ax.add_patch(goal_circle)

# Draw path in orange
if path:
    for px, py in path:
        path_square = plt.Rectangle((px * cell_len, py * cell_len), cell_len, cell_len, color="orange", alpha=0.6)
        ax.add_patch(path_square)

# Set plot limits and labels
ax.set_xlim(0, grid_width)
ax.set_ylim(0, grid_height)
ax.set_aspect("equal")
ax.set_xlabel("X-axis (feet)")
ax.set_ylabel("Y-axis (feet)")

plt.show()



#############_______________FOR VISUALIZATION_________________________________________############################
# fig, ax = plt.subplots(figsize=(10, 6))

# # Draw grid
# for x in range(int(grid_width / cell_len) + 1):
#     ax.plot([x * cell_len, x * cell_len], [0, grid_height], color="black", linewidth=0.5)
# for y in range(int(grid_height / cell_len) + 1):
#     ax.plot([0, grid_width], [y * cell_len, y * cell_len], color="black", linewidth=0.5)

# # Draw occupied cells (obstacles)
# for ox, oy in occupied_cells:
#     occupied_square = plt.Rectangle((ox * cell_len, oy * cell_len), cell_len, cell_len, color="black")
#     ax.add_patch(occupied_square)

# # Draw obstacles centers
# for cx, cy in obstacles_center_in_cells:
#     ax.plot(cx * cell_len, cy * cell_len, 'ro')  # scaled by cell_len to match the plot

# # Draw start location in green
# ax.plot(start_loc_in_cells[0] * cell_len, start_loc_in_cells[1] * cell_len, 'go', markersize=8)

# # Draw goal location as a blue circle
# goal_circle = plt.Circle((goal_loc_center_in_cells[0] * cell_len, goal_loc_center_in_cells[1] * cell_len),
#                          goal_radius, color="blue", fill=True, linewidth=2)
# ax.add_patch(goal_circle)

# # Draw path in orange
# if path:
#     for px, py in path:
#         path_square = plt.Rectangle((px * cell_len, py * cell_len), cell_len, cell_len, color="orange", alpha=0.6)
#         ax.add_patch(path_square)

# # Set plot limits and labels
# ax.set_xlim(0, grid_width)
# ax.set_ylim(0, grid_height)
# ax.set_aspect("equal")
# ax.set_xlabel("X-axis (feet)")
# ax.set_ylabel("Y-axis (feet)")

# plt.show()


#############_______________FOR VISUALIZATION_________________________________________############################
# fig, ax = plt.subplots(figsize=(10, 6))
# for x in range(int(grid_width / cell_len) + 1):
#     ax.plot([x * cell_len, x * cell_len], [0, grid_height], color="black", linewidth=0.5)
# for y in range(int(grid_height / cell_len) + 1):
#     ax.plot([0, grid_width], [y * cell_len, y * cell_len], color="black", linewidth=0.5)
# for ox, oy in occupied_cells:
#     occupied_square = plt.Rectangle((ox * cell_len, oy * cell_len), cell_len, cell_len, color="black")
#     ax.add_patch(occupied_square)
# for cx, cy in obstacles_center_in_cells:
#     ax.plot(cx * cell_len, cy * cell_len, 'ro')  # scaled by cell_len to match the plot
# ax.plot(start_loc_in_cells[0] * cell_len, start_loc_in_cells[1] * cell_len, 'go', markersize=8)
# goal_circle = plt.Circle((goal_loc_center_in_cells[0] * cell_len, goal_loc_center_in_cells[1] * cell_len),
#                          goal_radius, color="blue", fill=True, linewidth=2)
# ax.add_patch(goal_circle)
# ax.set_xlim(0, grid_width)
# ax.set_ylim(0, grid_height)
# ax.set_aspect("equal")
# ax.set_xlabel("X-axis (feet)")
# ax.set_ylabel("Y-axis (feet)")

# plt.show()
