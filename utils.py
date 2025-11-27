def calc_assessments_average(assessments):
    """
    Return the average from a given list of assessments.
    The average should only apply for assessments that have been completed
    (where the grade isn't None). If list is empty return 0.
    """

    weight_completed = 0
    earned = 0
    for assessment in assessments:
        # skip assessments that haven't been completed
        if assessment.grade is None:
            continue
        earned += assessment.weight * (assessment.grade / 100)
        weight_completed += assessment.weight

    if weight_completed == 0:
        return 0

    average = earned / weight_completed
    average_percent = average * 100
    return average_percent


def get_remaining_weight(assessments):
    """
    Return the remaining weight (weight of assessments that haven't been completed -
    grade is None).
    """
    completed_weight = 0

    for assessment in assessments:
        if assessment.grade is not None:
            completed_weight += assessment.weight

    remaining_weight = 100 - completed_weight
    return remaining_weight


def calc_worst_case_final_mark(assessments):
    """
    Return worst possible final mark from given assessments.
    """
    earned = 0

    for assessment in assessments:
        if assessment.grade is None:
            continue
        earned += assessment.weight * (assessment.grade / 100)

    worst_average_percent = earned
    return worst_average_percent


def calc_best_case_final_mark(assessments):
    """
    Return best possible final mark from given assessments.
    """
    earned = 0
    remaining_weight = get_remaining_weight(assessments)

    for assessment in assessments:
        if assessment.grade is None:
            continue
        earned += assessment.weight * (assessment.grade / 100)

    best_case_average_percent = earned + remaining_weight
    return best_case_average_percent


def get_count_of_incomplete_assessments(assessments):
    """
    Return the count of assessments that haven't been completed
    (grade is None).
    """
    count = 0
    for assessment in assessments:
        if assessment.grade is None:
            count += 1
    return count


def calc_required_remaining_average(
        assessments, aspired_final_mark
):
    """
    Return the average for remaining incomplete assessments that will
    achieve the aspired final mark average.
    """
    earned = 0
    remaining_weight = get_remaining_weight(assessments)
    for assessment in assessments:
        if assessment.grade is None:
            continue
        earned += assessment.weight * (assessment.grade / 100)

    if remaining_weight == 0:
        return 0

    necessary_average = (aspired_final_mark - earned) / remaining_weight
    necessary_average_percent = necessary_average * 100
    return necessary_average_percent