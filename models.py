import os, sys
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
#import json
#from flask_migrate import Migrate


#get the database URL from os environment
#For local, %export DATBASE_URL=postgre://localhost:5432/golf_test.
#For Herko, get DATABASE_URL from platform Config variables
database_path = os.environ['DATABASE_URL'] 

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #We have manage.py to use Migration process, we don't need db.create_all().
    #db.create_all()
    print('&&&& setup_ check database URL &&&&',database_path)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique = True, nullable = False )
    state = db.Column(db.String(120), nullable = True)
    image_link = db.Column(db.String(500), nullable = True)
    score = db.relationship('Score', backref='course')
    
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
        'state': self.state,
        'image_link': self.image_link
        }



class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True, nullable = False)
    # name must be unique
    user_id = db.Column(db.String(), unique = False, nullable = True)
    image_link = db.Column(db.String(500))
    score = db.relationship('Score', backref='player')

    def insert(self):
        db.session.add(self)
        print(sys.exc_info())
        db.session.commit()
        print(sys.exc_info())
        print('insert done')
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()
    def format(self):
        return {
        'id': self.id,
        'name': self.name,
        'image_link': self.image_link,
        'seeking_course': self.seeking_course,
        'seeking_description': self.seeking_description,
        'best_score': self.best_score
        }



class Score(db.Model):
    __tablename__ = 'score'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()


