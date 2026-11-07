from hypothesis import given, strategies as st
from password_policy import first_character_type, split_credentials, digit_ratio


@given(st.text() | st.none())
def test_first_character_type_no_crash(s):
    try:
        result = first_character_type(s)
    except Exception as e:
        assert False, f"first_character_type crashed with: {type(e).__name__}: {e}"
    assert result in ("digit", "letter", "symbol", "invalid")


@given(st.text() | st.none())
def test_split_credentials_no_crash(s):
    try:
        result = split_credentials(s)
    except Exception as e:
        assert False, f"split_credentials crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, tuple) and len(result) == 2
    if isinstance(s, str) and ":" in s:
        user, password = result
        assert isinstance(user, str) and isinstance(password, str)
        assert user == user.strip()
        assert password == password.strip()
    else:
        assert result == (None, None)


@given(st.text() | st.none())
def test_digit_ratio_no_crash(s):
    try:
        result = digit_ratio(s)
    except Exception as e:
        assert False, f"digit_ratio crashed with: {type(e).__name__}: {e}"
    assert isinstance(result, float)
    assert 0.0 <= result <= 1.0