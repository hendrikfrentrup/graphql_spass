import graphene
from graphene_django import DjangoObjectType

from .models import Link, Vote
from users.schema import UserType
from graphql import GraphQLError
from django.db.models import Q

# this creates a linktype, gluing to the Link ORM
class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(LinkType, 
                          search=graphene.String(),
                          first=graphene.Int(),
                          skip=graphene.Int()
                          )
    votes = graphene.List(VoteType)

    # by convention resolvers are resolve_<object>
    def resolve_links(self, info, search=None, first=None, skip=None, **kwargs):
        
        link_list=Link.objects.all()
        
        # The value sent with the search parameter will be on the args variable
        if search:
            filter = (
                Q(url__icontains=search) | 
                Q(description__icontains=search)
            )
            link_list=link_list.filter(filter)

        if skip:
            link_list = link_list[skip::]

        if first:
            link_list = link_list[:first]

        print("-found links: ", len(link_list))
        return link_list

    def resolve_votes(self, info, **kwargs):
        vote_list=Vote.objects.all()
        print("-found votes: ", len(vote_list))
        return vote_list 

class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    # defines expected data received from client, i.e. expected in POST request's payload
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        user = info.context.user or None

        # create link in mapped ORM and save link to db
        link = Link(url=url, 
                    description=description,
                    posted_by=user)
        print("-saving link: ", link.id, link.url, link.description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        # obtain active user from context (via JWT)
        user = info.context.user
        if user.is_anonymous:
            # raise Exception('You must be logged to vote!')
            raise GraphQLError('You must be logged to vote!')

        # obtain target link_id from payload
        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)

class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()
    print("==Mutations instantiated==")
