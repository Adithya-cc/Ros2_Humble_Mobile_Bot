#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
import math


class obstacle_detection(Node):
    def __init__(self):
        super().__init__('findobstracle')
        self.sub = self.create_subscription(LaserScan, '/scan', self.callback, 10)
        self.objects = {}
        self.pub = self.create_publisher(Float32MultiArray, '/object_info', 10)
        self.get_logger().info('obstracle finder online')

    def callback(self, msg):
        angdis = []
        objects= []
        prev_r = None
        DIST_JUMP = 0.3        # meters (tune this)
        MIN_POINTS = 3        # minimum rays per object
        current_object = []
        for ind, r in enumerate(msg.ranges):
            if math.isfinite(r) and r > msg.range_min:
                angle = msg.angle_min + ind * msg.angle_increment
                angdis.append((math.degrees(angle), r))
                    

        """if vld_range:
            min_dist = min(vld_range)
            index = range.index(min_dist)
            ang_rad = msg.range_min + (index * msg.angle_increment)
            angle = math.degrees(ang_rad)
            msg_out = Float32MultiArray()
            msg_out.data = [angle, min_dist]
            self.pub.publish(msg_out)
            self.get_logger().info(f'min distance: {min_dist}, angle = {angle}')

        else:
            self.get_logger().info('No valid object detected')
        """
        


def main(args = None):
    rclpy.init(args = args)
    node = obstacle_detection()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()