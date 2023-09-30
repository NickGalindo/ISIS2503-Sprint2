from typing import Any, Dict

from datetime import datetime, timedelta
from colorama import Fore

import redis
import json

from decimal import Decimal

from authentication import redisConnectionPool

class MultiEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                "__type": "datetime",
                "value": obj.isoformat()
            }
        if isinstance(obj, Decimal):
            return float(obj)
        return super(MultiEncoder, self).default(obj)

class MultiDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "__type" not in obj:
            return obj

        if obj["__type"] == "datetime":
            return datetime.fromisoformat(obj["value"])

        return obj
        
def getUserSession(user_id: str):
    __redis = redis.Redis(connection_pool=redisConnectionPool)

    try:
        val = __redis.get(user_id)
    except Exception as e:
        print(Fore.RED + f"ERROR: Failed to get user session from cache")
        print(e)
        return None

    if val is None:
        return None

    if not isinstance(val, str):
        print(Fore.RED + f"ERROR: Error validating user session")
        print(val)
        return None

    loaded_val = json.loads(val, cls=MultiDecoder)
    if not isinstance(loaded_val, Dict):
        print(Fore.RED + f"ERROR: Error validating user session")
        print(loaded_val)
        return None

    return loaded_val

def setUserSession(user_id: str, value: Any):
    __redis = redis.Redis(connection_pool=redisConnectionPool)

    __serialized_value = json.dumps(value, cls=MultiEncoder)
    try:
        __redis.set(user_id, __serialized_value)
    except Exception as e:
        print(Fore.RED + f"Error while saving into redis:\n{e}")
        return False

    return True

def checkJwtBlacklist(token: str):
    __redis = redis.Redis(connection_pool=redisConnectionPool)

    try:
        if __redis.get(token) is not None:
            return True
    except Exception as e:
        print(Fore.RED + f"ERROR: Failed to check jwt blacklist falling back to default blacklisted")
        print(e)
        return True

    return False

def addJwtBlacklist(token: str, exp: timedelta):
    __redis = redis.Redis(connection_pool=redisConnectionPool)

    try:
        __redis.setex(token, exp, 1)
    except Exception as e:
        print(Fore.RED + f"ERROR: Couldn't blacklist jwt token")
        print(e)
        return False

    return True
