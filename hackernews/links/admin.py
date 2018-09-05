from django.contrib import admin
from django.contrib.auth.models import User
from links.models import Link, Vote
from ingredients.models import Category, Ingredient

# admin.site.register(User)
admin.site.register(Link)
admin.site.register(Vote)
admin.site.register(Category)
admin.site.register(Ingredient)