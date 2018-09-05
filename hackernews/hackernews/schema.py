import graphene
import graphql_jwt
import links.schema
import users.schema
import ingredients.schema

# should log lots of things
import logging
logger = logging.getLogger(__name__)

from graphene_django.debug import DjangoDebug

class Query(users.schema.Query, 
            links.schema.Query,
            ingredients.schema.Query,
            graphene.ObjectType):
    # TODO: the logging doesn't seem to work at the moment

    debug = graphene.Field(DjangoDebug, name='__debug')

    logger.debug("Query executed. gg")
    print("="*28)
    print("graphene version: ", graphene.get_version())
    print("="*28)
    print("Query executed. p")
    pass


class Mutation(users.schema.Mutation,
               links.schema.Mutation, 
               graphene.ObjectType):
    print("Mutation executed. p")
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
