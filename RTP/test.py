cap = cv2.VideoCapture(0)
path = "Video/yoga10.jpg"
x = extractKeypoint(path)
dim = (960, 760)
resized = cv2.resize(x[3], dim, interpolation=cv2.INTER_AREA)
cv2.imshow('target', resized)
angle_target = x[2]
point_target = x[1]

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

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

        #
        try:
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,
                        round(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility*100, 2)]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,
                     round(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility*100, 2)]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z,
                     round(landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility*100, 2)]

            angle_point = []

            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            angle_point.append(right_elbow)

            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            angle_point.append(left_elbow)

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            angle_point.append(right_shoulder)

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            angle_point.append(left_shoulder)

            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            angle_point.append(right_hip)

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            angle_point.append(left_hip)

            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            angle_point.append(right_knee)

            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            angle_point.append(left_knee)
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            keypoints = []
            for point in landmarks:
                keypoints.append({
                    'X': point.x,
                    'Y': point.y,
                    'Z': point.z,
                })

            p_score = dif_compare(keypoints, point_target)

            angle = []

            angle1 = calculateAngle(right_shoulder, right_elbow, right_wrist)
            angle.append(int(angle1))
            angle2 = calculateAngle(left_shoulder, left_elbow, left_wrist)
            angle.append(int(angle2))
            angle3 = calculateAngle(right_elbow, right_shoulder, right_hip)
            angle.append(int(angle3))
            angle4 = calculateAngle(left_elbow, left_shoulder, left_hip)
            angle.append(int(angle4))
            angle5 = calculateAngle(right_shoulder, right_hip, right_knee)
            angle.append(int(angle5))
            angle6 = calculateAngle(left_shoulder, left_hip, left_knee)
            angle.append(int(angle6))
            angle7 = calculateAngle(right_hip, right_knee, right_ankle)
            angle.append(int(angle7))
            angle8 = calculateAngle(left_hip, left_knee, left_ankle)
            angle.append(int(angle8))

            compare_pose(image, angle_point, angle, angle_target)
            a_score = diff_compare_angle(angle, angle_target)

            if (p_score >= a_score):
                cv2.putText(image, str(int((1 - a_score)*100)), (80, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 2, cv2.LINE_AA)

            else:
                cv2.putText(image, str(int((1 - p_score)*100)), (80, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 0, 255], 2, cv2.LINE_AA)

        except:
            pass

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(
                                      color=(0, 0, 255), thickness=4, circle_radius=4),
                                  mp_drawing.DrawingSpec(
                                      color=(0, 255, 0), thickness=3, circle_radius=3)
                                  )


#         cv2.putText(output_image, 'ID', (10,14), cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0,0,255], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(1), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(2), (10,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(3), (10,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(4), (10,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(5), (10,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(6), (10,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(7), (10,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(8), (10,250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)

#         cv2.putText(output_image, 'Angle', (40,12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, [0,0,255], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle1)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle2)), (40,70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle3)), (40,100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle4)), (40,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle5)), (40,160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle6)), (40,190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle7)), (40,220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)
#         cv2.putText(output_image, str(int(angle8)), (40,250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [0,153,0], 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
