import pytest

from gsenha import PasswordManager


def test_key_load_error():
    with pytest.raises(Exception) as excinfo:
        PasswordManager(key='')
    assert "key load error" in str(excinfo.value)

