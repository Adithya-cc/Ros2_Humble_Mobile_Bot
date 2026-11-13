#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan   
from std_msgs.msg import Float32MultiArray
import math


class LifarFilter(Node):
    def __init__(self):
        super().__init__('lidarfilter')
        self.subscription = self.create_subscription(LaserScan, '/scan', self.filter_callback, 10)

        self.publisher_ = self.create_publisher(Float32MultiArray,'/closest_objet_distance', 10)
        self.get_logger().info('Lidar Filter is online!')

    def filter_callback(self, msg):
        range_angle = 15.0
        angle_rad = range_angle*(math.pi/180.0)

        center_ind = len(msg.ranges)//2

        steps = int(angle_rad/ msg.angle_increment)

        start_ind = center_ind - steps
        end_ind  = center_ind + steps


        range = msg.ranges[start_ind:end_ind]

        valid_range = []
        for r in range:
            if math.isfinite(r) and r > msg.range_min:
                valid_range.append(r)



        if valid_range:
            closest_dist = min(valid_range)
            valid_range.sort()
            median = valid_range[len(valid_range)//2]
            average = sum(valid_range)/len(valid_range)



            array = [float(median), float(closest_dist), float(average)]
            dist_msg = Float32MultiArray()
            dist_msg.data = array
            self.publisher_.publish(dist_msg)


            self.get_logger().info(f'Distance of object in front: median {median:.2f}m, average {average:.2f}m, minimum {closest_dist:.2f}m')
        else:
            self.get_logger().warn("Path is clear No Object in front")


def main(args = None):
    rclpy.init(args=args)
    node = LifarFilter()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()