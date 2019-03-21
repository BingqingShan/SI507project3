import os
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movie_db.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy



##### Set up Models #####

# Set up association Table
collections = db.Table('collections',db.Column('director_id',db.Integer, db.ForeignKey('Directors.id')),db.Column('distributor_id',db.Integer, db.ForeignKey('Distributors.id')))

class Distributor(db.Model):
    __tablename__ = "Distributors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    directors = db.relationship('Director',secondary=collections,backref=db.backref('Distributors',lazy='dynamic'),lazy='dynamic')
    movies = db.relationship('Movie',backref='Distributor')


class Director(db.Model):
    __tablename__ = "Directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    movies = db.relationship('Movie',backref='Director')

    def __repr__(self):
        return "{} (ID: {})".format(self.lastname, self.firstname, self.id)


class Movie(db.Model):
    __tablename__ = "Movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title songs can exist in this data model
    director_id = db.Column(db.Integer, db.ForeignKey("Directors.id")) # ok to be null for now
    distributor_id = db.Column(db.Integer, db.ForeignKey("Distributors.id")) #ok to be null for now
    major_genre = db.Column(db.String(64))
    us_gross = db.Column(db.Integer)
    worldwide_gross = db.Column(db.Integer)
    us_dvd_sales = db.Column(db.Integer)
    production_budget = db.Column(db.Integer)
    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.director_id, self.distributor_id, self.major_genre)


##### Helper functions #####

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

def get_or_create_distributor(distributor_name):
    distributor = Distributor.query.filter_by(name=distributor_name).first()
    if distributor:
        return distributor
    else:
        distributor = Distributor(name=distributor_name)
        session.add(distributor)
        session.commit()
        return distributor


##### Set up Controllers (route functions) #####

@app.route('/movie/new/<title>/<director>/<distributor>/<major_genre>/<us_gross>/<worldwide_gross>/<us_dvd_sales>/<production_budget>/')
def new__movie(title, director, distributor, major_genre,us_gross,worldwide_gross,us_dvd_sales,production_budget):
    if Movie.query.filter_by(title=title).first():
        return "That movie already exists. Go back to the main app."
    else:
        director = get_or_create_director(director)
        distributor = get_or_create_distributor(distributor)
        movie = Movie(title=title, director_id=director.id,distributor_id=distributor.id,major_genre=major_genre,us_gross=us_gross,worldwide_gross=worldwide_gross,us_dvd_sales=us_dvd_sales,production_budget=production_budget)
        session.add(movie)
        session.commit()
        return "New movie: {} directed by {}, distributed by {}, has been saved in the list. More info: Major Genre: {}; US Gross: {}, Worldwide Gross: {}, US DVD Sales: {}, Production Budget: {}. ".format(movie.title, director.name,distributor.name,movie.major_genre,movie.us_gross,movie.worldwide_gross,movie.us_dvd_sales,movie.production_budget)

@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/all_movies')
def see_all():
    all_movies = []
    movies = Movie.query.all()
    for i in movies:
        all_movies.append((i.title))
    return render_template('all_movies.html',all_movies=all_movies)

@app.route('/all_directors')
def see_director():
    all_directors = []
    directors = Director.query.all()
    for i in directors:
        all_directors.append((i.name))
    return render_template('all_directors.html',all_directors=all_directors)


if __name__ == '__main__':
    db.create_all()
    app.run() 
