import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        link_list=Link.objects.all()
        print("-found links: ", len(link_list))
        return link_list


class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        print("-saving link: ", link.id, link.url, link.description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )



class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    print("-mutation happening: ", create_link)
