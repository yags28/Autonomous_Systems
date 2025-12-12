# Autonomous Systems

ROS 2 labs and final project from an Autonomous Systems course. All packages are built with `colcon` and tested on ROS 2 (Python).

---

## Lab 1 — ROS 2 Publisher/Subscriber & Services

**Location:** `Lab1/11/`

### Task 1 — Publisher & Subscriber
- `talker.py` publishes the node's uptime (seconds) to `/my_first_topic` at 10 Hz using `std_msgs/Float32`.
- `listener.py` subscribes to the topic and logs the doubled value.
- Launch: `ros2 launch task_1 pub_sub_launch.py`

### Task 2 — Custom Service
- Defines a custom `JointState.srv` interface with three float fields (`x`, `y`, `z`) and a boolean response (`valid`).
- `service.py` serves requests and returns `valid = True` if the sum of the three values is non-negative.
- `client.py` sends test requests to the service.
- Launch: `ros2 launch task_2 service_launch.py`

**Demo:** `Lab2/Lab2.mp4`

---

## Lab 2 — PID Speed Controller

**Location:** `Lab2/11/`

### Task 3 — PID Wall-Following
- `pid_speed_controller.py` uses a LaserScan subscriber and a `Twist` publisher to maintain a target distance of **0.35 m** from a wall using a PID controller (Kp=1.0, Kd=0.1).
- Subscribes to `/scan`, publishes to `/cmd_vel`.
- Launch: `ros2 launch task_3 pid_control_launch.py`

**Demo:** `Lab2/11/Lab2.mp4`

---

## Lab 3 — Autonomous Navigation with A\*

**Location:** `Lab3/11/`

### Task 4 — A\* Path Planning & Navigation
- `auto_navigator.py` implements an A\* planner on an inflated occupancy grid.
- Subscribes to `/map`, `/odom`, and `/scan`; publishes velocity commands to `/cmd_vel` and the planned path to `/path`.
- Obstacle inflation radius: 0.2 m. Goal tolerance: 0.1 m.
- Also includes a Jupyter notebook (`navigation_astar_f24.ipynb`) for offline A\* visualization.
- Launch: `ros2 launch task_4 gen_sync_map_launch.py`

**Demo:** `Lab3/11/Lab3_simulation.mp4`, `Lab3/11/Lab3_turtlebot.mp4`

---

## Lab 4 — Computer Vision & Object Tracking

**Location:** `Lab4/11/`

### Task 4 — Map-Based Navigation
- Continued autonomous navigation using a pre-built map.
- Launch: `ros2 launch task_4 gen_sync_map_launch.py`

### Task 5 — Object Detection
- `image_publisher.py` streams a video file to `/video_data`.
- `object_detector.py` uses OpenCV to detect objects in the stream and publishes bounding boxes to `/bbox` using `vision_msgs/BoundingBox2D`.
- Launch: `ros2 launch task_5 object_detector_launch.py`

### Task 6 — Red Ball Tracker
- `red_ball_tracker.py` subscribes to `/camera/image_raw`, detects a red ball using HSV color masking, and publishes velocity commands to `/cmd_vel` to track it.
- Forward speed: 0.2 m/s, Turn speed: 0.3 rad/s.
- Launch: `ros2 launch task_6 red_ball_tracker_launch.py`

**Demo:** `Lab4/11/Lab4.webm`

---

## Final Project — Autonomous Navigation in Gazebo House World

**Location:** `Final_Project/turtlebot3_gazebo/`

A full autonomous navigation stack for a TurtleBot3 Waffle in a simulated Gazebo house environment.

### Launch Commands
```bash
# Launch house world (no RViz)
ros2 launch turtlebot3_gazebo turtlebot3_house_norviz.launch.py

# Launch house world with Red Ball task
ros2 launch turtlebot3_gazebo task_6.launch.py
```

### Tasks
| Script | Description |
|--------|-------------|
| `task1.py` | Pure pursuit path following with A\* planning and obstacle inflation |
| `task2.py` | Autonomous navigation with goal waypoints |
| `task2_bonus.py` | Extended bonus navigation task |
| `task3.py` | Full navigation with dynamic obstacle handling |
| `spawn_objects.py` | Spawns colored objects (red, green, blue) into the Gazebo world |
| `static_obstacles.py` | Spawns static obstacles for testing |

### Maps
Pre-built maps of the house environment are located in `Final_Project/turtlebot3_gazebo/maps/`.

### Key Parameters (task1.py)
- Lookahead distance: 0.20 m
- Nominal speed: 0.20 m/s
- Obstacle inflation: 4 cells
- Goal tolerance: 0.10 m

---

## Dependencies

- ROS 2 (tested on Humble/Iron)
- `rclpy`, `sensor_msgs`, `geometry_msgs`, `nav_msgs`, `vision_msgs`
- OpenCV (`cv_bridge`, `cv2`)
- NumPy, SciPy
- Gazebo + `turtlebot3_gazebo`
