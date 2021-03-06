import sys, os, inspect, thread, math, serial
import cv2
from lcm import LCM
import numpy as np
from time import sleep
from PyQt4 import QtGui, QtCore, Qt
from ui import Ui_MainWindow
from rexarm import Rexarm
from decimal import *
import time
from video import Video
from threading import Lock

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=2) # FIXME: uncomment
ser.isOpen() # FIXME: uncomment

""" Radians to/from  Degrees conversions """
D2R = 3.141592/180.0
R2D = 180.0/3.141592
PI = np.pi
#[0.19973263883694628, 0.0016855746897424617, 0.06664578153381727, -0.15], # new HOME
""" Pyxel Positions of image in GUI """
MIN_X = 310
MAX_X = 950

MIN_Y = 30
MAX_Y = 510

""" Link lengths of arm """
OFFSET = 7.50 / 100
LINK1_LENGTH = 4.50 / 100
LINK2_LENGTH = 10.00 / 100
LINK3_LENGTH = 10.00 / 100
LINK4_LENGTH = 7 / 100 # TODO: change this to our gripper
cfg = [LINK1_LENGTH + OFFSET, LINK2_LENGTH, LINK3_LENGTH, LINK4_LENGTH, 0] # Lengths of the links

FK_DEBUG = 0 # Change to '1' to print out stuff for Forward Kinematics
IK_DEBUG = 0 # Change to '1' to print out stuff for Inverse Kinematics
LCM_DEBUG = 0 # Change to '1' to print out stuff for LCM
MIX_DEBUG = 1

lock = Lock()
ERROR_IF_REACHED = 0.01

FINAL_END_EFFECTORS = [
    [0.10125143894897511, -0.12094915633605999, 0.18061180478670984, -0.15],
    [0.021227449684100921, -0.16329518003527718, 0.18061180478670984, -0.15],
    [-0.070747536793389756, -0.14850850805866353, 0.18061180478670984, -0.15],
    [-0.13855895338992918, -0.088664577840474698, 0.18061180478670984, -0.15],
    [-0.16497080154134619, 0.00050624926499197244, 0.18061180478670984, -0.15],
    [-0.14187864044490325, 0.084178815832835346, 0.18061180478670984, -0.15],
    [-0.072391107920756079, 0.14014306904605794, 0.18061180478670984, -0.15],
    [0.012632140474910281, 0.15722907280355261, 0.18061180478670984, -0.15],
    [0.093447433342095709, 0.12707529071151988, 0.18061180478670984, -0.15],
    [0.1903263883694628, 0.0016855746897424617, 0.15664578153381727, -0.15], # HOME 1
    [0.1903263883694628, 0.0016855746897424617, 0.06664578153381727, -0.15], # HOME 2
    [10, 10, 10, 10] # GARBAGE
]

MIX_RADIUS = 0.03
MIX_CENTER = [0.119176, -0.01154, 0.18061180478670984, -0.15]
# MIX_CENTER = [0.12, 0.00154, 0.20749, -0.15]
NUMBER_OF_POINTS = 16
CHANGE_IN_ANGLE = 2*PI/NUMBER_OF_POINTS
MIX_PHI = []
MIX_END_EFFECTORS = []
for i in range(NUMBER_OF_POINTS):
    MIX_PHI.append(CHANGE_IN_ANGLE*i)
    MIX_END_EFFECTORS.append([0,0,0])


# import LCM packages
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from lcm_python import arm_command_t    

current_hole_index = 10
is_reached_current_bottle = 0
goal_ee = [0.0, 0.0, 0.0]

def arm_handler(channel, data):
    global current_hole_index, is_reached_current_bottle, goal_ee
    goal_ee = [0.0, 0.0, 0.0]
    current_hole_index = 10
    is_reached_current_bottle = 0
    msg = arm_command_t.arm_command_t.decode(data)
    if LCM_DEBUG:
        print "\nMessage Received"
        print "Size:", msg.size
        print "Hole Indices:", msg.hole_indices
        print "Stop Times:", msg.stop_times
    hole_indices = []
    for i in range(msg.size):
        hole_indices.append(msg.hole_indices[i])
    hole_indices_sorted = sorted(hole_indices)
    # add another point before going out of home
    hole_indices_sorted = [9] + hole_indices_sorted

    for i in range(msg.size+1):
        # if (i == 1):
        #     ex.change_speed(12)
        current_hole_index = hole_indices_sorted[i]
        print "TEST 1"
        ex.driveToBottle(FINAL_END_EFFECTORS[current_hole_index])
        print "TEST 2"
        while True:
            lock.acquire()
            if is_reached_current_bottle == 0:
                lock.release()
                continue
            else:
                lock.release()
                break
        
        if (i == 0):
            time.sleep(0.5)
        else:
            ser.write(chr(ord('0') + current_hole_index))
            time.sleep(msg.stop_times[hole_indices.index(hole_indices_sorted[i])])  
            ser.write(chr(ord('a') + current_hole_index))
            time.sleep(1.0)

        is_reached_current_bottle = 0
    # ex.driveToHome() # Drive home
    
    if (msg.size > 1):
        ex.mixDrink()
    else:
        ex.driveToHome()


def handle_lcm():
    lc = LCM()
    subscription = lc.subscribe('ARM', arm_handler)
    print 'Subscribed to the ARM channel, waiting for command...'
    while True:
        lc.handle()

thread.start_new_thread( handle_lcm, () )

class Gui(QtGui.QMainWindow):
    """ 
    Main GUI Class
    It contains the main function and interfaces between 
    the GUI and functions
    """
    def __init__(self,parent=None):
        print 'TEST INITial'
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Main Variables Using Other Classes"""
        self.rex = Rexarm()
        self.video = Video(cv2.VideoCapture(0))

        """ Other Variables """
        self.last_click = np.float32([0,0])

        """ Set GUI to track mouse """
        QtGui.QWidget.setMouseTracking(self,True)

        """ 
        Video Function 
        Creates a timer and calls play() function 
        according to the given time delay (27mm) 
        """
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
       
        """ 
        LCM Arm Feedback
        Creates a timer to call LCM handler continuously
        No delay implemented. Reads all time 
        """  
        self._timer2 = QtCore.QTimer(self)
        self._timer2.timeout.connect(self.rex.get_feedback)
        self._timer2.start()

        """ 
        Connect Sliders to Function
        LAB TASK: CONNECT THE OTHER 5 SLIDERS IMPLEMENTED IN THE GUI 
        """ 
        self.ui.sldrShoulder.setValue(-112.1)
        self.ui.sldrElbow.setValue(10.8)
        self.ui.sldrWrist.setValue(18.4)
        self.ui.sldrMaxTorque.setValue(90)
        self.ui.sldrSpeed.setValue(12)

        self.ui.sldrBase.valueChanged.connect(self.sliderChange)
        self.ui.sldrShoulder.valueChanged.connect(self.sliderChange)
        self.ui.sldrElbow.valueChanged.connect(self.sliderChange)
        self.ui.sldrWrist.valueChanged.connect(self.sliderChange)
        self.ui.sldrMaxTorque.valueChanged.connect(self.sliderChange)
        self.ui.sldrSpeed.valueChanged.connect(self.sliderChange)

        """ Commands the arm as the arm initialize to 0,0,0,0 angles """
        self.sliderChange() 
        
        """ Connect Buttons to Functions 
        LAB TASK: NAME AND CONNECT BUTTONS AS NEEDED
        """
        self.ui.btnUser1.setText("Check Pressure Sensor")
        self.ui.btnUser1.clicked.connect(self.isPressureSensorOccupied)

        self.ui.btnUser2.setText("Mix Drink")
        self.ui.btnUser2.clicked.connect(self.mixDrink)

        self.ui.btnUser3.setText("Home")
        self.ui.btnUser3.clicked.connect(self.driveToHome)

        self.ui.btnUser4.setText("Bottle 0")
        self.ui.btnUser4.clicked.connect(self.driveToBottle0)

        self.ui.btnUser5.setText("Bottle 1")
        self.ui.btnUser5.clicked.connect(self.driveToBottle1)

        self.ui.btnUser6.setText("Bottle 2")
        self.ui.btnUser6.clicked.connect(self.driveToBottle2)

        self.ui.btnUser7.setText("Bottle 3")
        self.ui.btnUser7.clicked.connect(self.driveToBottle3)

        self.ui.btnUser8.setText("Bottle 4")
        self.ui.btnUser8.clicked.connect(self.driveToBottle4)

        self.ui.btnUser9.setText("Bottle 5")
        self.ui.btnUser9.clicked.connect(self.driveToBottle5)

        self.ui.btnUser10.setText("Bottle 6")
        self.ui.btnUser10.clicked.connect(self.driveToBottle6)

        self.ui.btnUser11.setText("Bottle 7")
        self.ui.btnUser11.clicked.connect(self.driveToBottle7)

        self.ui.btnUser12.setText("Bottle 8")
        self.ui.btnUser12.clicked.connect(self.driveToBottle8)
    
    def play(self):
        """ 
        Play Funtion
        Continuously called by GUI 
        """

        """ Renders the Video Frame """
        # try:
        #     self.video.captureNextFrame()
        #     self.video.blobDetector()
        #     self.ui.videoFrame.setPixmap(
        #         self.video.convertFrame())
        #     self.ui.videoFrame.setScaledContents(True)
        # except TypeError:
        #     print "No frame"
        
        """ 
        Update GUI Joint Coordinates Labels
        LAB TASK: include the other slider labels 
        """
        self.ui.rdoutBaseJC.setText(str("%.2f" % (self.rex.joint_angles_fb[0]*R2D)))
        self.ui.rdoutShoulderJC.setText(str("%.2f" % (-1*self.rex.joint_angles_fb[1]*R2D)))
        self.ui.rdoutElbowJC.setText(str("%.2f" % (-1*self.rex.joint_angles_fb[2]*R2D)))
        self.ui.rdoutWristJC.setText(str("%.2f" % (-1*self.rex.joint_angles_fb[3]*R2D)))
        self.fk()
        self.check_if_reached()

        """ 
        Mouse position presentation in GUI
        TO DO: after getting affine calibration make the apprriate label
        to present the value of mouse position in world coordinates 
        """    
        x = QtGui.QWidget.mapFromGlobal(self,QtGui.QCursor.pos()).x()
        y = QtGui.QWidget.mapFromGlobal(self,QtGui.QCursor.pos()).y()
        if ((x < MIN_X) or (x > MAX_X) or (y < MIN_Y) or (y > MAX_Y)):
            self.ui.rdoutMousePixels.setText("(-,-)")
            self.ui.rdoutMouseWorld.setText("(-,-)")
        else:
            x = x - MIN_X
            y = y - MIN_Y
            self.ui.rdoutMousePixels.setText("(%.0f,%.0f)" % (x,y))
            if (self.video.aff_flag == 2):
                """ TO DO Here is where affine calibration must be used """
                self.ui.rdoutMouseWorld.setText("(-,-)")
            else:
                self.ui.rdoutMouseWorld.setText("(-,-)")

        """ 
        Updates status label when rexarm playback is been executed.
        This will be extended to includ eother appropriate messages
        """ 
        if(self.rex.plan_status == 1):
            self.ui.rdoutStatus.setText("Playing Back - Waypoint %d"
                                    %(self.rex.wpt_number + 1))


    def sliderChange(self):
        """ 
        Function to change the slider labels when sliders are moved
        and to command the arm to the given position 
        Implement for the other sliders
        """
        self.ui.rdoutBase.setText(str(self.ui.sldrBase.value()))
        self.ui.rdoutShoulder.setText(str(-1*self.ui.sldrShoulder.value()))
        self.ui.rdoutElbow.setText(str(-1*self.ui.sldrElbow.value()))
        self.ui.rdoutWrist.setText(str(-1*self.ui.sldrWrist.value()))
        self.ui.rdoutTorq.setText(str(self.ui.sldrMaxTorque.value()) + "%")
        self.ui.rdoutSpeed.setText(str(self.ui.sldrSpeed.value()) + "%")

        self.rex.max_torque = self.ui.sldrMaxTorque.value()/100.0
        self.rex.speed = self.ui.sldrSpeed.value()/100.0
        self.rex.joint_angles[0] = self.ui.sldrBase.value()*D2R
        self.rex.joint_angles[1] = self.ui.sldrShoulder.value()*D2R
        self.rex.joint_angles[2] = self.ui.sldrElbow.value()*D2R
        self.rex.joint_angles[3] = self.ui.sldrWrist.value()*D2R
        self.rex.cmd_publish()

    def mousePressEvent(self, QMouseEvent):
        """ 
        Function used to record mouse click positions for 
        affine calibration 
        """
 
        """ Get mouse posiiton """
        x = QMouseEvent.x()
        y = QMouseEvent.y()

        """ If mouse position is not over the camera image ignore """
        if ((x < MIN_X) or (x > MAX_X) or (y < MIN_Y) or (y > MAX_Y)): return

        """ Change coordinates to image axis """
        self.last_click[0] = x - MIN_X
        self.last_click[1] = y - MIN_Y
       
        """ If affine calibration is been performed """
        if (self.video.aff_flag == 1):
            """ Save last mouse coordinate """
            self.video.mouse_coord[self.video.mouse_click_id] = [(x-MIN_X),
                                                                 (y-MIN_Y)]

            """ Update the number of used poitns for calibration """
            self.video.mouse_click_id += 1

            """ Update status label text """
            self.ui.rdoutStatus.setText("Affine Calibration: Click Point %d" 
                                      %(self.video.mouse_click_id + 1))

            """ 
            If the number of click is equal to the expected number of points
            computes the affine calibration.
            
            LAB TASK: Change this code to use your affine calibration routine
            and NOT openCV pre-programmed function as it is done now.
            """
            if(self.video.mouse_click_id == self.video.aff_npoints):
                """ 
                Update status of calibration flag and number of mouse
                clicks
                """
                self.video.aff_flag = 2
                self.video.mouse_click_id = 0
                
                """ Perform affine calibration with OpenCV """
                self.video.aff_matrix = cv2.getAffineTransform(
                                        self.video.mouse_coord,
                                        self.video.real_coord)
            
                """ Updates Status Label to inform calibration is done """ 
                self.ui.rdoutStatus.setText("Waiting for input")

                """ 
                print affine calibration matrix numbers to terminal
                """ 
                print self.video.aff_matrix

    def affine_cal(self):
        """ 
        Function called when affine calibration button is called.
        Note it only chnage the flag to record the next mouse clicks
        and updates the status text label 
        """
        self.video.aff_flag = 1 
        self.ui.rdoutStatus.setText("Affine Calibration: Click Point %d" 
                                    %(self.video.mouse_click_id + 1))

    def check_if_reached(self):
        global is_reached_current_bottle, goal_ee
        error_x = abs(end_effector[0,0] - goal_ee[0])
        error_y = abs(end_effector[1,0] - goal_ee[1])
        error_z = abs(end_effector[2,0] - goal_ee[2])
        if LCM_DEBUG:
            print "\nerror_x:", error_x
            print "error_y:", error_y
            print "error_z:", error_z
            print "current_hole_index:", current_hole_index
            print "goal_ee:", goal_ee

        lock.acquire()
        is_reached_current_bottle = ((error_x < ERROR_IF_REACHED) and (error_y < ERROR_IF_REACHED) and (error_z < ERROR_IF_REACHED)) 
        lock.release()
        # if is_reached_current_bottle:
        #     print "REACHED:", goal_ee

        return is_reached_current_bottle 

    def fk(self):
        """ 
        Function called when affine calibration button is called.
        Note it only chnage the flag to record the next mouse clicks
        and updates the status text label 
        """
        self.video.aff_flag = 1 
        global end_effector

        dh_table = [[self.rex.joint_angles_fb[0], LINK1_LENGTH], [self.rex.joint_angles_fb[1], LINK2_LENGTH], [self.rex.joint_angles_fb[2], LINK3_LENGTH], [self.rex.joint_angles_fb[3], LINK4_LENGTH]]
        end_effector = self.rex.rexarm_fk(dh_table)
        end_effector[2] = end_effector[2] + OFFSET
        if FK_DEBUG:
            print "\nend_effector:\n", end_effector

        self.ui.rdoutX.setText(str(round(end_effector[0,0],3)))
        self.ui.rdoutY.setText(str(round(end_effector[1,0],3)))
        self.ui.rdoutZ.setText(str(round(end_effector[2,0],3)))
        self.ui.rdoutT.setText(str(round(end_effector[3,0],3)))    

        self.rex.cmd_publish()

    def ik(self):
        self.ui.rdoutStatus.setText("Computing Inverse Kinematics for EE = " + str(end_effector_for_ik) + "...")

        if IK_DEBUG:
            print "\nExpected angles (in degrees):"
            print "B:", round(correct_angles_for_ik[0]*R2D, 2)
            print "S:", round(correct_angles_for_ik[1]*R2D, 2)
            print "E:", round(correct_angles_for_ik[2]*R2D, 2)
            print "W:", round(correct_angles_for_ik[3]*R2D, 2)

        ee_pose = [end_effector_for_ik[0], end_effector_for_ik[1], end_effector_for_ik[2], -0.15] # [EE-x_g, EE-y_g, EE-z_g, EE-orientation], where EE is End Effector goal position
        result_angles = self.rex.rexarm_ik(ee_pose, cfg)

        if IK_DEBUG:
            print "\nExpected angles (in degrees):"
            print "B:", round(correct_angles_for_ik[0]*R2D, 2)
            print "S:", round(correct_angles_for_ik[1]*R2D, 2)
            print "E:", round(correct_angles_for_ik[2]*R2D, 2)
            print "W:", round(correct_angles_for_ik[3]*R2D, 2)
            print "\nInverse Kinematics angles (in degrees):"
            print "B:", round(result_angles[0]*R2D, 2)
            print "S:", round(result_angles[1]*R2D, 2)
            print "E:", round(result_angles[2]*R2D, 2)
            print "W:", round(result_angles[3]*R2D, 2)

        dh_table_correct = [[correct_angles_for_ik[0], LINK1_LENGTH], [correct_angles_for_ik[1], LINK2_LENGTH], [correct_angles_for_ik[2], LINK3_LENGTH], [correct_angles_for_ik[3], LINK4_LENGTH]]
        fk_correct = self.rex.rexarm_fk(dh_table_correct)
        fk_correct[2] = fk_correct[2] + OFFSET

        dh_table_ik = [[result_angles[0], LINK1_LENGTH], [-1*result_angles[1], LINK2_LENGTH], [-1*result_angles[2], LINK3_LENGTH], [-1*result_angles[3], LINK4_LENGTH]]
        fk_ik = self.rex.rexarm_fk(dh_table_ik)
        fk_ik[2] = fk_ik[2] + OFFSET

        if IK_DEBUG:
            print "\nExpected End Effector:"
            print "X:", round(fk_correct[0,0],3)
            print "Y:", round(fk_correct[1,0],3)
            print "Z:", round(fk_correct[2,0],3)
            print "\nActual End Effector:"
            print "X:", round(fk_ik[0,0],3)
            print "Y:", round(fk_ik[1,0],3)
            print "Z:", round(fk_ik[2,0],3)
        
        self.rex.joint_angles[0] = result_angles[0]
        self.rex.joint_angles[1] = -1*result_angles[1]
        self.rex.joint_angles[2] = -1*result_angles[2]
        self.rex.joint_angles[3] = -1*result_angles[3]

        self.rex.cmd_publish()

    def record_end_effector(self):
        global end_effector_for_ik, correct_angles_for_ik
        end_effector_for_ik = [end_effector[0,0], end_effector[1,0], end_effector[2,0], end_effector[3,0]]
        correct_angles_for_ik = [self.rex.joint_angles_fb[0], self.rex.joint_angles_fb[1], self.rex.joint_angles_fb[2], self.rex.joint_angles_fb[3]]

        if IK_DEBUG:
            print "End Effector:", str(end_effector_for_ik)
        self.ui.rdoutStatus.setText("End Effector Recorded: " + str(end_effector_for_ik))

    def isPressureSensorOccupied(self):
        print "Checking weight..."
        ser.write('w')
        time.sleep(0.1)
        result = ser.read()
        print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6 result:", result  
        if result == 'G':
            return 0
        elif result == 'B':
            return 1          

    def driveToBottle0(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[0])

    def driveToBottle1(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[1])

    def driveToBottle2(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[2])
        
    def driveToBottle3(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[3])
        
    def driveToBottle4(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[4])

    def driveToBottle5(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[5])
        
    def driveToBottle6(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[6])
        
    def driveToBottle7(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[7])

    def driveToBottle8(self):   
        self.driveToBottle(FINAL_END_EFFECTORS[8])   

    def driveToHome(self):
        thread.start_new_thread( handle_driving_home, () )
    
    def driveToBottle(self, end_effector):
        global goal_ee
        goal_ee = end_effector
        result_angles = self.rex.rexarm_ik(end_effector, cfg)

        self.rex.joint_angles[0] = result_angles[0]
        self.rex.joint_angles[1] = -1*result_angles[1]
        self.rex.joint_angles[2] = -1*result_angles[2]
        self.rex.joint_angles[3] = -1*result_angles[3]

        self.rex.cmd_publish()

    def findMixPoints(self):
        for i in range(NUMBER_OF_POINTS):
            MIX_END_EFFECTORS[i] = [MIX_CENTER[0] + math.cos(MIX_PHI[i])*MIX_RADIUS, MIX_CENTER[1] + math.sin(MIX_PHI[i])*MIX_RADIUS, MIX_CENTER[2], MIX_CENTER[3]]
        if MIX_DEBUG:
            print "MIX_CENTER", MIX_CENTER

    def mixDrink(self):
        
        self.ui.rdoutStatus.setText("Mixing drink...")

        self.findMixPoints()

        thread.start_new_thread( handle_mixing, () )

def handle_driving_home():
        global current_hole_index, is_reached_current_bottle, goal_ee
           
        current_home_indices = [9,10]

        while True:
            for j in range(2):
                if (j==1):
                        lock.acquire()
                        ex.ui.sldrSpeed.setValue(3)
                        lock.release()
                    #print "Driving to", k, ":", MIX_END_EFFECTORS[k]
                ex.driveToBottle(FINAL_END_EFFECTORS[current_home_indices[j]])
                while (is_reached_current_bottle == 0):
                    pass
                #print "Sleeping..."    
                time.sleep(0.4)  
                is_reached_current_bottle = 0
            break        
        lock.acquire()
        ex.ui.sldrSpeed.setValue(12)
        lock.release()
def handle_mixing():
        global current_hole_index, is_reached_current_bottle, goal_ee
           
        while True:
        
            for j in range(2):
                print "NUMBER_OF_POINTS ", NUMBER_OF_POINTS
                for k in range(NUMBER_OF_POINTS):
                    #if (k==1):
                        #ex.ui.sldrSpeed.setValue(30)
                    #print "Driving to", k, ":", MIX_END_EFFECTORS[k]
                    ex.driveToBottle(MIX_END_EFFECTORS[k])
                    while (is_reached_current_bottle == 0):
                        pass
                    #print "Sleeping..."    
                    time.sleep(0.0001)  
                    is_reached_current_bottle = 0
            
            break

        #ex.ui.sldrSpeed.setValue(12)
        ex.driveToHome()        

def main():
    global ex
    print "STARTED\n"
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()