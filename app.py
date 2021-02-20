import os
from flask import Flask, request, abort, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import actor, movie, setup_db, db


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET')
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            mov = movie.query.all()
            movies = [data.format() for data in mov]
            return jsonify({
                'success': True,
                'movies': movies
            }), 200
        except BaseException as e:
            print(e)
            abort(404)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(jwt, movie_id):
        mov = movie.query.filter(movie.id == movie_id).one_or_none()

        if mov is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movies': mov.format()
            }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movies(jwt):

        body = request.get_json()
        title = body.get('title')
        genres = body.get('genres')
        year = body.get('year')
        try:
            mov = movie(title=title, genres=genres, year=year)
            mov.insert()
            return jsonify({
                'success': True,
                'message': 'added Successfully',
                'movie': mov.format()
            }), 200
        except BaseException:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(jwt, movie_id):

        mov = movie.query.filter(movie.id == movie_id).one_or_none()

        if mov is None:
            abort(404)
        else:
            body = request.get_json()
            title = body.get('title')
            genres = body.get('genres')
            year = body.get('year')

        if title:
            mov.title = title
        if genres:
            mov.genres = genres
        if year:
            mov.year = year
        mov.update()
        return jsonify({
            'success': True,
            'message': 'Updated Successfully',
            'movie': mov.format()
        }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, movie_id):

        mov = movie.query.filter(movie.id == movie_id).one_or_none()

        if mov is None:
            abort(404)
        else:
            mov.delete()
            return jsonify({
                'success': True,
                'message': 'Deleted Successfully',
                'movie': mov.title
            }), 200

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):

        try:
            act = actor.query.all()
            actors = [data.format() for data in act]
            return jsonify({
                'success': True,
                'actors': actors
            }), 200
        except BaseException:
            abort(404)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(jwt, actor_id):
        act = actor.query.filter(actor.id == actor_id).one_or_none()

        if act is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actors': act.format()
            }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actors(jwt):

        body = request.get_json()
        name = body.get('name')
        age = int(body.get('age'))
        gender = body.get('gender')
        try:
            act = actor(name=name, age=age, gender=gender)
            act.insert()
            return jsonify({
                'success': True,
                'message': 'added Successfully',
                'actors': act.format()
            }), 200
        except BaseException:
            abort(422)

    @ app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(jwt, actor_id):
        act = actor.query.filter(actor.id == actor_id).one_or_none()
        if act is None:
            abort(404)
        else:
            body = request.get_json()
            name = body.get('name')
            age = int(body.get('age'))
            gender = body.get('gender')

            if name:
                act.name = name
            if age:
                act.age = age
            if gender:
                act.gender = gender

                act.update()

                return jsonify({
                    'success': True,
                    'message': 'Updated Successfully',
                    'actor': act.format()
                }), 200

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, actor_id):

        act = actor.query.filter(actor.id == actor_id).one_or_none()

        if act is None:
            abort(404)
        else:
            act.delete()
            return jsonify({
                'success': True,
                'message': 'Deleted Successfully',
                'actor': act.name
            }), 200

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        response = jsonify(exception.error)
        response.status_code = exception.status_code
        return response

    @app.errorhandler(AuthError)
    def handle_auth_error_404(x):
        return jsonify({
            "success": False,
            "error": x.status_code,
            "message": x.error
        }), 404

    @app.errorhandler(AuthError)
    def handle_auth_error_401(x):
        return jsonify({
            "success": False,
            "error": x.status_code,
            "message": x.error
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
