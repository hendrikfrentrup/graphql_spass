import graphene
import links.schema

import logging
logger = logging.getLogger(__name__)

class Query(links.schema.Query, graphene.ObjectType):
    logger.debug("Query executed. gg")
    print("Query executed. p")
    pass

class Mutation(links.schema.Mutation, graphene.ObjectType):
    print("Mutation executed. p")
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
