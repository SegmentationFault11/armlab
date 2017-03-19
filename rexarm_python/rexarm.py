import lcm
import time
import numpy as np
import math

from lcmtypes import dynamixel_command_t
from lcmtypes import dynamixel_command_list_t
from lcmtypes import dynamixel_status_t
from lcmtypes import dynamixel_status_list_t

PI = np.pi
D2R = PI/180.0
ANGLE_TOL = 2*PI/180.0 


""" Rexarm Class """
class Rexarm():
    def __init__(self):

        """ Commanded Values """
        self.num_joints = 6
        self.joint_angles = [0.0] * self.num_joints # radians
        # you must change this to control each joint speed separately 
        self.speed = 0.5                         # 0 to 1
        self.max_torque = 0.5                    # 0 to 1

        """ Feedback Values """
        self.joint_angles_fb = [0.0] * self.num_joints # radians
        self.speed_fb = [0.0] * self.num_joints        # 0 to 1   
        self.load_fb = [0.0] * self.num_joints         # -1 to 1  
        self.temp_fb = [0.0] * self.num_joints         # Celsius               

        """ Waypoint Plan - TO BE USED LATER """
        self.plan = []
        self.plan_status = 0
        self.wpt_number = 0
        self.wpt_total = 0

        """ Setup LCM and subscribe """
        self.lc = lcm.LCM()
        lcmMotorSub = self.lc.subscribe("ARM_STATUS",
                                        self.feedback_handler)

    def cmd_publish(self):
        """ 
        Publish the commands to the arm using LCM. 
        You need to activelly call this function to command the arm.
        You can uncomment the print statement to check commanded values.
        """    
        msg = dynamixel_command_list_t()
        msg.len = 6
        self.clamp()
        for i in range(msg.len):
            cmd = dynamixel_command_t()
            cmd.utime = int(time.time() * 1e6)
            cmd.position_radians = self.joint_angles[i]
            # you SHOULD change this to contorl each joint speed separately 
            cmd.speed = self.speed
            cmd.max_torque = self.max_torque
            #print cmd.position_radians
            msg.commands.append(cmd)
        self.lc.publish("ARM_COMMAND",msg.encode())
    
    def get_feedback(self):
        """
        LCM Handler function
        Called continuously from the GUI 
        """
        self.lc.handle_timeout(50)

    def feedback_handler(self, channel, data):
        """
        Feedback Handler for LCM
        """
        msg = dynamixel_status_list_t.decode(data)
        for i in range(msg.len):
            self.joint_angles_fb[i] = msg.statuses[i].position_radians 
            self.speed_fb[i] = msg.statuses[i].speed 
            self.load_fb[i] = msg.statuses[i].load 
            self.temp_fb[i] = msg.statuses[i].temperature

    def clamp(self):
        """
        Clamp Function
        Limit the commanded joint angles to ones physically possible so the 
        arm is not damaged.
        LAB TASK: IMPLEMENT A CLAMP FUNCTION
        """
        if self.joint_angles[1] > 120*D2R:
            self.joint_angles[1] = 120*D2R
        if self.joint_angles[2] > 115*D2R:
            self.joint_angles[2] = 115*D2R
        if self.joint_angles[3] > 120*D2R:
            self.joint_angles[3] = 120*D2R

        if self.joint_angles[1] < -120*D2R:
            self.joint_angles[1] = -120*D2R
        if self.joint_angles[2] < -120*D2R:
            self.joint_angles[2] = -120*D2R
        if self.joint_angles[3] < -120*D2R:
            self.joint_angles[3] = 120*D2R
        print self.joint_angles[1]

    def plan_command(self):
        """ Command planned waypoints """
        pass

    def rexarm_fk(self,dh_table):
        print dh_table
        final_point = np.matrix((0,0,0,1))
        final_point = final_point.transpose()
        print "dh_table[0][0] "
        print dh_table[0][0]
        theta1 = dh_table[0][0]
        theta2 = dh_table[1][0]
        print "Theta 1", theta1
        matrix1_1 = np.matrix(((1,0,0,0), (0,0,1,0), (0,1,0,dh_table[0][1]), (0,0,0,1)))
        matrix1_2 = np.matrix(((math.cos(theta1),0,math.sin(theta1),0), (0,1,0,0), (-math.sin(theta1),0,math.cos(theta1),0), (0,0,0,1)))
        matrix2 = np.matrix(((math.cos(PI/2+theta2), -math.sin(PI/2+theta2), 0, math.cos(PI/2+theta2)*dh_table[1][1]), (math.sin(PI/2+theta2), math.cos(PI/2+theta2), 0, math.sin(PI/2+theta2)*dh_table[1][1]), (0,0,1,0), (0,0,0,1)))
        #matrix2 = self.link_fk(dh_table, 1)
        matrix3 = self.link_fk(dh_table, 2)
        matrix4 = self.link_fk(dh_table, 3)
        print "MATRIX1_1 "
        print matrix1_1
        print "MATRIX1_2 "
        print matrix1_2
        print "MATRIX2 "
        print matrix2
        print "first RESULT\n",(np.mat(matrix4) * final_point)
        print "second RESULT\n",(np.mat(matrix3)*(np.mat(matrix4) * final_point))
        print "3rd RESULT\n",np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point))
        print "4th RESULT\n",np.mat(matrix1_2) *(np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point)))
        print "5th RESULT\n",np.mat(matrix1_1)*(np.mat(matrix1_2) *(np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point))))
        return (np.mat(matrix1_1)*(np.mat(matrix1_2) *(np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point)))))
 
    def link_fk(self, dh_table, link): 
        """
        Calculates forward kinematics for rexarm
        takes a DH table filled with DH parameters of the arm
        and the link to return the position for
        returns a 4-tuple (x, y, z, phi) representing the pose of the 
        desired link
        """
        # link = [index, whether it i]
        print dh_table[link]
        theta = dh_table[link][0]
        d = dh_table[link][1]
        print "link ", link, "theta ", theta
        print theta, math.cos(theta)
        if link == 0:
            return np.array(((math.cos(theta), 0, 0, -math.sin(theta)), (0, 1, 0, 0), (math.sin(theta),0,math.cos(theta),0), (0,0,0,1)))
        else:
    	   return np.array(((math.cos(theta), -math.sin(theta), 0, math.cos(theta)*d), (math.sin(theta), math.cos(theta), 0, math.sin(theta)*d), (0,0,1,0), (0,0,0,1)))
    def rexarm_ik(self, pose, cfg):
        """
        Calculates inverse kinematics for the rexarm
        pose is a tuple (x, y, z, phi) which describes the desired
        end effector position and orientation.  
        cfg describe elbow down (0) or elbow up (1) configuration
        returns a 4-tuple of joint angles or NONE if configuration is impossible
        """
        x_g = pose[0]
        y_g = pose[1]
        z_g = pose[2]
        phi = pose[3]
        print "x_g", x_g
        print "y_g", y_g
        print "z_g", z_g
        print "phi", phi
        
        L1 = cfg[0]
        L2 = cfg[1]
        L3 = cfg[2]
        L4 = cfg[3]
        print "L1", L1
        print "L2", L2
        print "L3", L3
        print "L4", L4
        z_g_prime = z_g + L4*math.sin(phi)
        r_g_prime  = math.sqrt(math.pow(x_g, 2) + math.pow(y_g, 2)) - L4*math.cos(phi)
        delta_z = z_g_prime - L1
        delta_r = r_g_prime
        print "z_g_prime", z_g_prime
        print "g_g",math.sqrt(math.pow(x_g, 2) + math.pow(y_g, 2))
        print "r_g_prime", r_g_prime
        print "delta_z", delta_z
        print "delta_r", delta_r 
        # theta3 in [0, pi]
        print "delta_z^2", math.pow(delta_z,2)
        print "delta_r^2", math.pow(delta_r,2)
        print "L2^2", math.pow(L2,2)
        print "L3^2", math.pow(L3,2)
        print "ACOS THETA",(math.pow(delta_z,2)+math.pow(delta_r,2)-math.pow(L2,2)-math.pow(L3,2))/(2*L2*L3)
        theta3 = math.acos((math.pow(delta_z,2)+math.pow(delta_r,2)-math.pow(L2,2)-math.pow(L3,2))/(2*L2*L3))
        # theta3 in [-pi/2, pi/2]
        theta3 = theta3 - PI/2
        beta = math.atan2(delta_z,delta_r)
        psi = math.acos((L3*L3-(delta_z*delta_z+delta_r*delta_r)-L2*L2)/(-2*math.sqrt(delta_z*delta_z+delta_r*delta_r)*L2))
        theta2 = 0.0
        if theta3 >= 0:
            theta2 = PI/2-beta-psi
        else:
            theta2 = PI/2-beta+psi
        theta4 = phi-theta2-theta3+PI/2
        theta1 = math.atan2(y_g,x_g)
        return [theta1, theta2, theta3, theta4]

    def rexarm_collision_check(q):
        """
        Perform a collision check with the ground and the base
        takes a 4-tuple of joint angles q
        returns true if no collision occurs
        """
        pass 
