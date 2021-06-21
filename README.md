# Casting Agency Project
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation
We are creating a Casting Agency Company that creats and assign actors to movies. We are creating roles within the company to simplify the precess of creating movies and assigning actors to them.
This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.


### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment


### Running Locally

#### Installing Dependencies

##### Python 

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup

In terminal run:
```bash
source setup.sh
flask db init
flask db migrate
flask db upgrade 
```

or you could use the provided psql dump:

```bash
createdb capstone
psql capstone < capstone.psql
```

#### Running Tests
To run the tests, run
```bash
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone.psql
python test_app.py
```


#### Auth0 Setup

Tokens for each role are in setup.sh 


##### Roles

There are three roles in this API, which are:

* Casting Assistant
	* Can view actors and movies
* Casting Director
	* All permissions a Casting Assistant has and…
	* Add or delete an actor from the database
	* Modify actors or movies
* Executive Producer
	* All permissions a Casting Director has and…
	* Add or delete a movie from the database

##### Permissions

The full permissions are:

*    "add:actor",
*    "add:movie",
*    "delete:actor",
*    "delete:movie",
*    "get:actors",
*    "get:movies",
*    "update:actor",
*    "update:movie"

#### Launching The App

1. Initialize and activate a virtualenv

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = "postgres://{}/{}".format('localhost:5432', 'capstone')
    ```

4. Setup the environment variables for flask, and testing:
	```bash
	source setup.sh 
	```
5.  To run the server locally, execute:

    ```bash
    flask run
    ```

## API Documentation

### Models
There are two models:
* Movie
	* title
	* release_date
* Actor
	* name
	* age
	* gender


### Endpoints


#### GET /movies 
* Get all movies

* Require `get:movies` permission

* Responds with a 404 error if no movies are not found

* **Example Request:** `curl 'http://localhost:5000/movies'`

* **Expected Result:**
    ```json
	{
		"movies": [
			"id": 1,
			"title": "Yahşi Batı",
			"release_date": "Fri, 04 May 2012 00:00:00 GMT"
			},
			...
		],
		"success": true
    }
    ```
	
#### GET /actors 
* Get all actors

* Requires `view:actors` permission

* Responds with a 404 error if no actors are not found

* **Example Request:** `curl 'http://localhost:5000/actors'`

* **Expected Result:**
    ```json
	{
   	 "actors": [
        	{
            	"age": 1,
            	"gender": "M",
            	"id": 1,
            	"name": "Example_1"
       	 },
        	{
            	"age": 2,
            	"gender": "M",
            	"id": 2,
            	"name": "Example_2"
        	},
        	{
            "age": 3,
            "gender": "M",
            "id": 3,
            "name": "Example_3"
        	}
    	],
    	"success": true
	}
	```
	
#### POST /movies
* Creates a new movie.

* Requires `add:movie` permission

* Requires the title and release date.

* Responds with a 422 error if data is not provided.

* **Example Request:** (Create)
    ```bash
	curl --location --request POST 'http://localhost:5000/movies' \
		--header 'Content-Type: application/json' \
		--data-raw '{
            		"title" : "An Example",
            		"release_date": "1-2-1234"
        		}'
    ```
    
* **Example Response:**
    ```bash
	{
		"success": true
	}
    ```

#### POST /actors
* Creates a new actor.

* Requires `add:actor` permission

* Requires the name, age and gender of the actor.

* Responds with a 422 error if data is not provided.

* **Example Request:** (Create)
    ```json
	curl --location --request POST 'http://localhost:5000/actors' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Example",
			"age": "1",
			"gender": "M"
        }'
    ```
    
* **Example Response:**
    ```json
	{
		"success": true
    }
    ```

#### DELETE /movies/<int:movie_id>
* Deletes the movie with given id 

* Require `delete:movie` permission

* Responds with a 422 error if it is not found.

* **Example Request:** `curl --request DELETE 'http://localhost:5000/movies/1'`

* **Example Response:**
    ```json
	{

		"success": true
    }
    ```
    
#### DELETE /actors/<int:actor_id>
* Deletes the actor with given id 

* Require `delete:actor` permission

* Responds with a 422 error if it is not found.

* **Example Request:** `curl --request DELETE 'http://localhost:5000/actors/1'`

* **Example Response:**
    ```json
	{
		"success": true
    }
    ```

#### PATCH /movies/<movie_id>
* Updates the movie where <movie_id> is the existing movie id

* Require `update:movie` permission

* Responds with a 404 error if <movie_id> is not found

* Update the corresponding fields for Movie with id <movie_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/movies/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"title": "Example"
        }'
  ```
  
* **Example Response:**
    ```json
	{
		"movie": {
			"id": 1, 
			"release_date": "Wed, 01 June 1999 00:00:00 GMT", 
			"title": "Example"
		}
		"success": true
    }
    ```
	
#### PATCH /actors/<actor_id>
* Updates the actor where <actor_id> is the existing actor id

* Require `update:actor`

* Responds with a 404 error if <actor_id> is not found

* Update the given fields for Actor with id <actor_id>

* **Example Request:** 
	```json
    curl --location --request PATCH 'http://localhost:5000/actors/1' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Example"
        }'
  ```
  
* **Example Response:**
    ```json
	{
		"actor": { 
			"name": "Example",
			"Age: "1",
			"gender": M
			},
		"success": true
		}

### Error Handling

The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 422: Not Processable 
