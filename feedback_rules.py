def generate_feedback(measurements):
    feedback = []

    if measurements["status"] != "measurements_available":
        return [measurements["message"]]

    head_offset = measurements["head_offset"]

    # Initial heuristic threshold, to be calibrated later
    if abs(head_offset) > 0.15:
        feedback.append(
            "Your head appears displaced relative to your shoulder. "
            "Try maintaining a more neutral head position."
        )
    else:
        feedback.append("Head alignment appears relatively neutral.")

    return feedback