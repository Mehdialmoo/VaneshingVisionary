import cv2
import os
from utilities import Posefunc
import numpy as np

path = "./RTP/video/yoga_data/"
joint_dic ={ 
    'RIGHT_ELBOW':14,
    'LEFT_SHOULDER':11,
    'RIGHT_SHOULDER':12,
    'LEFT_ELBOW':13,
    'RIGHT_WRIST':16,
    'LEFT_WRIST':15,
    'RIGHT_HIP':24,
    'LEFT_HIP':23,
    'RIGHT_KNEE':26,
    'LEFT_KNEE':25,
    'RIGHT_ANKLE':28,
    'LEFT_ANKLE':27
}
angle_dic = {
    1:'RIGHT_ELBOW',
    2:'LEFT_ELBOW',
    3:'RIGHT_SHOULDER',
    4:'LEFT_SHOULDER',
    5:'RIGHT_HIP',
    6:'LEFT_HIP',
    7:'RIGHT_KNEE',
    8:'LEFT_KNEE'
}

cal_list = [
    ['RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_WRIST'],
    ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST'],
    ['LEFT_ELBOW', 'RIGHT_SHOULDER', 'RIGHT_HIP'],
    ['LEFT_ELBOW', 'LEFT_SHOULDER', 'LEFT_HIP'],
    ['RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE'],
    ['LEFT_SHOULDER', 'LEFT_HIP','LEFT_KNEE'],
    ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE'],
    ['LEFT_HIP','LEFT_KNEE','LEFT_ANKLE'],
]



def test():
    P = Posefunc()
    cap = cv2.VideoCapture(0)

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
                    print(results.pose_landmarks)
                    
                    angle_point = []

                    right_elbow = [
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_ELBOW.value].y]
                    angle_point.append(right_elbow)

                    left_elbow = [
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_ELBOW.value].y]
                    angle_point.append(left_elbow)

                    right_shoulder = [
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_SHOULDER.value].y]
                    angle_point.append(right_shoulder)

                    left_shoulder = [
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].y]
                    angle_point.append(left_shoulder)

                    right_wrist = [
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_WRIST.value].y]

                    left_wrist = [
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_WRIST.value].y]

                    right_hip = [
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_HIP.value].y]
                    angle_point.append(right_hip)

                    left_hip = [
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_HIP.value].y]
                    angle_point.append(left_hip)

                    right_knee = [
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_KNEE.value].y]
                    angle_point.append(right_knee)

                    left_knee = [
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_KNEE.value].y]
                    angle_point.append(left_knee)
                    right_ankle = [
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_ANKLE.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.RIGHT_ANKLE.value].y]

                    left_ankle = [
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_ANKLE.value].x,
                        landmarks[P.MP_POSE.PoseLandmark.LEFT_ANKLE.value].y]

                    keypoints = []
                    for point in landmarks:
                        keypoints.append({
                            'X': point.x,
                            'Y': point.y,
                            'Z': point.z,
                        })

                    p_score = P.dif_compare(keypoints, point_target)

                    angle = []

                    angle1 = P.calculateAngle(
                        right_shoulder, right_elbow, right_wrist)
                    angle.append(int(angle1))
                    angle2 = P.calculateAngle(
                        left_shoulder, left_elbow, left_wrist)
                    angle.append(int(angle2))
                    angle3 = P.calculateAngle(
                        right_elbow, right_shoulder, right_hip)
                    angle.append(int(angle3))
                    angle4 = P.calculateAngle(
                        left_elbow, left_shoulder, left_hip)
                    angle.append(int(angle4))
                    angle5 = P.calculateAngle(
                        right_shoulder, right_hip, right_knee)
                    angle.append(int(angle5))
                    angle6 = P.calculateAngle(
                        left_shoulder, left_hip, left_knee)
                    angle.append(int(angle6))
                    angle7 = P.calculateAngle(
                        right_hip, right_knee, right_ankle)
                    angle.append(int(angle7))
                    angle8 = P.calculateAngle(left_hip, left_knee, left_ankle)
                    angle.append(int(angle8))

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

if __name__ == "__main__":
    test()