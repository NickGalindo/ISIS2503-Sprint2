from typing import Dict, Any
from django.core.exceptions import ValidationError

import jwt
from datetime import datetime, timedelta

from authentication import ACCESS_SECRET, REFRESH_SECRET, redisConnectionPool

from . import cache

def createAccessToken(data: Dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire: datetime = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_SECRET, algorithm="HS256")
    return encoded_jwt

def createRefreshToken(data: Dict, expires_delta: timedelta = timedelta(weeks=2)):
    to_encode = data.copy()
    expire: datetime = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET, algorithm="HS256")
    return encoded_jwt

def decodeJwtToken(token: str) -> Dict[str, Any]:
    try:
        decoded_token = jwt.decode(token, ACCESS_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValidationError("JWT not valid")
    except jwt.InvalidTokenError:
        raise ValidationError("JWT not valid")

    return decoded_token


def decodeRefreshToken(refresh_token: str) -> Dict:
    try:
        decoded_token = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValidationError("JWT not valid")
    except jwt.InvalidTokenError:
        raise ValidationError("JWT not valid")

    return decoded_token

def refreshAccessToken(token: str):
    if cache.checkJwtBlacklist(token):
        raise ValidationError("JWT not valid")

    data: Dict = decodeRefreshToken(token)

    if not cache.addJwtBlacklist(token, timedelta(weeks=2)):
        raise ValidationError("JWT not valid")

    refresh_token = createRefreshToken(data=data)
    data["sub"] = data["cedula"]
    access_token = createAccessToken(data=data)

    return {"access_token": {"token": access_token, "token_type": "bearer"}, "refresh_token": {"token": refresh_token, "token_type": "bearer"}}
