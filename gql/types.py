from graphene import String, ObjectType, Int, List, Field
from db.database import Session
from db.models import Employer, Job


class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(parent, info):
        return parent.jobs


class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(parent, info):
        return parent.employer

    @staticmethod
    def resolve_application(parent, info):
        return parent.applications


class UserObject(ObjectType):
    id = Int()
    name = String()
    username = String()
    email = String()
    role = String()
    applications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_application(parent, info):
        return parent.applications


class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(parent, info):
        return parent.user

    @staticmethod
    def resolve_job(parent, info):
        return parent.job



