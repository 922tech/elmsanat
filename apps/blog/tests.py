"""Generating fake data for the database"""

from faker import Faker
from .models.models import Post, Category
from django.contrib.auth import get_user_model
from django.db import models 
from typing import  Any, Callable

user_model = get_user_model()

faker = Faker('en_US')


class FakeModelFactory:
    """
    The tool to create fake data.

    params: modle: table in which the data will be persisted

    params: fake_field_creator: the function which returns
            a dictionary containing fields and faker implementations
    
    """
    def __init__(
            self,
            model: models.base.ModelBase, 
            fake_field_creator:  Callable[[],dict[str, Any]]
            ):
        self.model = model
        self.fake_field_creator = fake_field_creator 

    def create_fake_record(self, how_many: int):
        objs = (self.model(**self.fake_field_creator()) for _ in range(how_many))
        self.model.objects.bulk_create(objs)
        

# specify how many of records of each model you want 
FAKE_OBJECTS_QUANTITY = {
    'user':1000,
    'category':20,
    'post':1000,
}

def user_fake_field_creator() -> dict[str, Any]:
    return {
    'title':faker.unique.name(),
    'category_id':faker.pyint(
        min_value=1, 
        max_value=FAKE_OBJECTS_QUANTITY['category']
    ),
    'thumbnail':faker.url(),
    'writer':faker.name(),
    'content':faker.text(faker.pyint(min_value=5000, max_value=20000)),
    }

def post_fake_field_creator():
    return {
    'title':faker.name(),
    'category_id':faker.pyint(min_value=1, max_value=20),
    'thumbnail':faker.url(),
    'writer':faker.name(),
    'content':faker.text(faker.pyint(min_value=5000, max_value=20000)),
    }

def category_fake_field_creator(): 
    return {
    'title':faker.unique.name()
    }


fake_category_factory = FakeModelFactory(Category,category_fake_field_creator)
fake_post_factory = FakeModelFactory(Post, post_fake_field_creator)

fake_category_factory.create_fake_record(FAKE_OBJECTS_QUANTITY['category'])
fake_post_factory.create_fake_record(FAKE_OBJECTS_QUANTITY['post'])


# users = baker.make(user_model, _quantity=1000)
# categories = baker.make(Category, _quantity=20)
# posts = baker.make(Post, _quantity=10000, _bulk_create=True)
# comments = baker.make(Comment)

