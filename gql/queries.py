from graphene import ObjectType, List, Field, Int

from gql.types import EmployerObject, JobObject, UserObject, JobApplicationObject
from db.database import Session
from db.models import Employer, Job, User, JobApplication


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    applications = List(JobApplicationObject)

    @staticmethod
    def resolve_users(parent, info):
        return Session().query(User).all()

    @staticmethod
    def resolve_applications(parent, info):
        return Session().query(JobApplication).all()


    @staticmethod
    def resolve_jobs(parent, info):
        return Session().query(Job).all()

    @staticmethod
    def resolve_job(parent, info, id):
        return Session().query(Job).filter(Job.id == id).first()

    @staticmethod
    def resolve_employers(parent, info):
        return Session().query(Employer).all()

    @staticmethod
    def resolve_employer(parent, info, id):
        return Session().query(Employer).filter(Employer.id == id).first()
