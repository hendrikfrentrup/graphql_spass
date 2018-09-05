import graphene
from graphene_django.types import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

# class CategoryNode(DjangoObjectType):
#     class Meta:
#         model = Category
#         filter_fields = ['name', 'ingredients']
#         interfaces = (graphene.relay.Node, )

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

# class IngredientNode(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#         # Allow for some more advanced filtering here
#         filter_fields = {
#             'name': ['exact', 'icontains', 'istartswith'],
#             'notes': ['exact', 'icontains'],
#             'category': ['exact'],
#             'category__name': ['exact'],
#         }
#         interfaces = (graphene.relay.Node, )


class Query(object):
    all_categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.Int(),name=graphene.String())
    all_ingredients = graphene.List(IngredientType)
    ingredient = graphene.Field(IngredientType, id=graphene.Int(),name=graphene.String())

    # category_node = graphene.relay.Node.Field(CategoryNode)
    # all_categories_node = DjangoFilterConnectionField(CategoryNode)
    # ingredient_node = graphene.relay.Node.Field(IngredientNode)
    # all_ingredients_node = DjangoFilterConnectionField(IngredientNode)

    def resolve_all_categories(self, info, **kwargs):
        category_list = Category.objects.all()
        return category_list

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        ingredient_list = Ingredient.objects.select_related('category').all()
        return ingredient_list

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None