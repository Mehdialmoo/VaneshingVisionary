import cv2
from utilities import Posefunc

P = Posefunc()
cap = cv2.VideoCapture(0)
path = r"./gp/VaneshingVisionary/RTP/video/yoga_data"
x = P.extractKeypoint(path)
dim = (960, 760)
resized = cv2.resize(x[3], dim, interpolation=cv2.INTER_AREA)
cv2.imshow('target', resized)
angle_target = x[2]
point_target = x[1]

with P.MP_POSE.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape
        image = cv2.resize(
            image, (int(image_width * (860 / image_height)), 860))
        # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        try:
            landmarks = results.pose_landmarks.landmark
            print(results.pose_landmarks)
            shoulder = [
                landmarks[P.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[P.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].y,
                landmarks[P.MP_POSE.PoseLandmark.LEFT_SHOULDER.value].z,
                round(
                    landmarks[
                        P.MP_POSE.PoseLandmark.LEFT_SHOULDER.value
                    ].visibility*100, 2)]
            elbow = [
                landmarks[P.MP_POSE.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[P.MP_POSE.PoseLandmark.LEFT_ELBOW.value].y,
                landmarks[P.MP_POSE.PoseLandmark.LEFT_ELBOW.value].z,
                round(
                    landmarks[
                        P.MP_POSE.PoseLandmark.LEFT_ELBOW.value
                    ].visibility*100, 2)]
            wrist = [
                landmarks[P.MP_POSE.PoseLandmark.LEFT_WRIST.value].x,
                landmarks[P.MP_POSE.PoseLandmark.LEFT_WRIST.value].y,
                landmarks[P.MP_POSE.PoseLandmark.LEFT_WRIST.value].z,
                round(
                    landmarks[
                        P.MP_POSE.PoseLandmark.LEFT_WRIST.value
                    ].visibility*100, 2)]

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

            angle1 = P.calculateAngle(right_shoulder, right_elbow, right_wrist)
            angle.append(int(angle1))
            angle2 = P.calculateAngle(left_shoulder, left_elbow, left_wrist)
            angle.append(int(angle2))
            angle3 = P.calculateAngle(right_elbow, right_shoulder, right_hip)
            angle.append(int(angle3))
            angle4 = P.calculateAngle(left_elbow, left_shoulder, left_hip)
            angle.append(int(angle4))
            angle5 = P.calculateAngle(right_shoulder, right_hip, right_knee)
            angle.append(int(angle5))
            angle6 = P.calculateAngle(left_shoulder, left_hip, left_knee)
            angle.append(int(angle6))
            angle7 = P.calculateAngle(right_hip, right_knee, right_ankle)
            angle.append(int(angle7))
            angle8 = P.calculateAngle(left_hip, left_knee, left_ankle)
            angle.append(int(angle8))

            P.compare_pose(image, angle_point, angle, angle_target)
            a_score = P.diff_compare_angle(angle, angle_target)

            if (p_score >= a_score):
                cv2.putText(
                    image, str(int((1 - a_score)*100)), (80, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 2, cv2.LINE_AA)

            else:
                cv2.putText(
                    image, str(int((1 - p_score)*100)), (80, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 2, cv2.LINE_AA)

        except None:
            pass

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

        cv2.imshow('MediaPipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
