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

FK_DEBUG = 0 # Change to '1' to print out stuff for Forward Kinematics
IK_DEBUG = 1 # Change to '1' to print out stuff for Inverse Kinematics

""" Rexarm Class """
class Rexarm():
    def __init__(self):

        """ Commanded Values """
        self.num_joints = 6
        self.joint_angles = [0.0] * self.num_joints # radians # FIXME: uncomment
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

    def plan_command(self):
        """ Command planned waypoints """
        pass

    def rexarm_fk(self, dh_table):
        """
        Calculates forward kinematics for rexarm
        takes a DH table filled with DH parameters of the arm
        and the link to return the position for
        returns a 4-tuple (x, y, z, phi) representing the pose of the 
        desired link
        """

        final_point = (np.matrix((0,0,0,1))).transpose()
        theta1 = dh_table[0][0]
        theta2 = dh_table[1][0]
        matrix0 = np.matrix(( (1,0,0,0), (0,0,1,0), (0,1,0,dh_table[0][1]), (0,0,0,1) ))
        matrix1 = np.matrix(( (math.cos(theta1),0,math.sin(theta1),0), (0,1,0,0), (-math.sin(theta1),0,math.cos(theta1),0), (0,0,0,1) ))
        matrix2 = np.matrix(( (math.cos(PI/2+theta2), -math.sin(PI/2+theta2), 0, math.cos(PI/2+theta2)*dh_table[1][1]), (math.sin(PI/2+theta2), math.cos(PI/2+theta2), 0, math.sin(PI/2+theta2)*dh_table[1][1]), (0,0,1,0), (0,0,0,1) ))
        matrix3 = self.link_fk(dh_table, 2)
        matrix4 = self.link_fk(dh_table, 3)

        if FK_DEBUG:
            print "\ndh_table:\n", dh_table        
            print "\nmatrix0:\n", matrix0
            print "\nmatrix1\n", matrix1
            print "\nmatrix2:\n", matrix2
            print "\n1st result:\n",(np.mat(matrix4) * final_point)
            print "\n2nd result:\n",(np.mat(matrix3)*(np.mat(matrix4) * final_point))
            print "\n3rd result:\n",np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point))
            print "\n4th result:\n",np.mat(matrix1) *(np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point)))
            print "\n5th result:\n",np.mat(matrix0)*(np.mat(matrix1) *(np.mat(matrix2)*(np.mat(matrix3)*(np.mat(matrix4) * final_point))))

        return (np.mat(matrix0) * (np.mat(matrix1) * (np.mat(matrix2) * (np.mat(matrix3) * (np.mat(matrix4) * final_point)))))
 
    def link_fk(self, dh_table, link): 
        theta = dh_table[link][0]
        d = dh_table[link][1]
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
        print "________________________________________"
        print "IK: Started"

        x_g = pose[0]
        y_g = pose[1]
        z_g = pose[2]
        phi = pose[3]
        L1 = cfg[0]
        L2 = cfg[1]
        L3 = cfg[2]
        L4 = cfg[3]

        if IK_DEBUG:
            print "\nx_g:", x_g
            print "y_g:", y_g
            print "z_g:", z_g
            print "phi:", phi
            print "L1:", L1
            print "L2:", L2
            print "L3:", L3
            print "L4:", L4

        theta1 = -1*math.atan2(y_g,x_g)
        r_g = math.sqrt(x_g*x_g + y_g*y_g)
            
        z_g_prime = z_g + L4*math.sin(phi)
        r_g_prime  = r_g - L4*math.cos(phi)

        delta_z = z_g_prime - L1
        delta_r = r_g_prime

        if IK_DEBUG:
            print "\ntheta1:", round(theta1,3)
            print "r_g:", round(r_g,3)
            print "z_g_prime:", round(z_g_prime,3)
            print "r_g_prime:", round(r_g_prime,3)
            print "delta_z:", round(delta_z,3)
            print "delta_r:", round(delta_r,3)

        cos_theta3 = math.cos( (delta_z*delta_z + delta_r*delta_r - L2*L2 - L3*L3) / (2*L2*L3) )
        if IK_DEBUG:
            print "cos_theta3:", round(cos_theta3,3)
        if cos_theta3 > 1 or cos_theta3 < -1:
            print "\nERROR: cos(theta3) lies outside of [-1, 1]\ncos(theta3) =", cos_theta3
        theta3 = math.acos(cos_theta3) - PI/2 # theta3 needs to be in [-PI/2, PI/2]

        beta = math.atan2(delta_z, delta_r)
        cos_psi = math.cos( (L3*L3 - (delta_z*delta_z + delta_r*delta_r) - L2*L2) / (-2*math.sqrt(delta_z*delta_z + delta_r*delta_r)*L2) )
        if cos_psi > 1 or cos_psi < -1:
            print "\nERROR: cos(psi) lies outside of [-1, 1]\ncos(psi) =", cos_psi
        psi = math.acos( cos_psi ) - PI/2
        
        if theta3 >= 0:
            theta2 = PI/2 - beta - psi # "Elbow-up" 
        else:
            theta2 = PI/2 - beta + psi # "Elbow-down"

        theta4 = phi - theta2 - theta3 + PI/2 

        if IK_DEBUG:
            print "\ntheta3:", round(theta3,3)
            print "beta:", round(beta,3)
            print "psi:", round(psi,3)
            print "theta2:", round(theta2,3)
            print "theta4:", round(theta4,3)

        print "\nIK: Done"
        print "________________________________________"
        return [theta1, theta2, theta3, theta4]

    def rexarm_collision_check(q):
        """
        Perform a collision check with the ground and the base
        takes a 4-tuple of joint angles q
        returns true if no collision occurs
        """
        pass 
