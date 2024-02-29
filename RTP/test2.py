import cv2
from utilities import Posefunc


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

P = Posefunc()

x = P.extractKeypoint(r"./RTP/video/yoga10.jpg")

cv2.imshow('MediaPipe Feed', x[3])
cv2.waitKey(0)
cv2.destroyAllWindows()

y = P.extractKeypoint(r"./RTP/video/yoga11.jpg")

cv2.imshow('MediaPipe Feed', y[3])
cv2.waitKey(0)
cv2.destroyAllWindows()

P.dif_compare(x[1], y[1])
P.diff_compare_angle(x[2], y[2])

df1 = P.convert_data(x[0])

df2 = P.convert_data(y[0])


# %matplotlib notebook


P.visualization(df1)
#

P.visualization(df2)


# realtime to detect the pose
camera_video = cv2.VideoCapture(0)

cv2.namedWindow('Human Pose', cv2.WINDOW_NORMAL)

while camera_video.isOpened():

    ok, frame = camera_video.read()

    if not ok:

        continue
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    frame = cv2.resize(frame, (int(frame_width * (860 / frame_height)), 860))

    frame, landmarks = P.detectPose(frame, P.MP_POSE.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5),
        display=False)

    if landmarks:
        frame, _ = P.classifyPose(landmarks, frame, display=False)
    cv2.imshow('Human Pose', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    camera_video.release()
    cv2.destroyAllWindows()

    image = cv2.imread(r"./RTP/video/yoga25.jpg")
    cv2.imshow('window_name', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    output_image, landmarks = P.detectPose(image, P.MP_POSE.Pose(
        min_detection_confidence=0.5, min_tracking_confidence=0.5), display=False)
    if landmarks:
        P.classifyPose(landmarks, output_image, display=True)
