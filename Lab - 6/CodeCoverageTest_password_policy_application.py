import pytest
from password_policy import check_password, strength, suggest_fix


# ---- starter tests ----
def test_valid_password_has_no_issues():
    assert check_password("Abcdef1!") == []


def test_valid_password_is_good():
    assert strength("Abcdef1!") == "good"


# ---- check_password ----
def test_too_short():
    assert check_password("abc") == ["too short", "no uppercase", "no digit", "no special"]


def test_too_long():
    assert check_password("A" * 65) == ["too long", "no lowercase", "no digit", "no special"]


def test_common_password():
    assert check_password("password") == ["common", "no uppercase", "no digit", "no special"]


def test_no_uppercase():
    assert check_password("abcdefg1!") == ["no uppercase"]


def test_no_lowercase():
    assert check_password("ABCD1234!") == ["no lowercase"]


def test_no_digit():
    assert check_password("Abcdefgh!") == ["no digit"]


def test_no_special():
    assert check_password("Abcdefg1") == ["no special"]


# ---- strength ----
def test_strength_strong():
    assert strength("Abcdefghijk12!") == "strong"


def test_strength_weak():
    assert strength("Abcdefg1") == "weak"


def test_strength_very_weak():
    assert strength("abc") == "very weak"


# ---- suggest_fix ----
def test_fix_none_needed():
    assert suggest_fix([]) == "none needed"


def test_fix_too_short():
    assert suggest_fix(["too short"]) == "add more characters"


def test_fix_common():
    assert suggest_fix(["common"]) == "avoid common passwords"


def test_fix_missing_type():
    assert suggest_fix(["no digit"]) == "add digit"


def test_fix_too_long():
    assert suggest_fix(["too long"]) == "shorten it"