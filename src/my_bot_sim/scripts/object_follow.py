#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class object_follow(Node):
    def __init__(self):
        super().__init__("object_follow")
        self.sub = self.create_subscription(Float32MultiArray, '/object_info', self.follow, 10)
        self.setpoint = 180
        self.kp, self.ki, self.kd = 0.05, 0, 0.005
        self.previous_error = 0
        self.dt = 0.1
        self.integral = 0
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('following object started')
        self.pause = 0


    def pid_controller(self, setpoint, pv, kp, ki, kd, previous_error, integral, dt):
        error = pv-setpoint
        integral += error * dt
        derivative = (error - previous_error) / dt
        control = kp * error + kd * derivative
        return control, error, integral

    def follow(self,msg):
        try:
          if self.pause == 0:
               angle, dist = msg.data
               print(msg.data)
               cmd = Twist()
               tr = 180.0
               control, error, self.integral = self.pid_controller(tr, angle, self.kp, self.ki, self.kd, self.previous_error, self.integral, self.dt)
               self.previous_error = error
               
               if abs(error) > 2.0:
                    cmd.angular.z = control
               else:
                    cmd.angular.z = 0.0
               

               if dist > 1.8:
                    cmd.linear.x = 1.0
               else:
                    cmd.linear.x = 0.0
               self.get_logger().info(f'following object at {dist}')


               self.get_logger().info(f'pid:{control}')
               self.pub.publish(cmd)
        except KeyboardInterrupt:
             if self.pause == 0:
                  cmd.linear.x = 0.0
                  cmd.angular.z = 0.0
                  self.pause = 1
             else: 
                  self.pause = 0
             self.get_logger().info("objec following pause")

def main(args = None):
        rclpy.init(args=args)
        node = object_follow()

        rclpy.spin(node)
        rclpy.shutdown()

if __name__ == '__main__':
     main()