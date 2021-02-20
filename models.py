import os
import psycopg2
from flask import Flask
from sqlalchemy import (Column, String, Integer, Table, ForeignKey)
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "capstone"
database_path = 'postgres://ypgbozimookkky:ffafc5535389b50429c888ca99959c802e5f5ca2ffe10255ca6ce5eef199438f@ec2-3-87-180-131.compute-1.amazonaws.com:5432/df300nbstbk47k'

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


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
        return f'<movie ID:{self.id}, name:{self.title}, Genres:{self.genres},  year:{self.year}>'

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
        return f'<actor ID:{self.id}, name:{self.name}, age:{self.age}, gender:{self.gender}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        """returns a formatted response of the data in the model"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
