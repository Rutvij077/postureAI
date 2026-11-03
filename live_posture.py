import cv2
import mediapipe as mp

from posture_engine import analyze_posture
from feedback_rules import generate_feedback
from measurement_smoothing import MeasurementSmoother

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


cap = cv2.VideoCapture(0)

exercise = "squat"

smoother = MeasurementSmoother(window_size=5)


while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect pose
    results = pose.process(rgb)

    if results.pose_landmarks:

        # Draw skeleton
        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

       # Calculate raw measurements
        measurements = analyze_posture(
            results.pose_landmarks.landmark,
            exercise,
            width,
            height
        )

        # Smooth measurements
        measurements = smoother.smooth(measurements)

        # Generate feedback
        feedback = generate_feedback(measurements)

        # Display feedback
        y_position = 30

        for message in feedback:

            cv2.putText(
                frame,
                message[:65],
                (10, y_position),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            y_position += 30

    else:

        cv2.putText(
            frame,
            "No pose detected",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    cv2.imshow("PostureAI - Live Analysis", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Release resources
cap.release()
pose.close()
cv2.destroyAllWindows()