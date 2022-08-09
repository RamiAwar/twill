from app.model.user import User, UserDB, UserSession
from app.service.deps import auth, unauthorized_error
from fastapi import Depends, HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def get_user(email: str):

    return UserDB(
        email="rami.awar.ra@gmail.com", name="Rami Awar", twitter_handle="@iamramiawar"
    )


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False

    # if not verify_password(password, user.hashed_password):
    #     return False

    if not fake_hash_password(password) == user.hashed_password:
        return False

    return user


async def get_current_user(session: UserSession = Depends(auth)):
    user = get_user(fake_users_db, username=session.username)
    if user is None:
        raise unauthorized_error

    return user


async def get_current_user(session: UserSession = Depends(auth)):
    user = get_user(session.email)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
