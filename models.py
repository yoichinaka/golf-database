import os, sys
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_filename = "golf"
project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path = "postgres://{}/{}".format('localhost:5432', database_filename)

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
    migrate = Migrate(app, db)
    print('setup%%%%%')


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable
     to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(), unique = False, nullable = True)
  name = db.Column(db.String(30), nullable=False)

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique = True, nullable = False )
    state = db.Column(db.String(120), nullable = True)
    image_link = db.Column(db.String(500), nullable = True)
    score = db.relationship('Score', backref='course')

    # def __repr__(self):
    #   return f'<Course {self.id} {self.name}>'
    
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

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True, nullable = False)
    # name must be unique
    user_id = db.Column(db.String(), unique = False, nullable = True)
    image_link = db.Column(db.String(500))
    seeking_course = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(120))
    best_score = db.Column(db.String(3))
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

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
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

class Drink(db.Model):
    # Autoincrementing, unique primary key

    id = db.Column(db.Integer, primary_key=True)
    #id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(100), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is
    #  [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        print(self.id, self.title)
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
