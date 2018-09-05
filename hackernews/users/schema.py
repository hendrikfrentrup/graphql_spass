import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType, 
                          search=graphene.String(),
                          first=graphene.Int(),
                          skip=graphene.Int())

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            print("-loggin error")
            raise Exception('Not logged in!')
        print("-found active user")
        return user

    def resolve_users(self, info, search=None, first=None, skip=None, **kwargs):
        user_list=get_user_model().objects.all()
        
        if skip:
            user_list = user_list[skip::]

        if first:
            user_list = user_list[:first]

        print("-found users: ", len(user_list))
        return user_list


class CreateUser(graphene.Mutation):
    # instead of defining individual user fields, 
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        print("-saving user: ", user.id, user.username, user.email)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()