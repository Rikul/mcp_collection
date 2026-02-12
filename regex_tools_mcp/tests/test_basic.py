from regex_tools_mcp import server as srv


def test_regex_validate_valid_pattern():
    result = srv.regex_validate(r"\d+")
    assert result["ok"] is True


def test_regex_validate_invalid_pattern():
    result = srv.regex_validate(r"[invalid(")
    assert result["ok"] is False
    assert "error" in result


def test_regex_find_basic():
    result = srv.regex_find(r"\d+", "abc 123 def 456")
    assert result["count"] == 2
    assert result["matches"][0]["match"] == "123"
    assert result["matches"][1]["match"] == "456"


def test_regex_replace_basic():
    result = srv.regex_replace(r"\d+", "X", "abc 123 def 456")
    assert result["result"] == "abc X def X"
    assert result["replacements"] == 2


def test_regex_find_with_groups():
    result = srv.regex_find(r"(\w+)@(\w+)", "user@example")
    assert result["count"] == 1
    assert result["matches"][0]["groups"] == ["user", "example"]
