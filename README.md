# Capstone

Capstone is final project  fullstack backend course provide by  Udicity, 

## this  project covering the following Lessons:
```json5
1- Coding in Python 3
2- Relational Database Architecture
3- Modeling Data Objects with SQLAlchemy
4- Internet Protocols and Communication
5- Developing a Flask API
6- Authentication and Access
7- Authentication with Auth0
8- Authentication in Flask
9- Role-Based Access Control (RBAC)
10- Testing Flask Applications
11- Deploying Applications
``` 

## Hosted on heroku.

```json5
Link](https://movieagencies.herokuapp.com).
```

## Dependencies

All dependencies are listed in the `requirements.txt` file. 
They can be installed by running `pip3 install -r requirements.txt`.

## Authentication

The API has three users :

1-  Assistant

```json5
--Credentials:
Email: assistent@agency19.com
Password: Password!19
```

```json5
-- Roles:
a- Get actors
b- Get movies
```

2. Director

```json5
--Credentials:
Email: director@agency19.com
Password: Password!19
```

```json5
-- Roles:
a- Get actors
b- Get movies
c- add actor
d- edit actor
e- edit movie
f- delete actor
```


3. Producer

```json5
--Credentials:
Email: producaer@agency19.com
Password: Password!19
```

--```json5
-- Roles:
a- Get actors
b- Get movies
c- add actor
d- add movie
e- edit actor
f- edit movie
g- delete actor
h- delete movie
```


The Auth0 domain and api audience can be found in `setup.sh`.

## Endpoints

### `GET /movies`

Gets all movies 



```json5

"movies": [
        {
            "genres": "Romance,Drama",
            "id": 1,
            "title": "Titanic",
            "year": "1998"
        },
        {
            "genres": "Action,Comedy",
            "id": 2,
            "title": "Bad Boys 4",
            "year": "2019"
        }
    ],
    "success": true
}
```

### `POST /movies`

Adds a new movie 



```json5
{
    "message": "added Successfully",
    "movie": {
        "genres": "Action,Comedy",
        "id": 1,
        "title": "Bad Boys 4",
        "year": "2019"
    },
    "success": true
}
```



### `PATCH /movies/<int:id>`

Edit data on a movie in the db.


```json5
{
    "message": "Updated Successfully",
    "movie": {
        "genres": "Romance",
        "id": 1,
        "title": "Titanic",
        "year": "1999"
    },
    "success": true
}
```

### `DELETE /movies/<int:id>`

Delete a movie 



```json5
{
    "message": "Deleted Successfully",
    "movie": "Titanic",
    "success": true
}
```

### `GET /actors`

Gets all actors 



```json5
{
    "actors": [
        {
            "Roles": "all acted movies here",
            "age": 83,
            "gender": "Male",
            "id": 1,
            "name": "Morgan Freeman"
        },
        {
            "Roles": "all acted movies here",
            "age": 51,
            "gender": "Male",
            "id": 2,
            "name": "Leonrdo De Capreo"
        },
        {
            "Roles": "all acted movies here",
            "age": 30,
            "gender": "Female",
            "id": 3,
            "name": "Emma Watson"
        }
    ],
    "success": true
}```

### `POST /actors`

Adds a new actor 


```json5
{
    "actors": {
        "age": 30,
        "gender": "Female",
        "id": 1,
        "name": "Emma Watson"
    },
    "message": "added Successfully",
    "success": true
}
```




### `PATCH /actors/<int:id>`

Edit actor


```json5
{
    "actor": {
        "age": 73,
        "gender": "Male",
        "id": 1,
        "name": "Robert De Niro"
    },
    "message": "Updated Successfully",
    "success": true
}
```

### `DELETE /actors/<int:id>`

Delete a actor 

Response:

```json5
{
    "actor": "Robert De Niro",
    "message": "Deleted Successfully",
    "success": true
}
```

## Tests using unitests

To run the tests, run `python3 tests.py`.

## Test using Postman 

There are two Files :

1- the First one is "Capstone.postman_collection" which you can use it to 

test all Api end points.

PS: Update the Tokens for the folders before start the test

2- The Second file  is "Postman_Test_result" which contain the result of runner test.