import sys
import cv2
import numpy as np
from time import sleep
from PyQt4 import QtGui, QtCore, Qt
from ui import Ui_MainWindow
from rexarm import Rexarm
from decimal import *

from video import Video

""" Radians to/from  Degrees conversions """
D2R = 3.141592/180.0
R2D = 180.0/3.141592
PI = np.pi

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
LINK4_LENGTH = 10.5 / 100 # TODO: change this to our gripper

FK_DEBUG = 0 # Change to '1' to print out stuff for Forward Kinematics
IK_DEBUG = 1 # Change to '1' to print out stuff for Inverse Kinematics
 
class Gui(QtGui.QMainWindow):
    """ 
    Main GUI Class
    It contains the main function and interfaces between 
    the GUI and functions
    """
    def __init__(self,parent=None):
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
        self.ui.sldrBase.valueChanged.connect(self.sliderChange)
        self.ui.sldrShoulder.valueChanged.connect(self.sliderChange)
        self.ui.sldrElbow.valueChanged.connect(self.sliderChange)
        self.ui.sldrWrist.valueChanged.connect(self.sliderChange)
        self.ui.sldrMaxTorque.valueChanged.connect(self.sliderChange)

        """ Commands the arm as the arm initialize to 0,0,0,0 angles """
        self.sliderChange() 
        
        """ Connect Buttons to Functions 
        LAB TASK: NAME AND CONNECT BUTTONS AS NEEDED
        """
        self.ui.btnUser1.setText("Affine Calibration")
        self.ui.btnUser1.clicked.connect(self.affine_cal)

        self.ui.btnUser2.setText("Forward Kinematics")
        self.ui.btnUser2.clicked.connect(self.fk)

        self.ui.btnUser3.setText("Inverse Kinemetics")
        self.ui.btnUser3.clicked.connect(self.ik)

        self.ui.btnUser4.setText("Record End Effector")
        self.ui.btnUser4.clicked.connect(self.record_end_effector)

    
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
        self.ui.rdoutShoulderJC.setText(str("%.2f" % (self.rex.joint_angles_fb[1]*R2D)))
        self.ui.rdoutElbowJC.setText(str("%.2f" % (self.rex.joint_angles_fb[2]*R2D)))
        self.ui.rdoutWristJC.setText(str("%.2f" % (self.rex.joint_angles_fb[3]*R2D)))
        self.fk()

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
        self.ui.rdoutShoulder.setText(str(self.ui.sldrShoulder.value()))
        self.ui.rdoutElbow.setText(str(self.ui.sldrElbow.value()))
        self.ui.rdoutWrist.setText(str(self.ui.sldrWrist.value()))

        self.ui.rdoutTorq.setText(str(self.ui.sldrMaxTorque.value()) + "%")
        self.rex.max_torque = self.ui.sldrMaxTorque.value()/100.0
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

        cfg = [LINK1_LENGTH + OFFSET, LINK2_LENGTH, LINK3_LENGTH, LINK4_LENGTH] # Lengths of the links
        ee_pose = [end_effector_for_ik[0], end_effector_for_ik[1], end_effector_for_ik[2], 0] # [EE-x_g, EE-y_g, EE-z_g, EE-orientation], where EE is End Effector goal position
        result_angles = self.rex.rexarm_ik_kuipers(ee_pose, cfg)

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

        dh_table_ik = [[result_angles[0], LINK1_LENGTH], [result_angles[1], LINK2_LENGTH], [result_angles[2], LINK3_LENGTH], [result_angles[3], LINK4_LENGTH]]
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
        
        # self.rex.joint_angles[0] = result_angles[0]
        # self.rex.joint_angles[1] = result_angles[1]
        # self.rex.joint_angles[2] = result_angles[2]
        # self.rex.joint_angles[3] = result_angles[3]

        # self.rex.cmd_publish()

    def record_end_effector(self):
        global end_effector_for_ik, correct_angles_for_ik
        end_effector_for_ik = [end_effector[0,0], end_effector[1,0], end_effector[2,0], end_effector[3,0]]
        correct_angles_for_ik = [self.rex.joint_angles_fb[0], self.rex.joint_angles_fb[1], self.rex.joint_angles_fb[2], self.rex.joint_angles_fb[3]]

        self.ui.rdoutStatus.setText("End Effector Recorded: " + str(end_effector_for_ik))
 
def main():
    print "STARTED\n"
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
