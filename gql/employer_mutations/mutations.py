from graphene import Mutation, Int, String, Field, Boolean

from gql.types import EmployerObject
from db.models import Employer
from db.database import Session


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(parent, info, name, contact_email, industry):
        emp = Employer(name=name, contact_email=contact_email, industry=industry)
        with Session() as session:
            session.add(emp)
            session.commit()
            session.refresh(emp)
        return AddEmployer(employer=emp)


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(parent, info, id, name=None, contact_email=None, industry=None):
        session = Session()

        emp = session.query(Employer).filter(Employer.id == id).first()

        if not emp:
            raise Exception(f"No Employer found with id={id}")

        if name is not None:
            emp.name = name

        if contact_email is not None:
            emp.contact_email = contact_email

        if industry is not None:
            emp.industry = industry

        session.commit()
        session.refresh(emp)

        return UpdateEmployer(employer=emp)


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(parent, info, id):
        session = Session()
        job = session.query(Employer).filter(Employer.id == id).first()

        if not job:
            raise Exception(f"No Employer found with id={id}")

        session.delete(job)
        session.commit()
        session.close()

        return DeleteEmployer(success=True)
