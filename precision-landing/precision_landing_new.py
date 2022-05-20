import cv2
import cv2.aruco as aruco
import djitellopy
import av
import sys
import traceback
import time
import threading
import numpy as np
import math
from simple_pid import PID

#--- Define pid conntroller
pid_X = PID(2, 0.1, 0.3, setpoint=0)
pid_Y = PID(2, 0.1, 0.3, setpoint=0)
pid_Z = PID(1.3, 0.1, 0.3, setpoint=30)

pid_X.output_limits = (0, 30)
pid_Y.output_limits = (0, 30)
pid_Z.output_limits = (0, 30)

pid_X.sample_time = 0.05  # update every 0.05 seconds (20Hz)
pid_Y.sample_time = 0.05  # update every 0.05 seconds (20Hz)
pid_Z.sample_time = 0.05  # update every 0.05 seconds (20Hz)

pid_X.proportional_on_measurement = True
pid_Y.proportional_on_measurement = True
pid_Z.proportional_on_measurement = True

pid_X.setpoint = 0
pid_Y.setpoint = 0
pid_Z.setpoint = 30

#--- Define Tag
id_to_find  = 42
marker_size  = 10 #- [cm]

#-- Font for the text in the image
font = cv2.FONT_HERSHEY_PLAIN

#------------------------------------------------------------------------------
#------- ROTATIONS https://www.learnopencv.com/rotation-matrix-to-euler-angles/
#------------------------------------------------------------------------------
# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


#--- Get the camera calibration path
calib_path  = "./"
camera_matrix   = np.loadtxt(calib_path+'cameraMatrix.txt', delimiter=',')
camera_distortion   = np.loadtxt(calib_path+'cameraDistortion.txt', delimiter=',')

#--- 180 deg rotation matrix around the x axis
R_flip  = np.zeros((3,3), dtype=np.float32)
R_flip[0,0] = 1.0
R_flip[1,1] =-1.0
R_flip[2,2] =-1.0

#--- Define the aruco dictionary
aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
parameters  = aruco.DetectorParameters_create()


def main():
    process_this_frame = True
    drone = djitellopy.Tello()
    current_milli_time = lambda: int(round(time.time() * 1000))
    global CMD
    pid_X_output = 0
    pid_Y_output = 0
    pid_Z_output = 0
    tgt_lock = False
    tgt_lost = False
    CMD=1
    target_distance = 30
    try:
        drone.connect()
        drone.streamon()

        container = drone.get_frame_read()
        drone.takeoff()
        drone.set_speed(10)

        # skip first 100 frames
        frame_skip = 200
        while True:
            print(f"Battery : {drone.get_battery()}")
            image = container.frame
            if 0 < frame_skip:
                frame_skip = frame_skip - 1
                continue
            start_time = time.time()
            
            #image = np.array(frame)

            #-- Convert in gray scale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #-- remember, OpenCV stores color images in Blue, Green, Red

            #-- initialize vector of int
            ids = [0]

            #-- Find all the aruco markers in the image
            corners, ids, rejected = aruco.detectMarkers(image=gray, dictionary=aruco_dict, parameters=parameters,
                            cameraMatrix=camera_matrix, distCoeff=camera_distortion)

            if ids is not None and id_to_find in ids:
                #-- ret = [rvec, tvec, ?]
                #-- array of rotation and position of each marker in camera frame
                #-- rvec = [[rvec_1], [rvec_2], ...]    attitude of the marker respect to camera frame
                #-- tvec = [[tvec_1], [tvec_2], ...]    position of the marker in camera frame
                ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

                #-- Unpack the output, get only the first
                rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]

                #-- Obtain the rotation matrix tag vs camera
                R_ct = np.matrix(cv2.Rodrigues(rvec)[0])
                R_tc = R_ct

                #-- Get the attitude in terms of euler 321 (Needs to be flipped first)
                roll_marker, pitch_marker, yaw_marker = rotationMatrixToEulerAngles(R_flip*R_tc)

                #-- Draw the detected marker and put a reference frame over it
                aruco.drawDetectedMarkers(image, corners)
                aruco.drawAxis(image, camera_matrix, camera_distortion, rvec, tvec, 10)

                #-- Print the tag position in camera frame
                str_position = "MARKER Position x=%4.0f  y=%4.0f  z=%4.0f "%(tvec[0], tvec[1], tvec[2])
                cv2.putText(image, str_position, (0, 100), font, 1, (10, 10, 200), 2, cv2.LINE_AA)

                #-- Print the marker's attitude respect to camera frame
                str_attitude = "MARKER Attitude r=%4.0f  p=%4.0f  y=%4.0f"%(math.degrees(roll_marker),math.degrees(pitch_marker),
                math.degrees(yaw_marker))
                cv2.putText(image, str_attitude, (0, 200), font, 1, (255, 10, 10), 2, cv2.LINE_AA)


            cv2.imshow('Navigation Window', image)
            cv2.waitKey(1)

            """
            if frame.time_base < 1.0/60:
                time_base = 1.0/60
            else:
                time_base = frame.time_base
            frame_skip = int((time.time() - start_time)/time_base)
            """
            
            #searching for target
            if CMD == 1:
                drone.rotate_clockwise(360)
                #drone.move_forward(30)

            # Initial approach
            if ids is not None and id_to_find in ids:
                tgt_lock = True
                tgt_lost = False
                tgt_lock_time = time.time()
                drone.rotate_clockwise(0)

                #-- Translation X
                if tvec[0] < 0:
                    if tvec[0] < -15:
                        drone.move_left(15)
                        print("move_left 6")
                    if tvec[0] > -9:
                        drone.move_left(10)
                        print("move_left 3")
                    if tvec[0] > -3:
                        drone.move_left(0)
                if tvec[0] > 0:
                    if tvec[0] > 15:
                        drone.move_right(15)
                    if tvec[0] < 10:
                        drone.move_right(10)
                    if tvec[0] < 3:
                        drone.move_right(0)

                #-- Translation Y
                if tvec[1] < 0:
                    if tvec[1] < -15:
                        drone.move_up(20)
                    if tvec[1] > -9:
                        drone.move_up(10)
                        print("move_left 3")
                    if tvec[1] > -3:
                        drone.move_up(0)
                if tvec[1] > 0:
                    if tvec[1] > 15:
                        drone.move_down(20)
                    if tvec[1] < 10:
                        drone.move_down(10)
                    if tvec[1] < 3:
                        drone.move_down(0)

                #-- Translation Z
                if tvec[2] < target_distance :
                    drone.move_back(11)
                if tvec[2] > target_distance:
                    if tvec[2] > target_distance + 100:
                        drone.move_forward(25)
                    if tvec[2] > target_distance + 30:
                        drone.move_forward(15)
                    if tvec[2] < target_distance + 30:
                        drone.move_forward(11)
                    if tvec[2] < target_distance + 10:
                        drone.move_forward(7)
                    if tvec[2] < target_distance + 2:
                        drone.move_forward(0)

                #-- Rotation allign
                Rotation=math.degrees(pitch_marker)
                if Rotation < -3 :
                    drone.rotate_clockwise(15)
                if Rotation > 3 :
                    drone.rotate_counter_clockwise(15)
                if Rotation >= -3 and Rotation <= 3 :
                    drone.rotate_counter_clockwise(0)
                    drone.rotate_clockwise(0)

                #--Landing
                if tvec[2] < target_distance + 3 and tvec[2] > target_distance -3:
                    if tvec[1] < 2 and tvec[1] > -2:
                        if tvec[0] < 2 and tvec[0] > -2:
                            drone.land()
                CMD=0

            #-- target lost
            if tgt_lock == True:
                if tgt_lock_time + 1 < time.time():
                    drone.move_back(0)
                    drone.move_forward(0)
                    drone.move_up(0)
                    drone.move_down(0)
                    drone.move_left(0)
                    drone.move_right(0)
                    drone.move_back(25)
                    if tgt_lock_time + 6 < time.time():
                        drone.move_back(0)
                        tgt_lock = False
                        tgt_lost=True

            #-- star search after target lost
            if tgt_lost == True:
                if tgt_lock_time +5 < time.time():
                    CMD=1

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.land()
        time.sleep(5)
        drone.end()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
