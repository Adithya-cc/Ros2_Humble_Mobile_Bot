#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class BallCircle(Node):
    def __init__(self):
        super().__init__('ball_circle_driver')
        # Matching your current topic list (global namespace)
        self.pub = self.create_publisher(Twist, 'ball/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_in_circle)
        self.get_logger().info("Moving in a circle... Press Ctrl+C to stop.")

    def move_in_circle(self):
        msg = Twist()
        
        # 1. Forward Speed (m/s)
        msg.linear.x = 1.2 
        
        # 2. Constant Turn Rate (rad/s)
        # Higher value = smaller circle
        msg.angular.z = 0.2  

        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = BallCircle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Send a stop command on exit
        stop_msg = Twist()
        node.pub.publish(stop_msg)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()


    """ros2 run gazebo_ros spawn_entity.py   -entity moving_ball   -file ~/ros2_ws/src/my_bot_sim/urdf/ball.urdf   -x 3.0 -y 0.0 -z 0.0
"""