import cv2
import numpy as np
import pandas as pd
import math
import mediapipe as mp
import os

# MediaPipe for the calculations and the overlay for the annotated video
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing = mp.solutions.drawing_utils

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # suppressing some annoying warnings

# Function to calculate the angle between three points
def calculate_angle(p1, p2, p3):
    """Calculate angle between three points using vector math."""
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude2 = math.sqrt(v2[0]**2 + v2[1]**2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0  # Avoid division by zero

    angle = math.degrees(math.acos(dot_product / (magnitude1 * magnitude2)))
    return angle

# Function to process the video, calculate angles, and overlay skeleton
def processVideo(video_path, output_video):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    frame_id = 0
    angle_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            # Draw skeleton overlay
            drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                connection_drawing_spec=drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

            # Extract key landmarks
            landmarks = results.pose_landmarks.landmark

            def get_coords(index):
                return (int(landmarks[index].x * width), int(landmarks[index].y * height))

            # Extract body part coordinates
            shoulder = get_coords(11)  # visible side
            elbow = get_coords(13)
            wrist = get_coords(15) 
            hip = get_coords(23)
            knee = get_coords(25)
            ankle = get_coords(27)

            # Create a virtual ground reference for ankle angle
            ground_ref = (ankle[0] + 50, ankle[1])

            # Calculate angles
            elbow_angle = calculate_angle(shoulder, elbow, wrist)
            knee_angle = calculate_angle(hip, knee, ankle)
            ankle_angle = calculate_angle(knee, ankle, ground_ref)

            # Store angle data
            angle_data.append([frame_id, elbow_angle, knee_angle, ankle_angle])

            # Overlay angles on the frame
            cv2.putText(frame, f"Elbow: {int(elbow_angle)} deg", (elbow[0]-30, elbow[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Knee: {int(knee_angle)} deg", (knee[0]-30, knee[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Ankle: {int(ankle_angle)} deg", (ankle[0]-30, ankle[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    angle_data = np.array(angle_data)
    preparatory_phase = angle_data[np.argmin(angle_data[:, 1])]  # Min elbow angle
    release_phase = angle_data[np.argmax(angle_data[:, 1])]  # Max elbow angle

    preparatory_phase = {"Elbow": preparatory_phase[0], "Knee": preparatory_phase[1], "Ankle": preparatory_phase[2]}
    release_phase = {"Elbow": release_phase[0], "Knee": release_phase[1], "Ankle": release_phase[2]}

    return {"Preparatory": preparatory_phase, "Release": release_phase}
