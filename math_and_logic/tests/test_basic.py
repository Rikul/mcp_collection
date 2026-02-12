from math_and_logic import server as srv


def test_add():
    assert srv.add(2, 3) == 5
    assert srv.add(-1, 1) == 0


def test_subtract():
    assert srv.subtract(5, 3) == 2
    assert srv.subtract(0, 5) == -5


def test_multiply():
    assert srv.multiply(3, 4) == 12
    assert srv.multiply(-2, 3) == -6


def test_divide():
    assert srv.divide(10, 2) == 5
    assert srv.divide(7, 2) == 3.5


def test_divide_by_zero():
    result = srv.divide(10, 0)
    assert "Division by zero" in result


def test_sqrt():
    assert srv.sqrt(9) == 3
    assert srv.sqrt(4) == 2


def test_sqrt_negative():
    result = srv.sqrt(-1)
    assert "negative number" in result


def test_greater_than():
    assert srv.greater_than(5, 3) is True
    assert srv.greater_than(3, 5) is False


def test_less_than():
    assert srv.less_than(3, 5) is True
    assert srv.less_than(5, 3) is False


def test_set_intercept():
    result = srv.set_intercept([1, 2, 3], [2, 3, 4])
    assert set(result) == {2, 3}


def test_set_union():
    result = srv.set_union([1, 2], [3, 4])
    assert set(result) == {1, 2, 3, 4}
