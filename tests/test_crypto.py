import pytest

from bamboopass.crypto import derive_password


def test_derive_password_deterministic():
    p1 = derive_password(key="k", seed="s", iterations=200000, length=30)
    p2 = derive_password(key="k", seed="s", iterations=200000, length=30)
    assert p1 == p2
    assert len(p1) == 30


def test_derive_password_validation():
    with pytest.raises(ValueError):
        derive_password(key="", seed="s", iterations=200000, length=30)
    with pytest.raises(ValueError):
        derive_password(key="k", seed="", iterations=200000, length=30)
    with pytest.raises(ValueError):
        derive_password(key="k", seed="s", iterations=999, length=30)
    with pytest.raises(ValueError):
        derive_password(key="k", seed="s", iterations=200000, length=7)
