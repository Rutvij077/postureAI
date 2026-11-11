
def generate_feedback(result):

    feedback = []

    # Extract the nested analysis result
    measurements = result.get("measurements", {})
    exercise = result.get("exercise", "unknown")

    missing = result.get("missing_measurements", [])

    # Check whether any measurements are available
    if not measurements:
        return [
            "Unable to analyse posture. Make sure your body is visible to the camera."
        ]

    # Exercise information
    feedback.append(f"Exercise: {exercise.replace('_', ' ').title()}")

    # 1. Head alignment feedback
    head_offset = measurements.get("head_offset")

    if head_offset is not None:

        # Experimental threshold; requires later validation
        if abs(head_offset) > 0.15:
            feedback.append(
                "Your head appears displaced relative to your shoulder. "
                "Try maintaining a neutral head position."
            )
        else:
            feedback.append(
                "Head alignment appears relatively neutral."
            )

    elif "head_alignment" in missing:
        feedback.append(
            "Unable to assess head alignment. Check camera visibility."
        )

    # 2. Torso inclination feedback
    torso_angle = measurements.get("torso_angle_degrees")

    if torso_angle is not None:
        feedback.append(
            f"Estimated torso inclination: {torso_angle} degrees."
        )

    elif "torso_inclination" in missing:
        feedback.append(
            "Unable to estimate torso inclination."
        )

    # 3. Torso stability feedback
    torso_variation = measurements.get(
        "torso_variation_degrees"
    )

    if torso_variation is not None:
        feedback.append(
            f"Torso angle variation: {torso_variation} degrees "
            "over the recent frames."
        )

    elif "torso_stability" in missing:
        feedback.append(
            "Collecting more frames to estimate torso stability."
        )

    # 4. Elbow angle feedback
    elbow_angle = measurements.get("elbow_angle_degrees")

    if elbow_angle is not None:
        feedback.append(
            f"Estimated elbow angle: {elbow_angle} degrees."
        )

    # 5. Report incomplete analysis
    if result.get("unsupported_measurements"):
        feedback.append(
            "Some requested measurements are not implemented yet."
        )

    return feedback
