from app import auth
from jose import jwt
from app.config import settings


def test_hash_and_verify_password():
    pwd = "SomeStrongPass!"
    hashed = auth.hash_password(pwd)
    assert hashed != pwd  # hashed should not equal plain
    assert auth.verify_password(pwd, hashed) is True
    assert auth.verify_password("wrong", hashed) is False

def test_create_token_contains_sub_and_exp():
    payload = {"sub": "unit@example.com"}
    token = auth.create_token(payload)
    # Decode with same SECRET_KEY to inspect claims
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == "unit@example.com"
    assert "exp" in decoded