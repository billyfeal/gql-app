from graphene import Mutation, Int, String, Field, Boolean

from gql.types import JobObject
from db.models import Job
from db.database import Session


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(parent, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        with Session() as session:
            session.add(job)
            session.commit()
            session.refresh(job)
        return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(parent, info, id, title=None, description=None, employer_id=None):
        session = Session()

        job = session.query(Job).filter(Job.id == id).first()
        # job = session.query(Job).options(joinedload(Job.employer)).filter(Job.id == id).first()

        if not job:
            raise Exception(f"No Job found with job_id={id}")

        if title is not None:
            job.title = title

        if description is not None:
            job.description = description

        if employer_id is not None:
            job.employer_id = employer_id

        session.commit()
        session.refresh(job)

        return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(parent, info, id):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()

        if not job:
            raise Exception(f"No Job found with job_id={id}")

        session.delete(job)
        session.commit()
        session.close()

        return DeleteJob(success=True)
