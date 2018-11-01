import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import math

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
        angle = 120
        PI = 3.14159265359
        print(coord)
        r = math.sqrt(coord[0]*coord[0] + coord[1]*coord[1])
        theta = 180/PI*(math.atan2(coord[1],coord[0])) - angle
        if theta < 0:
            print(theta)
            theta = 360 + theta
        return r, theta

mDetector = aruco_tracker()
coordinate = mDetector.detectMarker(46)
r, theta = mDetector.convert_R_Theta(coordinate[0])
print(r, theta)