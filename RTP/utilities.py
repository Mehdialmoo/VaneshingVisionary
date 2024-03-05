import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

# import time
# import datetime
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import math
# from mpl_toolkits import mplot3d
# from celluloid import Camera
from scipy import spatial
# import pyshine as ps


class Posefunc:
    def __init__(self) -> None:
        self.MP_DRAWING = mp.solutions.drawing_utils
        self.MP_POSE = mp.solutions.pose

    def calculateAngle(self, a, b, c):
        """
        Doc
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
            np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    # cap = cv2.VideoCapture(0)
    # 2D

    def extractKeypoint(self, path):

        # print(IMAGE_FILES)
        # stage = None
        joint_list_video = pd.DataFrame([])
        count = 0

        with self.MP_POSE.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:

            image = cv2.imread(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image_h, image_w, _ = image.shape

            try:
                landmarks = results.pose_landmarks.landmark

                left_shoulder = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].y]

                left_elbow = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_ELBOW.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_ELBOW.value].y]

                left_wrist = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_WRIST.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].y]

                right_elbow = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_ELBOW.value].y]

                right_wrist = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_WRIST.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_WRIST.value].y]

                left_hip = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_HIP.value].y]

                left_knee = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_KNEE.value].y]

                left_ankle = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_ANKLE.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.LEFT_ANKLE.value].y]

                right_hip = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_HIP.value].y]

                right_knee = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_KNEE.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_KNEE.value].y]

                right_ankle = [
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_ANKLE.value].x,
                    landmarks[
                        self.MP_POSE.PoseLandmark.RIGHT_ANKLE.value].y]
                angle_Lst = [
                    right_elbow,
                    left_elbow,
                    right_shoulder,
                    left_shoulder,
                    right_hip,
                    left_hip,
                    right_knee,
                    left_knee
                ]
                joints = []
                joint_list = pd.DataFrame([])

                for i, data_point in zip(range(len(landmarks)), landmarks):
                    joints = pd.DataFrame({
                        'frame': count,
                        'id': i,
                        'x': data_point.x,
                        'y': data_point.y,
                        'z': data_point.z,
                        'vis': data_point.visibility
                    }, index=[0])
                    """joint_list = joint_list.append(
                        joints, ignore_index=True)"""
                    joint_list = pd.concat(
                        [joint_list, joints],
                        ignore_index=True)

                keypoints = []
                for point in landmarks:
                    keypoints.append({
                        'X': point.x,
                        'Y': point.y,
                        'Z': point.z,
                    })

                angle = []
                # angle_list = pd.DataFrame([])
                angle1 = self.calculateAngle(
                    right_shoulder, right_elbow, right_wrist)
                angle.append(int(angle1))
                angle2 = self.calculateAngle(
                    left_shoulder, left_elbow, left_wrist)
                angle.append(int(angle2))
                angle3 = self.calculateAngle(
                    right_elbow, right_shoulder, right_hip)
                angle.append(int(angle3))
                angle4 = self.calculateAngle(
                    left_elbow, left_shoulder, left_hip)
                angle.append(int(angle4))
                angle5 = self.calculateAngle(
                    right_shoulder, right_hip, right_knee)
                angle.append(int(angle5))
                angle6 = self.calculateAngle(
                    left_shoulder, left_hip, left_knee)
                angle.append(int(angle6))
                angle7 = self.calculateAngle(
                    right_hip, right_knee, right_ankle)
                angle.append(int(angle7))
                angle8 = self.calculateAngle(
                    left_hip, left_knee, left_ankle)
                angle.append(int(angle8))

                for idx, agl in enumerate(angle_Lst):
                    cv2.putText(image,
                                str(idx+1),
                                tuple(np.multiply(agl, [
                                    image_w, image_h,]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                [255, 255, 0],
                                2,
                                cv2.LINE_AA
                                )

    #             if angle >120:
    #                 stage = "down"
    #             if angle <30 and stage == 'down':
    #                 stage = "up"
    #                 counter +=1

            except Exception as e:
                print("Error in drawing bones", e)
            joint_list_video = pd.concat(
                [joint_list_video, joint_list], ignore_index=True)
            cv2.rectangle(image, (0, 0), (100, 255), (255, 255, 255), -1)
            # ====================================================================
            cv2.putText(
                image, 'ID', (10, 14),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                [0, 0, 255], 2, cv2.LINE_AA)
            for i in range(1, 9):
                cv2.putText(
                    image, str(i), (10, ((i*30)+10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    [0, 153, 0], 2, cv2.LINE_AA)
            # ====================================================================
            cv2.putText(
                image, 'Angle', (40, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                [0, 0, 255], 2, cv2.LINE_AA)
            for i in range(8):
                cv2.putText(
                    image, str(int(angle[i])), ((40, (i*30)+40)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    [0, 153, 0], 2, cv2.LINE_AA)
            # ====================================================================
            # Render detections
            self.MP_DRAWING.draw_landmarks(
                image, results.pose_landmarks,
                self.MP_POSE.POSE_CONNECTIONS,
                self.MP_DRAWING.DrawingSpec(
                    color=(0, 0, 255),
                    thickness=4, circle_radius=2),
                self.MP_DRAWING.DrawingSpec(
                    color=(0, 255, 0), thickness=4, circle_radius=2)
            )

            # cv2.imshow('MediaPipe Feed',image)

            if cv2.waitKey(0) & 0xFF == ord('q'):
                print("00000000000000")

            cv2.destroyAllWindows()
        return landmarks, keypoints, angle, image

    def classifyPose(self, landmarks, output_image, display=False):

        # Initialize the label of the pose. It is not known at this stage.
        label = 'Unknown Pose'
        color = (0, 0, 255)
        left_shoulder = landmarks[
            self.MP_POSE.PoseLandmark.LEFT_SHOULDER.value]
        left_elbow = landmarks[self.MP_POSE.PoseLandmark.LEFT_ELBOW.value]
        left_wrist = landmarks[self.MP_POSE.PoseLandmark.LEFT_WRIST.value]
        right_shoulder = landmarks[
            self.MP_POSE.PoseLandmark.RIGHT_SHOULDER.value]
        right_elbow = landmarks[self.MP_POSE.PoseLandmark.RIGHT_ELBOW.value]
        right_wrist = landmarks[self.MP_POSE.PoseLandmark.RIGHT_WRIST.value]
        left_hip = landmarks[self.MP_POSE.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[self.MP_POSE.PoseLandmark.LEFT_KNEE.value]
        left_ankle = landmarks[self.MP_POSE.PoseLandmark.LEFT_ANKLE.value]
        right_hip = landmarks[self.MP_POSE.PoseLandmark.RIGHT_HIP.value]
        right_knee = landmarks[self.MP_POSE.PoseLandmark.RIGHT_KNEE.value]
        right_ankle = landmarks[self.MP_POSE.PoseLandmark.RIGHT_ANKLE.value]

        angle1 = self.calculateAngle(right_shoulder, right_elbow, right_wrist)

        angle2 = self.calculateAngle(left_shoulder, left_elbow, left_wrist)

        angle3 = self.calculateAngle(right_elbow, right_shoulder, right_hip)

        angle4 = self.calculateAngle(left_elbow, left_shoulder, left_hip)

        angle5 = self.calculateAngle(right_shoulder, right_hip, right_knee)

        angle6 = self.calculateAngle(left_shoulder, left_hip, left_knee)

        angle7 = self.calculateAngle(right_hip, right_knee, right_ankle)

        angle8 = self.calculateAngle(left_hip, left_knee, left_ankle)

        if angle2 > 160 and angle2 < 195 and angle1 > 160 and angle1 < 195:

            if angle4 > 70 and angle4 < 110 and angle3 > 70 and angle3 < 110:

                if ((angle8 > 165) and (angle8 < 195) or
                        (angle7 > 165) and (angle7 < 195)):

                    if ((angle8 > 80) and (angle8 < 120) or
                            (angle7 > 80) and (angle7 < 120)):

                        label = 'Warrior II Pose'

                if ((angle8 > 160) and (angle8 < 195) and
                        (angle7 > 160) and (angle7 < 195)):

                    label = 'T Pose'

        if (
            (angle8 > 165 and angle8 < 195) or
                (angle7 > 165 and angle7 < 195)):

            if (angle7 > 25 and angle7 < 45) or (angle8 > 25 and angle8 < 45):

                label = 'Tree Pose'

        if label != 'Unknown Pose':

            color = (0, 0, 255)

        cv2.putText(output_image, label, (400, 50),
                    cv2.FONT_HERSHEY_PLAIN, 4, color, 4)
        cv2.rectangle(output_image, (0, 0), (100, 255), (255, 255, 255), -1)
        # ====================================================================
        cv2.putText(output_image, 'ID', (10, 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0, 0, 255], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(1), (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(2), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(3), (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(4), (10, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(5), (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(6), (10, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(7), (10, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(8), (10, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        # ====================================================================
        #                                                                    #
        # ====================================================================
        cv2.putText(output_image, 'Angle', (40, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0, 0, 255], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle1)), (40, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle2)), (40, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle3)), (40, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle4)), (40, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle5)), (40, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle6)), (40, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle7)), (40, 220),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        cv2.putText(output_image, str(int(angle8)), (40, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)

        if display:

            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1])
            plt.title("Output Image")
            plt.axis('off')

        else:

            return output_image, label

    def detectPose(self, image, pose, display=True):

        output_image = image.copy()
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(imageRGB)
        height, width, _ = image.shape
        landmarks = []
        if results.pose_landmarks:

            self.MP_DRAWING.draw_landmarks(
                output_image,
                results.pose_landmarks,
                self.MP_POSE.POSE_CONNECTIONS,
                self.MP_DRAWING.DrawingSpec(
                    color=(0, 0, 255),
                    thickness=5, circle_radius=2),
                self.MP_DRAWING.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=5, circle_radius=2)
            )
            for landmark in results.pose_landmarks.landmark:

                landmarks.append((int(landmark.x * width),
                                  int(landmark.y * height),
                                  (landmark.z * width)))
        if display:
            plt.figure(figsize=[22, 22])
            plt.subplot(121)
            plt.imshow(image[:, :, ::-1])
            plt.title("Original Image")
            plt.axis('off')
            plt.subplot(122)
            plt.imshow(output_image[:, :, ::-1])
            plt.title("Output Image")
            plt.axis('off')

            self.MP_DRAWING.plot_landmarks(
                results.pose_world_landmarks, self.MP_POSE.POSE_CONNECTIONS)

        else:
            return output_image, landmarks

    @staticmethod
    def compare_pose(image, angle_point, angle_user, angle_target):
        angle_user = np.array(angle_user)
        angle_target = np.array(angle_target)
        angle_point = np.array(angle_point)
        stage = 0
        cv2.rectangle(image, (0, 0), (370, 40), (255, 255, 255), -1)
        cv2.rectangle(image, (0, 40), (370, 370), (255, 255, 255), -1)
        cv2.putText(image, str("Score:"), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
        height, width, _ = image.shape

        text_list = [
            ["Extend the right arm at elbow",
                "Fold the right arm at elbow"],  # 0
            ["Extend the left arm at elbow",
                "Fold the left arm at elbow"],  # 1
            ["Lift your right arm",
                "Put your right arm down a little"],  # 2
            ["Lift your left arm",
                "Put your arm down a little"],  # 3
            ["Extend the angle at right hip",
                "Reduce the angle of at right hip"],  # 4
            ["Extend the angle at left hip",
                "Reduce the angle at left hip"],  # 5
            ["Extend the angle of right knee",
                "Reduce the angle at right knee"],  # 6
            ["Extend the angle at left knee",
                "Reduce the angle at left knee"]  # 7
        ]

        for i in range(len(angle_user)):
            if angle_user[i] < (angle_target[i] - 15):
                stage += 1
                cv2.putText(
                    image, str(text_list[i][0]), (10, ((i*40)+60)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
                cv2.circle(image, (
                    int(angle_point[i][0]*width),
                    int(angle_point[i][1]*height)), 30, (0, 0, 255), 5)

            if angle_user[i] > (angle_target[i] + 15):
                stage += 1
                cv2.putText(
                    image, str(text_list[i][1]), (10, ((i*40)+80)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0, 153, 0], 2, cv2.LINE_AA)
                cv2.circle(image, (
                    int(angle_point[i][0]*width),
                    int(angle_point[i][1]*height)), 30, (0, 0, 255), 5)

        if stage != 0:
            # print("FIGHTING!")
            cv2.putText(
                image, str("FIGHTING!"), (170, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 2, cv2.LINE_AA)

            pass
        else:
            # print("PERFECT")
            cv2.putText(
                image, str("PERFECT"), (170, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 2, cv2.LINE_AA)

    def Average(self, lst) -> float:
        return sum(lst) / len(lst)

    def dif_compare(self, x, y):
        average = np.array([])
        for i, j in zip(range(len(list(x))), range(len(list(y)))):
            result = 1 - \
                spatial.distance.cosine(
                    list(x[i].values()), list(y[j].values()))
            average = np.append(average, result)
        score = math.sqrt(2*(1-round((self.Average(average)), 2)))
        # print(Average(average))
        return score

    def diff_compare(self, x, y) -> float:
        average = []
        for i, j in zip(range(len(x)), range(len(y))):
            result = 1 - spatial.distance.cosine(x[i], y[j])
            average.append(result)
        score = math.sqrt(2*(1-round(self.Average(average), 2)))
        print(self.Average(average))
        return score

    def diff_compare_angle(self, x, y) -> float:
        new_x = []
        for i, j in zip(range(len(x)), range(len(y))):
            z = np.abs(x[i] - y[j])/((x[i] + y[j])/2)
            new_x.append(z)
            # print(new_x[i])
        return (self.Average(new_x))

    def cal_acc(self, angle_list: list, target_list: list) -> list:
        res = []
        try:
            for i in range(8):
                dis = pow(((target_list[i] - angle_list[i])/180.0), 2)
                res.append(dis)
        except Exception as e:
            print(e)

        return res

    @staticmethod
    def convert_data(landmarks):
        df = pd.DataFrame(columns=['x', 'y', 'z', 'vis'])
        for i in range(len(landmarks)):
            df = df.append({"x": landmarks[i].x,
                            "y": landmarks[i].y,
                            "z": landmarks[i].z,
                            "vis": landmarks[i].visibility
                            }, ignore_index=True)
        return df

    def segment(p1, p2):

        fig = plt.figure(1)
        ax = fig.gca(projection='3d')
        p1 = np.array(p1)

        p2 = np.array(p2)
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        z = [p1[2], p2[2]]
        ax.scatter(x, y, z)
        ax.plot(x, y, z, c='r')

    def L2_normal(x):
        new_x = []
        for i in range(len(x)):
            z = list(x[i].values())/np.linalg.norm(list(x[i].values()))
            new_x.append(z)
            print(x[i])
        return new_x

    def load(self, dir, num):
        filenames = os.listdir(dir)
        x = self.extractKeypoint(dir+"\\"+filenames[num])
        resized = cv2.resize(x[3], (860, 960), interpolation=cv2.INTER_AREA)
        angle_target = x[2]
        point_target = x[1]
        return resized, angle_target, point_target
