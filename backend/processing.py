import cv2
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import math
import mediapipe as mp

# Load MoveNet model for pose estimation, MediaPipe for the overlay for the annotated video
model = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
movenet = model.signatures['serving_default']
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing = mp.solutions.drawing_utils

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc = a - b, c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle

# processing the video: determining angles of preparatory/release phases and also returning annotated video
def processVideo(video_path, output_video):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    elbow_angles = []
    knee_angles = []
    ankle_angles = []
    trunk_angles = []
    timestamps = []
    
    data = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = tf.image.resize_with_pad(tf.convert_to_tensor(frame_rgb), 192, 192)
        input_image = tf.cast(frame_resized, dtype=tf.int32)
        results = pose.process(frame_rgb)
        if results.pose_landmarks:
            # Draw landmarks and skeleton on frame
            drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=3),
                connection_drawing_spec=drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

            # Extract key landmarks
            landmarks = results.pose_landmarks.landmark

            # Keypoints for angle calculations
            shoulder = (int(landmarks[11].x * width), int(landmarks[11].y * height))
            elbow = (int(landmarks[13].x * width), int(landmarks[13].y * height))
            wrist = (int(landmarks[15].x * width), int(landmarks[15].y * height))
            hip = (int(landmarks[23].x * width), int(landmarks[23].y * height))
            knee = (int(landmarks[25].x * width), int(landmarks[25].y * height))
            ankle = (int(landmarks[27].x * width), int(landmarks[27].y * height))

            # Calculate angles
            elbow_angle = calculate_angle(shoulder, elbow, wrist)
            knee_angle = calculate_angle(hip, knee, ankle)
            ankle_angle = calculate_angle(knee, ankle, (ankle[0], ankle[1] + 50))  # Reference vertical
            trunk_angle = calculate_angle(hip, shoulder, (shoulder[0], hip[1]))  # Reference horizontal

            # Store angles for CSV output
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)  # Convert ms to seconds
            elbow_angles.append(elbow_angle)
            knee_angles.append(knee_angle)
            ankle_angles.append(ankle_angle)
            trunk_angles.append(trunk_angle)

            # Overlay angles on the frame
            cv2.putText(frame, f"Elbow: {int(elbow_angle)} deg", (elbow[0]-30, elbow[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Knee: {int(knee_angle)} deg", (knee[0]-30, knee[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Ankle: {int(ankle_angle)} deg", (ankle[0]-30, ankle[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(frame, f"Trunk: {int(trunk_angle)} deg", (hip[0]-30, hip[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # Write processed frame to output video
        out.write(frame)
        # Run MoveNet model
        outputs = movenet(tf.expand_dims(input_image, axis=0))
        keypoints = outputs['output_0'].numpy().reshape(17, 3)

        # Extract required keypoints
        shoulder, elbow, wrist = keypoints[5][:2], keypoints[7][:2], keypoints[9][:2]
        hip, knee, ankle, foot = keypoints[11][:2], keypoints[13][:2], keypoints[15][:2], keypoints[16][:2]

        # Calculate angles
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        knee_angle = calculate_angle(hip, knee, ankle)
        ankle_angle = calculate_angle(knee, ankle, foot)
        trunk_angle = calculate_angle(hip, shoulder, [shoulder[0], hip[1]])

        data.append([frame_id, elbow_angle, knee_angle, ankle_angle, trunk_angle])

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['Frame', 'Elbow Angle', 'Knee Angle', 'Ankle Angle', 'Trunk Angle'])
    
    # Identify preparatory and release phase angles
    preparatory_phase = [df['Elbow Angle'].min(), df['Knee Angle'].min(), df['Ankle Angle'].min(), df['Trunk Angle'].min()]
    release_phase = [df['Elbow Angle'].max(), df['Knee Angle'].max(), df['Ankle Angle'].max(), df['Trunk Angle'].max()]

    return [preparatory_phase, release_phase]
