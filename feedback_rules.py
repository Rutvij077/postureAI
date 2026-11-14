
def generate_feedback(result):

    feedback = []

    exercise = result.get("exercise", "unknown")
    measurements = result.get("measurements", {})
    missing = result.get("missing_measurements", [])
    unsupported = result.get("unsupported_measurements", [])

    exercise_name = exercise.replace("_", " ").title()

    if not measurements:
        return [
            f"Unable to analyse {exercise_name}. "
            "Make sure your body is visible to the camera."
        ]

    feedback.append(f"Exercise: {exercise_name}")

    # 1. Head alignment - common measurement
    head_offset = measurements.get("head_offset")

    if head_offset is not None:

        if abs(head_offset) > 0.15:
            feedback.append(
                "Your head appears displaced relative to your shoulder."
            )
        else:
            feedback.append(
                "Head alignment appears relatively neutral."
            )

    elif "head_alignment" in missing:
        feedback.append(
            "Unable to assess head alignment."
        )

    # 2. Exercise-specific measurements

    if exercise in [
        "squat",
        "deadlift",
        "romanian_deadlift",
        "bent_over_row",
        "forward_lunge"
    ]:

        torso_angle = measurements.get("torso_angle_degrees")

        if torso_angle is not None:
            feedback.append(
                f"Current torso inclination: {torso_angle} degrees."
            )

            feedback.append(
                "Interpret torso inclination according to the selected exercise."
            )

    # Squat and forward lunge
    if exercise in ["squat", "forward_lunge"]:

        knee_angle = measurements.get("knee_angle_degrees")

        if knee_angle is not None:
            feedback.append(
                f"Estimated knee angle: {knee_angle} degrees."
            )

    # Deadlift and Romanian deadlift
    if exercise in ["deadlift", "romanian_deadlift"]:

        hip_hinge = measurements.get("hip_hinge_degrees")

        if hip_hinge is not None:
            feedback.append(
                f"Estimated hip-hinge angle: {hip_hinge} degrees."
            )

    # Bicep curl
    if exercise == "bicep_curl":

        elbow_angle = measurements.get("elbow_angle_degrees")

        if elbow_angle is not None:
            feedback.append(
                f"Estimated elbow angle: {elbow_angle} degrees."
            )

        torso_variation = measurements.get(
            "torso_variation_degrees"
        )

        if torso_variation is not None:
            feedback.append(
                f"Recent torso angle variation: "
                f"{torso_variation} degrees."
            )
        else:
            feedback.append(
                "Collecting more frames to analyse torso stability."
            )

    # Push-up
    if exercise == "push_up":

        body_alignment = measurements.get(
            "body_alignment_degrees"
        )

        if body_alignment is not None:
            feedback.append(
                f"Estimated body alignment angle: "
                f"{body_alignment} degrees."
            )

        elbow_angle = measurements.get("elbow_angle_degrees")

        if elbow_angle is not None:
            feedback.append(
                f"Estimated elbow angle: {elbow_angle} degrees."
            )

    # Plank
    if exercise == "plank":

        body_alignment = measurements.get(
            "body_alignment_degrees"
        )

        hip_deviation = measurements.get(
            "hip_deviation_pixels"
        )

        if body_alignment is not None:
            feedback.append(
                f"Estimated body alignment angle: "
                f"{body_alignment} degrees."
            )

        if hip_deviation is not None:
            feedback.append(
                f"Hip deviation from shoulder-ankle line: "
                f"{hip_deviation} pixels."
            )

    # Lat pulldown and shoulder press
    if exercise in ["lat_pulldown", "shoulder_press"]:

        shoulder_asymmetry = measurements.get(
            "shoulder_asymmetry_pixels"
        )

        if shoulder_asymmetry is not None:
            feedback.append(
                f"Vertical shoulder difference: "
                f"{shoulder_asymmetry} pixels."
            )

        # Additional lat pulldown feedback
        if exercise == "lat_pulldown":

            torso_alignment = measurements.get(
                "torso_alignment_degrees"
            )

            if torso_alignment is not None:
                feedback.append(
                    f"Estimated front-view torso alignment: "
                    f"{torso_alignment} degrees."
                )
    # Report unavailable measurements
    if missing:
        feedback.append(
            "Some measurements could not be calculated. "
            "Check your camera angle and landmark visibility."
        )

    if unsupported:
        feedback.append(
            "Some exercise measurements are not implemented yet: "
            + ", ".join(unsupported)
        )

    return feedback
