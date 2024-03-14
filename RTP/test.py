import cv2
import numpy as np
import time

from utilities import Posefunc

# path = r"./RTP/video/yoga_data"
# path = r"D:\git ex\VaneshingVisionary\RTP\Data\yoga_data"
# path = r"D:\git ex\VaneshingVisionary\RTP\Data\side"
path = r"D:\git ex\VaneshingVisionary\RTP\Data\front"

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
ANGLE_LIST = [
    'RIGHT_ELBOW',
    'LEFT_ELBOW',
    'RIGHT_SHOULDER',
    'LEFT_SHOULDER',
    'RIGHT_HIP',
    'LEFT_HIP',
    'RIGHT_KNEE',
    'LEFT_KNEE'
]

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


def test():
    for i in range(16):
        cap = cv2.VideoCapture(0)
        P = Posefunc()
        t_b = 0
        t1 = None
        acc = []
        image = []

        resized, angle_target, point_target = P.load(path, i)

        with P.MP_POSE.Pose(min_detection_confidence=0.5,
                            min_tracking_confidence=0.5) as pose:

            while cap.isOpened():
                ok, frame = cap.read()
                if not ok:
                    continue
                frame = cv2.flip(frame, 1)
                notalike = True

                if (notalike):
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = pose.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    # image_height, image_width, _ = image.shape
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

                    except Exception as e:
                        print("landmarks err:", e)
                        continue

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

                    ang_acc = P.cal_acc(
                        angle_list=angle, target_list=angle_target)

                    P.compare_pose(
                        image, angle_point, angle,
                        angle_target, show_text=True)
                    a_score = P.diff_compare_angle(angle, angle_target)

                    # if (p_score >= a_score):
                    if (1-a_score >= 0.60):
                        cv2.putText(
                            image, str(
                                int((1 - a_score)*100)), (80, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            [0, 0, 255], 2, cv2.LINE_AA)

                        if (t_b == 0):
                            print("start")
                            t1 = time.time()
                            acc.append(a_score)
                            t_b = 1
                        if ((time.time() - t1) > 5) and (t_b == 1):
                            print("finish")
                            print(1-P.Average(acc))
                            print(ang_acc)
                            acc.clear()
                            t_b = 0
                            t1 = None
                            break
                        if (t_b == 1):
                            print("add")
                            acc.append(a_score)

                    else:
                        acc.clear()
                        t_b = 0
                        t1 = None
                        cv2.putText(
                            image, str(int((1 - p_score)*100)), (80, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1,
                            [0, 0, 255], 2, cv2.LINE_AA)

                    P.MP_DRAWING.draw_landmarks(image, results.pose_landmarks,
                                                P.MP_POSE.POSE_CONNECTIONS,
                                                P.MP_DRAWING.DrawingSpec(
                                                    color=(0, 0, 255),
                                                    thickness=4,
                                                    circle_radius=4),
                                                P.MP_DRAWING.DrawingSpec(
                                                    color=(0, 255, 0),
                                                    thickness=3,
                                                    circle_radius=3)
                                                )

                    # txt test 150-*
                    hori = np.concatenate((image, resized), axis=1)
                    # cv2.imshow('MediaPipe Feed', image)
                    cv2.imshow('Yoga pose estimator', hori)
                    # cv2.imshow("pose", resized)
                if cv2.waitKey(1) & 0xFF == ord('n'):
                    break
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    exit(0)
        cv2.destroyAllWindows()
        # cv2. destroyWindow("pose")
        cap.release()


if __name__ == "__main__":
    test()
