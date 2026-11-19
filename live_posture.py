import cv2
import mediapipe as mp

from exercise_controls import get_next_exercise
from posture_engine import ExerciseAnalyzer
from feedback_rules import generate_feedback


# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initial exercise
exercise = "squat"

# Initialize analysis coordinator
analyzer = ExerciseAnalyzer(stability_window=30)


try:

    if not cap.isOpened():
        raise RuntimeError("Unable to open webcam.")

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        # Convert BGR to RGB
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Detect pose
        results = pose.process(rgb)

        if results.pose_landmarks:

            # Draw detected skeleton
            mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

            # Run unified analysis pipeline
            result = analyzer.analyze_frame(
                results.pose_landmarks.landmark,
                exercise,
                width,
                height
            )

            # Generate feedback from analysis result
            feedback = generate_feedback(result)

        # Display static hold progress
        if exercise in ["plank", "wall_sit"]:

            measurements = result.get("measurements", {})

            duration = measurements.get(
                "hold_duration_seconds", 0
            )

            target = measurements.get(
                "hold_target_seconds", 30
            )

            completed = measurements.get(
                "hold_completed", False
            )

            hold_status = measurements.get(
                "hold_status", "INVALID"
            )

            status_colors = {
                "VALID": (0, 255, 0),
                "TEMPORARY LOSS": (0, 255, 255),
                "INVALID": (0, 0, 255)
            }

            status_color = status_colors.get(
                hold_status,
                (0, 0, 255)
            )

            progress = min(
                duration / target,
                1.0
            ) if target > 0 else 0

            progress_percent = int(progress * 100)

            # Progress information
            cv2.putText(
                frame,
                f"Hold: {duration:.1f} / {target} sec",
                (10, height - 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Posture: {hold_status}",
                (280, height - 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                status_color,
                2
            )

            # Progress bar background
            bar_x = 10
            bar_y = height - 65
            bar_width = 250
            bar_height = 15

            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (bar_x + bar_width, bar_y + bar_height),
                (100, 100, 100),
                -1
            )

            # Filled progress bar
            cv2.rectangle(
                frame,
                (bar_x, bar_y),
                (
                    bar_x + int(bar_width * progress),
                    bar_y + bar_height
                ),
                (0, 255, 0),
                -1
            )

            if completed:
                status = "TARGET COMPLETED"
            elif hold_status == "VALID":
                status = "HOLDING"
            elif hold_status == "TEMPORARY LOSS":
                status = "DETECTION LOST"
            else:
                status = "ADJUST POSTURE"

            cv2.putText(
                frame,
                f"{status} - {progress_percent}%",
                (10, height - 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

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

                if y_position > height - 60:
                    break

        else:

            # Clear temporal history after losing pose
            analyzer.reset()

            cv2.putText(
                frame,
                "No pose detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        # Display selected exercise
        cv2.putText(
            frame,
            f"Exercise: {exercise}",
            (280, height - 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.imshow(
            "PostureAI - Live Analysis",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("n"):

            exercise = get_next_exercise(exercise)

            # Reset temporal analysis
            analyzer.reset()

            print("Selected exercise:", exercise)


finally:

    # Release resources
    cap.release()
    pose.close()
    cv2.destroyAllWindows()
