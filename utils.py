import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from argon2.exceptions import VerifyMismatchError
from graphql import GraphQLError
from argon2 import PasswordHasher
from dotenv import load_dotenv

from db.database import Session
from db.models import User


load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRATION_TIME = int(os.getenv("TOKEN_EXPIRATION_TIME"))
SECRET_KEY = os.getenv("SECRET_KEY")


def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME)

    payload = {
        "sub": email,
        "exp": expiration_time
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password):
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(password_hash, password):
    ph = PasswordHasher()
    try:
        ph.verify(password_hash, password)
    except VerifyMismatchError:
        raise GraphQLError("Invalid password")


def get_authenticated_user(context):
    req_object = context.get('request', {})
    auth_header = req_object.headers.get('Authorization')

    if auth_header:
        token = auth_header.replace('Bearer ', '')

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if datetime.now(tz=timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError('Token has expired')

            session = Session()
            user = session.query(User).filter(User.email == payload.get('sub')).first()

            if not user:
                raise GraphQLError('Could not authenticate user')

            return user
        except jwt.exceptions.InvalidSignatureError:
            raise GraphQLError('Invalid authentication token')
    else:
        raise GraphQLError('Missing authentication token')


def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)

        if user.role != "admin":
            raise GraphQLError("Not authorized action")

        return func(*args, **kwargs)

    return wrapper
