import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, db
from auth.auth import AuthError, requires_auth
from flask_migrate import Migrate

RESULTS_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    results = [result.format() for result in selection]
    current_result = results[start:end]
    return current_result


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)


    @app.route('/')
    def status():
        return jsonify({'status': 'Running!!'}), 200
    # ROUTES
    '''
      GET /actors it should return list of actors
  '''

    @app.route('/actors')
    def get_actors():
        selection = Actor.query.order_by(Actor.id).all()
        current_actors = paginate_results(request, selection)
        if len(current_actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': current_actors
        }), 200

    '''
    Create an endpoint to POST a new actor
  '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor(token):
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        if not(name and age and gender):
            abort(422)
        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({'success': True}), 200
        except:
            abort(422)

    '''
      Create an endpoint to UPDATE actor's information
  '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(token, id):
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        if name:
            actor.name = name
        if age:
            actor.age = age
        if gender:
            actor.gender = gender
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    '''
    Create an endpoint to DELETE question using a question ID.
  '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            actor.delete()
            return jsonify({
                'success': True,
            }), 200
        except:
            abort(422)
    '''
      GET /moivies it should return list of movies
  '''

    @app.route('/movies')
    def get_movies():
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_results(request, selection)
        if len(current_movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': current_movies
        }), 200

    '''
      Create an endpoint to POST a new movie
  '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def create_movie(token):
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        if not(title and release_date):
            abort(422)
        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            return jsonify({'success': True}), 200
        except:
            abort(422)

    '''
      Create an endpoint to UPDATE movie's information
  '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(token, id):
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        body = request.get_json()
        title = body.get('title')
        release_date = body.get('release_date')
        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    '''
    Create an endpoint to DELETE question using a movie ID.
  '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            movie.delete()
            return jsonify({
                'success': True,
            }), 200
        except:
            abort(422)
    '''
  Create error handlers for all expected errors
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            'message': ex.error
        }), 401
    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
