from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_roundtrip():
    h = hash_password("hunter22")
    assert h.startswith("pbkdf2$")
    assert verify_password("hunter22", h)
    assert not verify_password("hunter23", h)


def test_hashes_are_salted():
    assert hash_password("same") != hash_password("same")


def test_malformed_hash_is_rejected():
    assert not verify_password("x", "not-a-hash")


def test_token_roundtrip():
    assert decode_access_token(create_access_token("42")) == "42"
    assert decode_access_token("bad.token.value") is None
