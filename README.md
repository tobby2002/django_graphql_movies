# app

This is a sample application to accompany my blog post on
 [Stack Abuse](https://stackabuse.com/building-a-graphql-api-with-django/). 
 This post introduces GraphQL, designs a schema for movies and details 
 how to create the GraphQL API with Graphene and Django.

Aside from the Django application, this repo also includes the following:

* **schema.graphql** - the complete GraphQL schema
* **queries.graphql** - an exmaple of every query and mutation defined in the schema
* **actorQuery.sh** - a sample cURL request to communicate with the API
* **movies.json** - test data

## Setting up

Clone this repo, and in the directory follow these steps:

```bash
# Create virtual environment
python3 -m venv env
# Activate virtual environment
. env/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run DB migration
python manage.py migrate
# Optional: load test data
python manage.py loaddata movies.json
# Run the application
python manage.py runserver
```

If you go to http://127.0.0.1:8000/graphql/, you'll be able to interact with the API there.

```bash
# query e.g.
query getQuery {
  actors {
    id
    name
    movieSet {
      id
    }
  }
  
}

# mutaion https://stackabuse.com/building-a-graphql-api-with-django/


# query 
query Qactors {
  actors {
    id
    name
    movieSet {
      id
    }
  }
}

# query $x
query Qactors_x($x:Int) {
  actor(id:$x) {
    id
    name
    movieSet {
      id
    }
  }
}

{
  "x": 2
}

# create $x
mutation McreateActor_x($x: ActorInput!) {
  createActor(input: $x) {
    ok
    actor {
      id
      name
    }
  }
}
{
  "x": {
    "name": "wooaaaasik"
  } 
}

# update $xy 
mutation MupdateActor_xy($x:Int!, $y: ActorInput!) {
  updateActor( id: $x, input: $y) {
    ok
    actor {
      id
      name
    }
  }
}

{  
  "x": 1,
  "y": {
   	"name": "good" 
  }
}

# create
mutation createActor {
  createActor(input: {
    name: "Tom Hanks"
  }) {
    ok
    actor {
      id
      name
    }
  }
}
```
