import graphene as g
from graphene_django.types import DjangoObjectType, ObjectType
from app.movies.models import Actor, Movie


# Create a GraphQL type for the actor model
class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


# Create a GraphQL type for the movie model
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


# Create a Query type
class Query(ObjectType):
    actor = g.Field(ActorType, id=g.Int())
    movie = g.Field(MovieType, id=g.Int())
    actors = g.List(ActorType)
    movies = g.List(MovieType)

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk=id)
        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk=id)
        return None

    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()


# Create Input Object Types
class ActorInput(g.InputObjectType):
    id = g.ID()
    name = g.String()

class MovieInput(g.InputObjectType):
    id = g.ID()
    title = g.String()
    actors = g.List(ActorInput)
    year = g.Int()

# Create mutations for actors
class CreateActor(g.Mutation):
    class Arguments:
        input = ActorInput(required=True)

    ok = g.Boolean()
    actor = g.Field(ActorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = Actor(name=input.name)
        actor_instance.save()
        return CreateActor(ok=ok, actor=actor_instance)


class UpdateActor(g.Mutation):
    class Arguments:
        id = g.Int(required=True)
        input = ActorInput(required=True)

    ok = g.Boolean()
    actor = g.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        actor_instance = Actor.objects.get(pk=id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok=ok, actor=actor_instance)
        return UpdateActor(ok=ok, actor=None)


# Create mutations for movies
class CreateMovie(g.Mutation):
    class Arguments:
        input = MovieInput(required=True)

    ok = g.Boolean()
    movie = g.Field(MovieType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actors = []
        for actor_input in input.actors:
          actor = Actor.objects.get(pk=actor_input.id)
          if actor is None:
            return CreateMovie(ok=False, movie=None)
          actors.append(actor)
        movie_instance = Movie(
          title=input.title,
          year=input.year
          )
        movie_instance.save()
        movie_instance.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie_instance)


class UpdateMovie(g.Mutation):
    class Arguments:
        id = g.Int(required=True)
        input = MovieInput(required=True)

    ok = g.Boolean()
    movie = g.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        movie_instance = Movie.objects.get(pk=id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
              actor = Actor.objects.get(pk=actor_input.id)
              if actor is None:
                return UpdateMovie(ok=False, movie=None)
              actors.append(actor)
            movie_instance.title = input.title
            movie_instance.year = input.yearce.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok=ok, movie=movie_instance)
        return UpdateMovie(ok=ok, movie=None)

class Mutation(g.ObjectType):
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()

schema = g.Schema(query=Query, mutation=Mutation)
