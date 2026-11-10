from measurement_smoothing import TorsoStabilityTracker

tracker = TorsoStabilityTracker(window_size=5)

# Simulate relatively stable torso movement
stable_angles = [5, 5.5, 6, 5.2, 5.8]

print("Stable movement:")

for angle in stable_angles:
    variation = tracker.update(angle)
    print("Variation:", variation)


# Reset tracker
tracker.reset()


# Simulate greater torso movement
unstable_angles = [5, 9, 15, 20, 25]

print("\nGreater movement:")

for angle in unstable_angles:
    variation = tracker.update(angle)
    print("Variation:", variation)