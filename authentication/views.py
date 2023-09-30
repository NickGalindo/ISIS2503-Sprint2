from typing import Any
from django.http import JsonResponse
import json

from . import user, jwt

# Create your views here.
def login(request: Any):
    body_unicode = request.body.decode("utf-8")
    body_data = json.loads(body_unicode)

    usr, flag = user.authenticate_user(body_data["username"], body_data["password"])

    if flag:
        data = {"user_id": usr["user_id"], "email": usr["email"]}
        refresh_token = jwt.createRefreshToken(data=data)
        data["sub"] = data["cedula"]
        access_token = jwt.createAccessToken(data=data)
        return JsonResponse({"access_token": {"token": access_token, "token_type": "bearer"}, "refresh_token": {"token": refresh_token, "token_type": "bearer"}})

    return JsonResponse({"ERROR": f"Wrong password. You have {3-usr} attempts left"})
