import factory.django

from ads.models import Category, Ad
from user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    birth_date = "2000-10-10"



class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("ean", length=8)



class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = factory.Faker("name")
    price = 1000
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
