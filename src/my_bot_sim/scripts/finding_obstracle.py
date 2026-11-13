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

        self.pub = self.create_publisher(Float32MultiArray, '/object_info', 10)
        self.get_logger().info('obstracle finder online')

    def callback(self, msg):
        range = msg.ranges
        vld_range = []
        for r in range:
            if math.isfinite(r) and r > msg.range_min:
                vld_range.append(r)                


        if vld_range:
            min_dist = min(vld_range)
            index = range.index(min_dist)
            ang_rad = msg.range_min + (index * msg.angle_increment)
            angle = math.degrees(ang_rad)
            msg_out = Float32MultiArray()
            msg_out.data = [angle, min_dist]
            self.pub.publish(msg_out)
            self.get_logger().info(f'min distance: {min_dist}, angle = {angle}')

        else:
            msg_out = Float32MultiArray()
            msg_out.data = [180.0, 0.0]
            self.pub.publish(msg_out)
            self.get_logger().info('No valid object detected')
        
        


def main(args = None):
    rclpy.init(args = args)
    node = obstacle_detection()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()