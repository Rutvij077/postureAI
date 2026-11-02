def generate_feedback(measurements):

    feedback = []

    # Check whether measurements are reliable
    if measurements["status"] != "measurements_available":
        return [measurements["message"]]

    head_offset = measurements["head_offset"]

    torso_angle = measurements["torso_angle_degrees"]

    # Head alignment check
    if abs(head_offset) > 0.15:
        feedback.append(
            "Your head appears displaced relative to your shoulder. "
            "Try maintaining a neutral head position."
        )
    else:
        feedback.append(
            "Head alignment appears relatively neutral."
        )

    # Torso measurement availability
    if torso_angle is not None:
        feedback.append(
            f"Estimated torso inclination: {torso_angle} degrees."
        )
    else:
        feedback.append(
            "Unable to estimate torso inclination."
        )

    return feedback