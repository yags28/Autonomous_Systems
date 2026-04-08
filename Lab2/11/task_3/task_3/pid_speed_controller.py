import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class PIDControllerNode(Node):
    def __init__(self):
        super().__init__('pid_speed_controller')

        # --- Subscriber, Publisher, and Timer ---
        self.scan_subscriber = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.velocity_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # --- Control Loop Timer ---
        self.timer_period = 0.1  
        self.timer = self.create_timer(self.timer_period, self.control_loop_callback)

        # --- PID Parameters ---
        self.setpoint = 0.35  
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.1
        
        # PID state variables
        self.last_error = 0.0
        self.integral = 0.0
        
        # --- State and Safety ---
        self.current_distance = 0.0
        self.is_lidar_ready = False
        
        # Max linear speed set to 0.15 m/s 
        self.max_velocity = 0.15
        self.integral_cap = 1.0

        self.get_logger().info('PID Controller Node has been started.')

    def scan_callback(self, msg):
        forward_distance = msg.ranges[0]
        
        if math.isfinite(forward_distance):
            self.current_distance = forward_distance
            if not self.is_lidar_ready:
                self.is_lidar_ready = True
                self.get_logger().info(f'Lidar data received. Target distance: {self.setpoint} m')

    def control_loop_callback(self):
        if not self.is_lidar_ready:
            return

        # PID Calculation...
        error = self.current_distance - self.setpoint
        self.integral += error * self.timer_period
        self.integral = max(min(self.integral, self.integral_cap), -self.integral_cap)
        
        # Clamping
        derivative = (error - self.last_error) / self.timer_period
        output_velocity = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.last_error = error
        
        # --- Create and Publish Twist Message ---
        twist_msg = Twist()
        twist_msg.linear.x = max(0.0, min(output_velocity, self.max_velocity))
        twist_msg.angular.z = 0.0 
        self.velocity_publisher.publish(twist_msg)
        self.get_logger().info(f'Dist: {self.current_distance:.2f}, Err: {error:.2f}, Vel: {twist_msg.linear.x:.2f}')


def main(args=None):
    rclpy.init(args=args)
    pid_speed_controller = PIDControllerNode()
    rclpy.spin(pid_speed_controller)
    pid_speed_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
