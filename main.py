from fastapi import FastAPI
from graphene import Schema
from starlette_graphene3 import GraphQLApp, make_playground_handler

from db.database import prepare_db, Session
from db.models import Employer, Job
from gql.queries import Query
from gql.mutations import Mutation


schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    prepare_db()


@app.get("/employers")
def get_employers():
    with Session() as session:
        return session.query(Employer).all()


@app.get("/jobs")
def get_employers():
    with Session() as session:
        return session.query(Job).all()


app.mount("/", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))
