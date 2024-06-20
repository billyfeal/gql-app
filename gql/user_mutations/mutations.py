from graphene import Mutation, Int, String, Field, Boolean
from graphql import GraphQLError

from gql.types import UserObject
from db.models import User
from db.database import Session
from utils import generate_token, verify_password, hash_password, get_authenticated_user, admin_user


class UserLogin(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(parent, info, email, password):
        session = Session()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError(f"No user found with the email {email}")

        verify_password(user.password_hash, password)

        token = generate_token(email)

        return UserLogin(token=token)


class AddUser(Mutation):
    class Arguments:
        name = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @staticmethod
    @admin_user
    def mutate(parent, info, name, email, password, role):
        if role == 'admin':
            auth_user = get_authenticated_user(info.context)
            if auth_user.role != 'admin':
                raise GraphQLError('Just admin users can add new admins')

        session = Session()
        user = session.query(User).filter(User.email == email).first()
        if user:
            raise GraphQLError("There is a user registered with the provided email")

        user = User(
            name=name,
            username=email,
            email=email,
            password_hash=hash_password(password),
            role=role
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return AddUser(user=user)
