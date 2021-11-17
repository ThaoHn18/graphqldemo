# from _typeshed import Self
# from django.http import request
# from typing_extensions import Required
import graphene
from graphene_django import DjangoListField
from graphene_django import DjangoObjectType, fields
from .models import Category,Quizzes,Question,Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id','name')

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields =('id','title','category','quiz')

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ('title','quiz')

class AnserType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ('question','answer_text')


class Query(graphene.ObjectType):
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnserType, id=graphene.Int())

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)
    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)
# C
class CategoryMutation_add(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation_add(category=category)

#U
class CategoryMutation_update(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required = True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root, info,name,id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryMutation_update(category=category)

#D
class CategoryMutation_del(graphene.Mutation):
    class Arguments:
        id= graphene.ID()
        # name = graphene.String(required= True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return CategoryMutation_del(category=category)

class Mutation(graphene.ObjectType):
    # pass
    update_category = CategoryMutation_update.Field()
    add_category = CategoryMutation_add.Field()
    delete_category = CategoryMutation_del.Field()



schema = graphene.Schema(query=Query,mutation=Mutation)
