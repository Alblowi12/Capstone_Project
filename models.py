import os
import psycopg2
from flask import Flask
from sqlalchemy import (Column, String, Integer, Table, ForeignKey)
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    app.secret_key = os.getenv('SECRET')


def init_db():
    db.drop_all()
    db.create_all()


casting = db.Table(
    'casting',
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actor.id')),
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movie.id')))


class movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'genres': self.genres,
            'year': self.year,
        }


class actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    Role = db.relationship('movie', secondary=casting,
                           backref='movies_list', lazy=True)

    def __repr__(self):
        return json.dumps(self.format())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
