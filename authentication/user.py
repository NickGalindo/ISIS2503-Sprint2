from django.core.exceptions import ValidationError
from passlib.context import CryptContext
from . import dbmanager, cache

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def __verifyPassword(password, hashed_password):
    return PWD_CONTEXT.verify(password, hashed_password)

def __getPasswordHash(password):
    return PWD_CONTEXT.hash(password)

def __getUser(username: str):
    q = f"SELECT auth.user.user_id, auth.user.email, auth.user.password_hashed, auth.user.password_salt, auth.user.state FROM auth.user WHERE auth.user.email == {username};"

    usr = dbmanager.dbQuery(q)

    if len(usr) == 0:
        raise ValidationError("User doesn't exist")

    return {"user_id": usr[0][0], "email": usr[0][1], "password_hashed": usr[0][2], "password_salt": usr[0][3], "state": usr[0][4]}

def authenticate_user(username, password):
    usr = __getUser(username)

    if usr["state"] == "blocked":
        raise ValidationError("YOUR USER HAS BEEN BLOCKED. PLEASE CONTACT SUPPORT FOR FURTHER HELP")

    usr_session = cache.getUserSession(usr["user_id"])

    if usr_session is None:
        cache.setUserSession(usr["user_id"], {"attempts": 0})
        usr_session = {"attempts": 0}

    if __verifyPassword(password, usr["password_hashed"]):
        return usr, True

    usr_session["attempts"] += 1

    if usr_session["attempts"] == 3:
        upd = f"UPDATE auth.users SET auth.users.state = 'blocked' WHERE auth.users.user_id = {usr['user_id']};"
        dbmanager.dbUpdate(upd)
        cache.setUserSession(usr["user_id"], usr_session)

        raise ValidationError("YOUR USER HAS BEEN BLOCKED. PLEASE CONTACT SUPPORT FOR FURTHER HELP")

    cache.setUserSession(usr["user_id"], usr_session)

    return usr_session["attempts"], False
