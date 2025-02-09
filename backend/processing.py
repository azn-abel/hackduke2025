import cv2
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import math

# Load MoveNet model for pose estimation
model = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
movenet = model.signatures['serving_default']

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

    data = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = tf.image.resize_with_pad(tf.convert_to_tensor(frame_rgb), 192, 192)
        input_image = tf.cast(frame_resized, dtype=tf.int32)

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

        # Overlay angles on the frame
        cv2.putText(frame, f"Elbow: {int(elbow_angle)} deg", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Knee: {int(knee_angle)} deg", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Ankle: {int(ankle_angle)} deg", (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Trunk: {int(trunk_angle)} deg", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        out.write(frame)
        frame_id += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['Frame', 'Elbow Angle', 'Knee Angle', 'Ankle Angle', 'Trunk Angle'])
    
    # Identify preparatory and release phase angles
    preparatory_phase = df.loc[df['Knee Angle'].idxmin()]
    release_phase = df.loc[df['Elbow Angle'].idxmax()]

    # returning phase details
    return [preparatory_phase, release_phase]

'''
# Example Usage
video_path = "bbshot1.mp4"
output_video = "basketball_shot_analysis.mp4"
processVideo(video_path, output_video)
'''
