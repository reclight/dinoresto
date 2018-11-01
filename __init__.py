import requests
import time
import serial
from flask import Flask, request, flash, render_template
import subprocess , time, os
import requests
from flask_cors import CORS, cross_origin
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import math
import os
import time
import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import math

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *


# Control table address
ADDR_MX_TORQUE_ENABLE      = 24               # Control table address is different in Dynamixel model
ADDR_MX_GOAL_POSITION      = 30
ADDR_MX_PRESENT_POSITION   = 36

# Protocol version
PROTOCOL_VERSION            = 1.0               # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM6'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 0           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

#****************************************


#****************************************
PI = 3.14159265359
class robotic_arm:
    def __init__(self, l1, l2):
        self.x=0
        self.y=0
        self.l1 = l1
        self.l2 = l2
        self.calib_theta1 = 0
        self.calib_theta2 = 0
        self.calib_theta3 = 0
        self.base_theta = 0
        
        self.portHandler = PortHandler(DEVICENAME)
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
    
    def connect_setup(self):

        # Open port
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")
            getch()
            quit()

        # Set Port Baud Rate
        if self.portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()

        #Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 10, 32, 80)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 20, 32, 80)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 30, 32, 80)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 40, 32, 80)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 50, 32, 80)
        if dxl_comm_result != COMM_SUCCESS:
                print("%sthere is too many error handler" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%sthere is too many error handler again" % self.packetHandler.getRxPacketError(dxl_error))


        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, 10, ADDR_MX_TORQUE_ENABLE, 1)
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, 20, ADDR_MX_TORQUE_ENABLE, 1)
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, 30, ADDR_MX_TORQUE_ENABLE, 1)
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, 40, ADDR_MX_TORQUE_ENABLE, 1)
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, 50, ADDR_MX_TORQUE_ENABLE, 1)


        if dxl_comm_result != COMM_SUCCESS:
            print("%scc" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%sdd" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully connected")

    def set_base(self,theta):
        self.base_theta=theta
    
    def set_xy(self, xx, yy):
        self.x = xx
        self.y = yy
    
    def calibrate (self, calib_1, calib_2, calib_3):
        self.calib_theta1=calib_1
        self.calib_theta2=calib_2
        self.calib_theta3=calib_3
    
    def calc_theta2(self):
        num = self.x*self.x + self.y*self.y - self.l1*self.l1 - self.l2 * self.l2
        det = 2*self.l1*self.l2
        result=-math.acos(num/det)*180.0/PI
        
        return result
    
    def calc_theta1(self):
        theta = self.calc_theta2()*PI/180
        a = self.y/self.x
        b_num = self.l2 * math.sin(theta)
        b_det = self.l1 + self.l2 * math.cos(theta)
        return (math.atan(a) - math.atan(b_num/b_det))*180/PI
    
    def calc_theta3(self):
        theta2 = self.calc_theta2()
        theta1 = self.calc_theta1()
        theta3 = 90+theta2+theta1
    
        return theta3
    

    def movegroup(self):

        theta1 = (self.calc_theta1()+self.calib_theta1)/0.293
        theta2 = (300-self.calc_theta2()-self.calib_theta2)/0.293
        theta3 = (self.calc_theta3()+self.calib_theta3)/0.293
        base = self.base_theta/0.293
        # Write goal position
        print(theta1)
        print(theta2)

        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 10, ADDR_MX_GOAL_POSITION, int(theta1))
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 20, ADDR_MX_GOAL_POSITION, int(theta2))
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 30, ADDR_MX_GOAL_POSITION, int(theta3))
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 50, ADDR_MX_GOAL_POSITION, int(base))
        print(dxl_comm_result)
        if dxl_comm_result != COMM_SUCCESS:
            print("%saa" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%sbb" % self.packetHandler.getRxPacketError(dxl_error))

        """while 1:
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, 50, ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%sffff" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%sff" % self.packetHandler.getRxPacketError(dxl_error))

            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (20, base, dxl_present_position))
            
            if abs(base - dxl_present_position) < DXL_MOVING_STATUS_THRESHOLD:
                break"""
          
        time.sleep(3)
        return 0
    

    def toogle_gripper(self, open_gripper):
        if(open_gripper):
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 40, ADDR_MX_GOAL_POSITION, 410)
            if dxl_comm_result != COMM_SUCCESS:
                print("gripper : %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("gripper : %s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, 40, ADDR_MX_GOAL_POSITION, 480)
            if dxl_comm_result != COMM_SUCCESS:
                print("gripper : %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("gripper : %s" % self.packetHandler.getRxPacketError(dxl_error))
        
        time.sleep(1)
        return 0


#****************************************



#****************************************
class aruco_tracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = self.calibrate_camera()

    def calibrate_camera(self):
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((9*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        images = glob.glob('D:/dinoresto/calib_images/*.jpg')

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (9,7),None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)

                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (9, 7), corners2,ret)


        return cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

    def findcoordinate(self, corners, ids, number, size):
        index = np.where(ids==number)
        a = np.array(index)
        if a.size!=0:
            a=a.item(0)

            rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners[a], size, self.mtx, self.dist) #Estimate pose of each marker and return the values rvet and tvec---different from camera coefficients
            (rvec-tvec).any() # get rid of that nasty numpy value array error

            aruco.drawAxis(self.frame, self.mtx, self.dist, rvec[0], tvec[0], 1) #Draw Axis
            aruco.drawDetectedMarkers(self.frame, corners) #Draw A square around the markers
            return rvec[0], tvec[0]
        else:
            return None, None

    def detectMarker(self,id):
        while (True):
            ret, self.frame = self.cap.read()
            # operations on the frame come here
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
            parameters = aruco.DetectorParameters_create()

            #lists of ids and the corners beloning to each id
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

            font = cv2.FONT_HERSHEY_SIMPLEX #font for displaying text (below)

            if np.all(ids != None):

                rtarg = np.empty((3,1))
                ttarg = np.empty((3,1))

                rcord, tcord = self.findcoordinate(corners, ids, 1, 1.5)
                rtarg, ttarg = self.findcoordinate(corners, ids, id, 3)

                if np.all(ttarg !=None) and np.all(tcord !=None):
                    ttc = ttarg - tcord
                    ttc = np.transpose(ttc)
                    mcord, _ = cv2.Rodrigues(rcord)
                    mcord = np.transpose(mcord)
                    coord = np.matmul(mcord,ttc)
                    coord = np.transpose(coord)
                    print(coord)
                    calibrate_coord = np.array([-3,2.5,0])
                    coord = coord + calibrate_coord
                    print("After calibration : ",coord)
                    
                    # When everything done, release the capture
                    self.cap.release()
                    cv2.destroyAllWindows()

                    return coord


            # Display the resulting frame
            cv2.imshow('frame',self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    def convert_R_Theta(self,coord):
        angle = 130
        PI = 3.14159265359
        print(coord)
        r = math.sqrt(coord[0]*coord[0] + coord[1]*coord[1])-1.5
        theta = 180/PI*(math.atan2(coord[1],coord[0])) - angle
        if theta < 0:
            print(theta)
            theta = 360 + theta
        return r, theta
#****************************************


#****************************************

app = Flask(__name__)
CORS(app)
app = Flask(__name__)
CORS(app)


class MenuForm(Form):
    table = StringField('table', validators=[validators.DataRequired()])
    food = StringField('food', validators=[validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def static_page0():
    return render_template('index.html', form="form")      #Host the web-browser based user interface (Warehouse and Assembly Line)

@app.route('/script', methods=['POST'])
def script():
    table = request.form['table']
    food = request.form['food']
    try:
        control_robot(table, food)
        return "success"
    except Exception as e:
        print(e.args[0])
        if "FileNotFoundError" in e.args[0]:
            return "notfoundError"
        elif "PermissionError" in e.args[0]:
            return "usedError"
        else:
            return "otherError"

def control_robot(table, food):

    i= robotic_arm(13.4, 10.3)
    i.connect_setup()
    i.calibrate(75,243,60)

    i.toogle_gripper(True)

    i.set_xy (10, 17)
    i.set_base(150)
    i.movegroup()

    mDetector = aruco_tracker()
    if food =="red":
        coordinate = mDetector.detectMarker(28)
    elif food =="green":
        coordinate = mDetector.detectMarker(179)
    elif food =="blue":
        coordinate = mDetector.detectMarker(527)
    elif food =="orange":
        coordinate = mDetector.detectMarker(314)

    r, theta = mDetector.convert_R_Theta(coordinate[0])
    
    i.set_xy (r, 14)
    i.set_base(theta)
    i.movegroup()

    i.set_xy (r, 6.5)
    i.set_base(theta)
    i.movegroup()

    i.toogle_gripper(False)


    """i.set_xy (15, 14)
    i.set_base(240)
    i.movegroup()

    i.set_xy (15, 7)
    i.set_base(240)
    i.movegroup()
    
    i.toogle_gripper(False)
    """
    i.set_xy (10, 16)
    i.set_base(theta)
    i.movegroup()

    print(table)
    print(type(table))

    if table=="1":
        i.set_base(110)
        i.set_xy (10, 17)
        i.movegroup()

        i.set_base(110)
        i.set_xy (15, 15.5)
        i.movegroup()
    elif table=="2":
        i.set_base(130)
        i.set_xy (10, 17)
        i.movegroup()

        i.set_base(130)
        i.set_xy (17.3, 15.5)
        i.movegroup()
    elif table=="3":
        i.set_base(155)
        i.set_xy (10, 17)
        i.movegroup()

        i.set_base(155)
        i.set_xy (17.3, 15.5)
        i.movegroup()
    elif table=="4":
        i.set_base(170)
        i.set_xy (10, 17)
        i.movegroup()

        i.set_base(170)
        i.set_xy (15, 15.5)
        i.movegroup()

    i.toogle_gripper(True)

    if table=="1":
        i.set_base(110)
        i.set_xy (15, 16)
        i.movegroup()
    elif table=="2":
        i.set_base(130)
        i.set_xy (17.3, 15.8)
        i.movegroup()
    elif table=="3":
        i.set_base(155)
        i.set_xy (17.3, 15.8)
        i.movegroup()
    elif table=="4":
        i.set_base(170)
        i.set_xy (15, 16)
        i.movegroup()


    i.set_xy (10, 17)
    i.set_base(150)
    i.movegroup()
    
    i.portHandler.closePort()
    return 0


if __name__ == "__main__":
    app.run(host='192.168.0.100', threaded=True, debug=True)
