from exercise_rules import EXERCISES


def get_exercise_list():
    return list(EXERCISES.keys())


def get_next_exercise(current_exercise):

    exercises = get_exercise_list()

    current_index = exercises.index(current_exercise)

    next_index = (current_index + 1) % len(exercises)

    return exercises[next_index]