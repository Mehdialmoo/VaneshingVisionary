import cv2
import os
from utilities import Posefunc
import numpy as np
import threading
import socket
import UdpComms as U
import time
import queue
import json

path = "./RTP/video/yoga_data/"
JOINT_DIC = {
    'RIGHT_ELBOW': 14,
    'LEFT_SHOULDER': 11,
    'RIGHT_SHOULDER': 12,
    'LEFT_ELBOW': 13,
    'RIGHT_WRIST': 16,
    'LEFT_WRIST': 15,
    'RIGHT_HIP': 24,
    'LEFT_HIP': 23,
    'RIGHT_KNEE': 26,
    'LEFT_KNEE': 25,
    'RIGHT_ANKLE': 28,
    'LEFT_ANKLE': 27
}
ANGLE_LIST = {
    'RIGHT_ELBOW',
    'LEFT_ELBOW',
    'RIGHT_SHOULDER',
    'LEFT_SHOULDER',
    'RIGHT_HIP',
    'LEFT_HIP',
    'RIGHT_KNEE',
    'LEFT_KNEE'
}

CAL_LIST = [
    ['RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_WRIST'],
    ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'],
    ['LEFT_ELBOW', 'RIGHT_SHOULDER', 'RIGHT_HIP'],
    ['LEFT_ELBOW', 'LEFT_SHOULDER', 'LEFT_HIP'],
    ['RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE'],
    ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE'],
    ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'],
    ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE'],
]


def cal_acc(angle_list:list, target_list:list) -> list:
    res = []
    try :
        for i in range(8):
            dis = pow(((target_list[i] - angle_list[i])/180.0), 2)
            res.append(dis)
    except Exception as e:
        print(e)    
    
    return res
        



def test(P,joints_acc : queue.Queue):
    i = 1
    IMAGE_FILES = os.listdir(path)
    resized, angle_target, point_target = P.load(path, IMAGE_FILES, i)

    with P.MP_POSE.Pose(min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            notalike = True

            if (notalike):
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image_height, image_width, _ = image.shape
                image = cv2.resize(image, (860, 960))

                # image = cv2.resize(
                #    image, (int(image_width * (860 / image_height)), 860))
                # finding the distance by calling function
                # Distance distance finder function need
                # these arguments the Focal_Length,
                # Known_width(centimeters),
                # and Known_distance(centimeters)
                try:
                    landmarks = results.pose_landmarks.landmark
                    # print(results.pose_landmarks)

                    angle_point = []  # 所有计算角度需要用到的点的坐标
                    landmark_dic = {}  # 所有会返回准确率的joint的的坐标
                    for k in JOINT_DIC:
                        v = JOINT_DIC[k]
                        pos = [landmarks[v].x, landmarks[v].y]
                        landmark_dic[k] = pos
                        if k in ANGLE_LIST:
                            angle_point.append(pos)

                    keypoints = []  # 从landmarks提取出的3d坐标
                    for point in landmarks:
                        keypoints.append({
                            'X': point.x,
                            'Y': point.y,
                            'Z': point.z,
                        })

                    p_score = P.dif_compare(keypoints, point_target)

                    angle = []

                    for i in range(8):
                        ang = P.calculateAngle(
                            landmark_dic[CAL_LIST[i][0]],
                            landmark_dic[CAL_LIST[i][1]],
                            landmark_dic[CAL_LIST[i][2]])
                        angle.append(ang)
                    ang_acc = cal_acc(angle,angle_target)
                    print("========")
                    print(ang_acc)
                    joints_acc.put(ang_acc)

                    P.compare_pose(image, angle_point, angle, angle_target)
                    a_score = P.diff_compare_angle(angle, angle_target)

                    if (p_score >= a_score):
                        cv2.putText(
                            image, str(int((1 - a_score)*100)), (80, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            [0, 0, 255], 2, cv2.LINE_AA)

                    else:
                        cv2.putText(
                            image, str(int((1 - p_score)*100)), (80, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            [0, 0, 255], 2, cv2.LINE_AA)

                except Exception as e:
                    print("Error in drawing bones", e)

                P.MP_DRAWING.draw_landmarks(image, results.pose_landmarks,
                                            P.MP_POSE.POSE_CONNECTIONS,
                                            P.MP_DRAWING.DrawingSpec(
                                                color=(0, 0, 255),
                                                thickness=4, circle_radius=4),
                                            P.MP_DRAWING.DrawingSpec(
                                                color=(0, 255, 0),
                                                thickness=3, circle_radius=3)
                                            )

                # txt test 150-*
                hori = np.concatenate((image, resized), axis=1)
                # cv2.imshow('MediaPipe Feed', hori)
                cv2.imshow('MediaPipe Feed', hori)
                # cv2.imshow("Camera", resized_frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()


def serverdata(message, joints_acc: queue.Queue):
    print(message)
    i = 0
    # Create UDP socket to use for sending (and receiving)
    sock = U.UdpComms(
        udpIP="127.0.0.1", portTX=8000,
        portRX=8001, enableRX=True,
        suppressWarnings=True)
    running = True
    nodata = 0
    while running:
        # sock.SendData('Sent from Python: ' + str(i))
        # Send this string to other application
        i += 1

        data = sock.ReadReceivedData()  # read data

        if data != None:
            # if NEW data has been received since last ReadReceivedData function call
            print(data)  # print new received data
            nodata = 0

        if joints_acc.qsize() == 0:
            nodata = nodata + 1
            if(nodata >= 50000000):
                print("Long time no data, quit")
                running = False
                break
        else:
            nodata = 0
            joints_acc_data = joints_acc.get()
            joints_acc_data = json.dumps({"score": joints_acc_data})
            sock.SendData(joints_acc_data)

        #time.sleep(1)
        
    
    sock.CloseSocket()


if __name__ == "__main__":
    P = Posefunc()
    cap = cv2.VideoCapture(0)
    i = 0

    joints_acc = queue.Queue()

    t1 = threading.Thread(target=test, args=(P, joints_acc,))
    t2 = threading.Thread(target=serverdata, args=(
        'enter Thread2', joints_acc,))

    t1.start()
    t2.start()
