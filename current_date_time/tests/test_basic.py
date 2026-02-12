import re

from current_date_time import server as srv


def test_get_today_date_format():
    result = srv.get_today_date()
    # Should return YYYY-MM-DD format
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    assert date_pattern.match(result)


def test_get_today_date_with_timezone():
    result = srv.get_today_date(timezone="UTC")
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    assert date_pattern.match(result)


def test_get_today_date_invalid_timezone():
    result = srv.get_today_date(timezone="Invalid/Timezone")
    assert "Error" in result
    assert "Invalid timezone" in result


def test_get_current_time_format():
    result = srv.get_current_time()
    # Should contain time and timezone
    assert ":" in result
    assert "(" in result and ")" in result


def test_get_current_time_with_timezone():
    result = srv.get_current_time(timezone="UTC")
    assert "UTC" in result
    assert ":" in result
