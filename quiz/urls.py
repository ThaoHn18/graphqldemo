from graphene_django.views import GraphQLView
import graphql
from quiz.schema import schema
from django.urls import path

urlpatterns = [
    path('thao', GraphQLView.as_view(graphiql=True, schema=schema))
]
