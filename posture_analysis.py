
import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

def calculate_angle(a, b, c):
    """Calculate angle ABC in degrees."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (
        np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8
    )

    cosine = np.clip(cosine, -1.0, 1.0)
    return np.degrees(np.arccos(cosine))


while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Select left side landmarks
        ear = landmarks[7]
        shoulder = landmarks[11]
        hip = landmarks[23]

        # Check landmark visibility
        if min(ear.visibility, shoulder.visibility, hip.visibility) > 0.5:

            # Calculate head displacement relative to shoulder
            head_offset = ear.x - shoulder.x

            # Calculate torso inclination relative to vertical
            torso_angle = calculate_angle(
                (hip.x, hip.y - 1),
                (hip.x, hip.y),
                (shoulder.x, shoulder.y)
            )

            # Display skeleton
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            cv2.putText(
                frame,
                f"Head offset: {head_offset:.3f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Torso angle: {torso_angle:.1f} deg",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    cv2.imshow("PostureAI - Analysis", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
pose.close()
cv2.destroyAllWindows()
