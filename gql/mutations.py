from graphene import ObjectType

from gql.job_mutations.mutations import AddJob, UpdateJob, DeleteJob
from gql.employer_mutations.mutations import AddEmployer, UpdateEmployer, DeleteEmployer
from gql.user_mutations.mutations import UserLogin, AddUser


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    user_login = UserLogin.Field()
    add_user = AddUser.Field()
