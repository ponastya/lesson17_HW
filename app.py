from flask import request
from flask_restx import Api, Resource
from marshmallow import Schema, fields
from create_data import *
from config import app


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


api = Api(app)
movie_ns = api.namespace("movies")
genre_ns = api.namespace("genres")
director_ns = api.namespace("directors")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# ===== Movie ======

@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        all_movies = db.session.query(Movie)
        #
        director_id = request.args.get("director_id")
        if director_id is not None:
            all_movies = all_movies.filter(Movie.director_id == director_id)
        genre_id = request.args.get("genre_id")
        if genre_id is not None:
            all_movies = all_movies.filter(Movie.genre_id == genre_id)

        return movies_schema.dump(all_movies.all()), 200

    def post(self):
        req_json = request.json
        print(req_json)
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

        return "", 201


@movie_ns.route("/<int:uid>/")
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = db.session.query(Movie).get(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404

    def put(self, uid):
        movie = db.session.query(Movie).filter(Movie.id == uid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


# ===== Directors ======
@director_ns.route("/")
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director)

        return directors_schema.dump(all_directors), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)

        with db.session.begin():
            db.session.add(new_director)

        return "", 201


@director_ns.route("/<int:uid>/")
class DirectorView(Resource):
    def get(self, uid: int):
        try:
            director = db.session.query(Director).get(uid)
            return director_schema.dump(director), 200
        except Exception as e:
            return "", 404

    def put(self, uid):
        director = db.session.query(Director).filter(Director.id == uid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        director = db.session.query(Director).get(uid)
        db.session.delete(director)
        db.session.commit()
        return "", 204


# ===== Genre ======
@genre_ns.route("/")
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre)

        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)

        with db.session.begin():
            db.session.add(new_genre)

        return "", 201


@genre_ns.route("/<int:uid>/")
class GenreView(Resource):
    def get(self, uid: int):
        try:
            genre = db.session.query(Genre).get(uid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404

    def put(self, uid):
        genre = db.session.query(Genre).filter(Genre.id == uid).update(request.json)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        genre = db.session.query(Genre).get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(host='127.0.0', port=80, debug=True)
