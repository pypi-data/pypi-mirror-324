import time
import typing

import jwt


def get_user_id_from_payload(payload: typing.Dict) -> typing.Text | None:
    return payload.get("sub")


def raise_if_payload_expired(payload: typing.Dict) -> None:
    exp = payload.get("exp")
    if exp is None:
        raise jwt.InvalidTokenError("Expiration time is missing")
    if time.time() > exp:
        raise jwt.ExpiredSignatureError


def create_jwt_token(
    user_id: typing.Text,
    expires_in: int = 3600,
    *,
    jwt_secret: typing.Text,
    jwt_algorithm: typing.Text,
    now: typing.Optional[int] = None,
) -> typing.Text:
    """Sign JWT, payload contains sub=user_id, exp=expiration time, iat=issued time"""

    now = now or int(time.time())
    payload = {
        "sub": user_id,
        "iat": now,
        "exp": now + expires_in,
    }
    token = jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)
    return token


def verify_jwt_token(
    token: typing.Text, *, jwt_secret: typing.Text, jwt_algorithm: typing.Text
) -> typing.Dict:
    """Verify JWT, return payload dict if success, raise jwt exceptions if failed"""

    payload = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
    return payload
