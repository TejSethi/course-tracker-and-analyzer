import utils
from models.db_models import Assessment

mocked_assessment = [
    Assessment(
        id=1,
        course_id=1,
        name="A1",
        grade=80.0,
        weight=10,
        type="Assignment"
    ),
    Assessment(
        id=2,
        course_id=1,
        name="Midterm 1",
        grade=75.0,
        weight=20,
        type="Test"
    ),
    Assessment(
        id=3,
        course_id=1,
        name="Midterm 2",
        grade=None,
        weight=20,
        type="Test"
    ),
]

def test_calc_assessments_average__non_empty_list():
    """
    Test calc_assessments_average correctly calculates the average
    for a list of assessments (with and with no grades).
    """
    # Test
    actual = utils.calc_assessments_average(assessments=mocked_assessment)

    # Verify
    expected = 23 / 30 * 100 # earned / total completed weight multiply by 100 to convert to percentage
    assert actual == expected

def test_calc_assessments_average__empty_list():
    """
       Test calc_assessments_average correctly calculates the average
       for a list of assessments (with and with no grades).
       """

    # Test
    actual = utils.calc_assessments_average(assessments=[])

    # Verify
    expected = 0
    assert actual == expected


def test_get_remaining_weight():
    """
    Test get_remaining_weight correctly sums the weights of incomplete assessments.
    """

    # Test
    actual = utils.get_remaining_weight(assessments=mocked_assessment)

    # Verify
    expected = 70
    assert actual == expected

def test_worst_case_final_mark():
    """
    Test worst_case_final_mark correctly computes the worst mark possible
    from the given mocked assessments.
    """
    # Test
    actual = utils.calc_worst_case_final_mark(assessments=mocked_assessment)

    # Verify
    expected = 23
    assert actual == expected


def test_best_case_final_mark():
    """
    Test best_case_final_mark correctly computes the best mark possible
    from the given mocked assessments.
    """
    # Test
    actual = utils.calc_best_case_final_mark(assessments=mocked_assessment)

    # Verify
    expected = 93
    assert actual == expected


def test_calc_required_remaining_average__non_empty_list():
    """
    Test calc_required_remaining_average with a non empty list of
    assessments (including incomplete assessment).
    """
    # Test
    actual = utils.calc_required_remaining_average(
        assessments=mocked_assessment, aspired_final_mark= 80)
    # Verify
    need_to_earn = 57  # 80 - the 23 earned
    remaining_weight = 70
    expected = need_to_earn / remaining_weight * 100
    assert actual == expected

def test_calc_required_remaining_average__empty_list():
    """
    Test calc_required_remaining_average with an empty list of
    assessments (including incomplete assessment).
    """
    # Test
    actual = utils.calc_required_remaining_average(
        assessments=[], aspired_final_mark=80)
    # Verify
    expected = 80
    assert actual == expected


def test_calc_required_remaining_average__no_remaining_weight():
    """
    Test calc_required_remaining_average with a list of
    assessments (all completed and weights add to 100).
    """
    completed_assessments = [
        Assessment(
            id=1,
            course_id=1,
            name="A1",
            grade=80.0,
            weight=10,
            type="Assignment"
        ),
        Assessment(
            id=2,
            course_id=1,
            name="Midterm 1",
            grade=75.0,
            weight=20,
            type="Test"
        ),
        Assessment(
            id=3,
            course_id=1,
            name="Final Exam",
            grade=90,
            weight=70,
            type="Exam"
        ),
    ]

    # Test
    actual = utils.calc_required_remaining_average(
        assessments=completed_assessments, aspired_final_mark=80)
    # Verify
    expected = 0  # 0 because all assessments have been completed and weights add to 100
    assert actual == expected
