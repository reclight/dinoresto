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

        theta1 = (self.calc_theta1()+self.calib_theta1)/0.29
        theta2 = (300-self.calc_theta2()-self.calib_theta2)/0.29
        theta3 = (self.calc_theta3()+self.calib_theta3)/0.29
        base = self.base_theta/0.29
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
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, 10, ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%sffff" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%sff" % self.packetHandler.getRxPacketError(dxl_error))

            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (20, theta1, dxl_present_position))
            
            if abs(theta1 - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
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
    
    i.set_xy (15, 14)
    i.set_base(240)
    i.movegroup()

    i.set_xy (15, 7)
    i.set_base(240)
    i.movegroup()

    i.toogle_gripper(False)

    i.set_xy (15, 17)
    i.set_base(240)
    i.movegroup()

    print(table)
    print(type(table))

    if table=="1":
        i.set_base(110)
        i.set_xy (15, 15.2)
        i.movegroup()
    elif table=="2":
        i.set_base(130)
        i.set_xy (18, 15.2)
        i.movegroup()
    elif table=="3":
        i.set_base(155)
        i.set_xy (18, 15.2)
        i.movegroup()
    elif table=="4":
        i.set_base(170)
        i.set_xy (15, 15.2)
        i.movegroup()

    i.toogle_gripper(True)


    i.toogle_gripper(False)

    i.set_xy (15, 15.2)
    i.set_base(240)
    i.movegroup()

    i.set_xy (15, 7)
    i.set_base(240)
    i.movegroup()

    i.toogle_gripper(True)
    
    i.portHandler.closePort()
    return 0


if __name__ == "__main__":
    app.run(host='192.168.0.101', threaded=True, debug=True)
