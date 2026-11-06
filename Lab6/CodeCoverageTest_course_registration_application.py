import pytest

from course_registration import (
    can_register,
    waitlist_position,
    late_fee,
)


# can_register() branch tests


def test_unknown_status():
    with pytest.raises(ValueError):
        can_register("unknown", 10, 3, True)


def test_valid_status():
    assert can_register("regular", 10, 3, True) == "registered"


def test_invalid_course_credits():
    with pytest.raises(ValueError):
        can_register("regular", 10, 0, True)


def test_valid_course_credits():
    assert can_register("regular", 10, 3, True) == "registered"


def test_prerequisites_false():
    assert can_register("regular", 10, 3, False) == "prerequisites missing"


def test_prerequisites_true():
    assert can_register("regular", 10, 3, True) == "registered"


def test_credit_limit_exceeded():
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


def test_credit_limit_not_exceeded():
    assert can_register("regular", 10, 3, True) == "registered"


# waitlist_position() branch tests


def test_invalid_capacity():
    with pytest.raises(ValueError):
        waitlist_position(10, 0, 2)


def test_valid_capacity():
    assert waitlist_position(10, 20, 2) == 0


def test_seat_available():
    assert waitlist_position(10, 20, 0) == 0


def test_seat_unavailable():
    assert waitlist_position(20, 20, 2) == 3


def test_waitlist_full():
    assert waitlist_position(20, 20, 10) == -1


def test_waitlist_not_full():
    assert waitlist_position(20, 20, 3) == 4


# late_fee() branch tests


def test_not_late():
    assert late_fee(0, 15, False) == 0


def test_late_payment():
    assert late_fee(5, 15, False) == 500


def test_waiver_applied():
    assert late_fee(5, 15, True) == 0


def test_no_waiver():
    assert late_fee(5, 15, False) == 500


def test_within_seven_days():
    assert late_fee(7, 15, False) == 500


def test_after_seven_days():
    assert late_fee(10, 15, False) == 800


def test_high_credit_surcharge():
    assert late_fee(5, 21, False) == 750


def test_no_high_credit_surcharge():
    assert late_fee(5, 15, False) == 500


def test_fee_cap_reached():
    assert late_fee(30, 25, False) == 2000


def test_fee_cap_not_reached():
    assert late_fee(5, 15, False) == 500
